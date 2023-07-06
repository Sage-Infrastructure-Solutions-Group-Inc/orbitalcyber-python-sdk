from logging import getLogger
from datetime import datetime
from uuid import uuid1

VALID_METHODS = ['get', 'post', 'put', 'patch', 'delete']


class OrbitalClient:
    session = None
    session_token = None
    id = None
    key = None
    secret = None
    logger = None
    api_host = None
    last_request = None
    max_retries = 3
    rate_limit = 1

    def __init__(self, id: str, key: str, secret: str, disable_ssl_verification: bool = False, proxy_config: dict = {},
                 api_host: str = "https://app.orbitalcyber.com"):
        from requests import Session
        from urllib.parse import urlparse
        self.id = id
        self.key = key
        self.secret = secret
        # Using this to error check that a valid URL has been passed to the constructor
        self.api_host = urlparse(api_host).geturl()
        self.logger = getLogger(
            str(self.__class__) + '-' + str(uuid1()))  # Create a logger with a globally unique name.
        self.session = Session()
        if disable_ssl_verification:
            self.logger.warning(f"SSL verification has been disabled for requests to the OrbitalCyber API")
            self.session.verify = False
        if proxy_config:
            self.session.proxies = proxy_config
        self.session.headers.update({'client-type': '1'})
        self.authenticate()


    def authenticate(self):
        from orbitalcyber.exceptions import OrbitalCyberAuthenticationError
        self.logger.debug(f"Attempting to authenticate to API at host: {self.api_host}")
        response = self.post('/api/auth/', json={'client_key': self.key, 'client_secret': self.secret})
        if response.status_code == 200:
            if response.json() is None:
                raise ValueError(f"Client did not receive expected response from the server.")
            self.session_token = response.json().get('cookie')
            if not self.session_token:
                raise OrbitalCyberAuthenticationError()
            self.session.headers['api-auth'] = self.session_token
        else:
            raise OrbitalCyberAuthenticationError()

    def post(self, api_path: str, **kwargs):
        return self.make_request('post', api_path, **kwargs)

    def get(self, api_path: str, **kwargs):
        return self.make_request('get', api_path, **kwargs)

    def delete(self, api_path: str, **kwargs):
        return self.make_request('delete', api_path, **kwargs)

    def patch(self, api_path: str, **kwargs):
        return self.make_request('patch', api_path, **kwargs)

    def put(self, api_path: str, **kwargs):
        return self.make_request('put', api_path, **kwargs)

    def enforce_rate_limit(self):
        from time import sleep
        if not self.last_request:
            return None
        now = datetime.utcnow()
        request_delta = now - self.last_request
        rate_limit_factor = 1 / self.rate_limit
        if request_delta.total_seconds() < rate_limit_factor:
            # We have not exceeded the rate limit
            return None
        self.logger.debug(f"Rate limit has been exceeded. Sleep for {rate_limit_factor} seconds.")
        sleep(rate_limit_factor)

    def make_request(self, method: str, api_path: str, retries: int = 0, **kwargs):
        self.enforce_rate_limit()
        method = method.lower()
        if method not in VALID_METHODS:
            raise ValueError(f"Invalid HTTP method: {method}")
        response = self.session.request(method, self.api_host + api_path, headers=self.session.headers, **kwargs)
        self.last_request = datetime.utcnow()
        if response.status_code != 200:
            self.logger.debug(f"Got non 200 status code from server ({response.status_code}) requesting path: {api_path}")
        if response.status_code == 401:
            # Session has likely expired
            self.authenticate()
            if retries > self.max_retries:
                raise ValueError(f"Client was unable to authenticate. Retry limit of {self.max_retries} has been "
                                 f"exceeded")
            return self.make_request(method, api_path, retries = retries + 1, **kwargs)
        if response.status_code == 500:
            if retries > self.max_retries:
                raise ValueError(f"Got server error of 500 too many times. Retry limit of {self.max_retries} has been "
                                 f"exceeded")
            return self.make_request(method, api_path, retries = retries + 1, **kwargs)
        return response
