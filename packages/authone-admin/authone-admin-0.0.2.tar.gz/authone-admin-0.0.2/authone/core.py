import os

import authone
from authone.config import api_secret_api_key_missing_message
from authone.error import AuthenticationError
from authone.resources.base import ResourceComponent


RETRIES = 3
TIMEOUT = 10
BACKOFF_FACTOR = 0.02


class AuthOne:

    def __getattr__(self, attribute_name):
        try:
            return getattr(self._resource, attribute_name)
        except AttributeError:
            pass

        return super().__getattribute__(attribute_name)

    def __init__(
        self,
        app_id,
        app_secret=None,
        retries=RETRIES,
        timeout=TIMEOUT,
        backoff_factor=BACKOFF_FACTOR,
    ):
        self._resource = ResourceComponent()

        self._resource.setup_request_client(retries, timeout, backoff_factor)
        self._set_api_secret_key(app_secret)

    def _set_api_secret_key(self, api_secret_key):
        authone.api_secret_key = api_secret_key or os.environ.get(
            'AUTHONE_APP_SECRET',
        )

        if authone.api_secret_key is None:
            raise AuthenticationError(api_secret_api_key_missing_message)
