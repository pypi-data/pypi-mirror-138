import json
import os

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import ConnectTimeout, ReadTimeout

DEFAULT_URL = "https://api.freedomrobotics.ai"

default_api = None


def set_default_api(api):
    global default_api
    default_api = api


def api_auth(token, secret, url=DEFAULT_URL):
    global default_api
    default_api = APIHandler.get_instance(token=token, secret=secret, url=url)


def api_call(*args, **kwargs):
    global default_api
    return default_api.call(*args, **kwargs)


class APIHandler(object):

    def __init__(self,
                 token=None,
                 secret=None,
                 url=DEFAULT_URL,
                 retry_config=None,
                 profiler=False,
                 profiler_min_duration=1,
                 global_timeout=30,
                 ):
        """Class that perform all the requests to the API

        Args:
            token (str): API token. Can be a session or user token.
            secret (str): API secret.
            url (str): Optional url to point to a specific API.
            retry_config (dict): Configuration for requests retry.
                By default it will use the usual requests configuration
            profiler (bool): If enabled, will enable the profiler on all API requests.
            profiler_min_duration (float/int): If profiler is enabled, will add the min duration
                for a profile results to be dumped on the API side.
            global_timeout (float/int): Default timeout for all API requests. By default is 30, which
                is the lambda timeout for the API.
        """
        self.token = token
        self.secret = secret
        self.url = url
        if retry_config is None:
            retry_config = {}
        self.retry_config = retry_config
        self.profiler = profiler
        self.profiler_min_duration = profiler_min_duration
        self.global_timeout = global_timeout

    def get_session(self):
        session = requests.Session()
        if self.retry_config:
            retry = Retry(
                total=self.retry_config.get('total', 3),
                backoff_factor=self.retry_config.get('backoff_factor', 1),
                status_forcelist=self.retry_config.get('status_forcelist', (500, 502, 504))
            )
            adapter = HTTPAdapter(
                max_retries=retry,
                pool_connections=self.retry_config.get('pool_connections', 10),
                pool_maxsize=self.retry_config.get('pool_maxsize', 10)
            )
            session.mount('http://', adapter)
            session.mount('https://', adapter)
        return session

    @classmethod
    def get_instance(cls, url=None, token=None, secret=None, username=None, password=None, **kwargs):
        if token is not None and secret is not None:
            token = token
            secret = secret
            if url is None:
                url = DEFAULT_URL

        # if class is initialized with a username and password, use it
        elif username is not None and password is not None:
            if url is None:
                url = DEFAULT_URL
            response = cls.simple_call(
                url,
                "PUT",
                "/users/{}/login".format(username),
                data={
                    "password": password
                }
            )
            token = response.get("token")
            secret = response.get("secret")

        # if there is a saved freedom credentials file, use it
        elif os.path.exists(os.path.expanduser("~/.freedom_credentials")):
            with open(os.path.expanduser("~/.freedom_credentials")) as f:
                credentials = json.load(f)
                if url is None:
                    url = credentials.get("url", DEFAULT_URL)
                token = credentials.get("token")
                secret = credentials.get("secret")
        else:
            raise Exception("Required: either token/secret, username/password, or saved ~/.freedom_credentials file")

        api = cls(token, secret, url=url, **kwargs)
        if default_api is None:
            set_default_api(api)
        return api

    @classmethod
    def simple_call(cls, url, *args, **kwargs):
        instance = cls(url=url)
        return instance.call(no_auth=True, *args, **kwargs)

    def call(self, method, path, data=None, params=None, no_auth=False, raw=False, timeout=None):
        if method.upper() not in ['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS']:
            raise Exception("Invalid method ")

        if no_auth:
            auth_headers = {}
        else:
            auth_headers = {
                "mc_token": self.token,
                "mc_secret": self.secret,
            }
        if self.profiler:
            if params is None:
                params = {}
            params['profiler'] = 'enable'
            params['profiler_min_duration'] = self.profiler_min_duration

        request_kwargs = dict(
            headers=auth_headers,
            params=params,
        )
        timeout = timeout if timeout is not None else self.global_timeout
        if timeout is not None:
            request_kwargs['timeout'] = timeout

        if method.upper() in ['PUT', 'POST']:
            request_kwargs['json'] = data

        url = self.url.strip("/") + "/" + path.strip("/")

        with self.get_session() as session:
            func = getattr(session, method.lower())
            try:
                response = func(url, **request_kwargs)
            except (ConnectTimeout, ReadTimeout) as e:
                raise RequestTimeoutError(e)

        if response.status_code >= 400:
            raise APIError.from_response(response)

        try:
            if raw:
                return response.text
            else:
                return response.json()
        except ValueError:
            raise ServerError(
                "Error parsing API response to JSON: [{}] {}".format(response.status_code, response.text)
            )


class APIError(Exception):
    ERROR = "API Error"

    def __init__(self, response):
        self.response = response
        super().__init__(self.make_message())

    def make_message(self):
        try:
            body = self.response.json()
            body = body.get("Message", self.response.text)
        except ValueError:
            body = self.response.text
        return "{} [{}]: {}".format(self.ERROR, self.response.status_code, body)

    @classmethod
    def from_response(cls, response):
        if response.status_code in (401, 403):
            return UnauthorizedError(response)
        elif response.status_code == 404:
            return NotFoundError(response)
        elif response.status_code >= 500:
            return ServerError(response)
        else:
            return cls(response)


class UnauthorizedError(APIError):
    ERROR = "Unauthorized"


class NotFoundError(APIError):
    ERROR = "Not Found"


class ServerError(APIError):
    ERROR = "Server Error"


class RequestTimeoutError(APIError):

    def __init__(self, request_exception):
        if isinstance(request_exception, ConnectTimeout):
            msg = "Timeout when connecting to the API: {}".format(request_exception)
        elif isinstance(request_exception, ReadTimeout):
            msg = "Timeout when reading response from the API: {}".format(request_exception)
        Exception.__init__(self, msg)
