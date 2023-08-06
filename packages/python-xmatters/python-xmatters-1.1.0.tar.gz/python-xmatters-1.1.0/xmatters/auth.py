import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from xmatters import errors as err
from xmatters.connection import Connection


class OAuth2Auth(Connection):
    _endpoints = {'token': '/oauth2/token'}

    def __init__(self, api_base_url, client_id, username=None, password=None, **kwargs):

        self.api_base_url = api_base_url
        self.client_id = client_id
        self.username = username
        self.password = password
        self._token = kwargs.get('token')
        self._refresh_token = kwargs.get('refresh_token')
        self.token_storage = kwargs.get('token_storage')
        self.session = None
        token_url = '{}{}'.format(self.api_base_url, self._endpoints.get('token'))
        client = LegacyApplicationClient(client_id=self.client_id)
        auto_refresh_kwargs = {'client_id': self.client_id}
        token_updater = self.token_storage.write_token if self.token_storage else None
        self.session = OAuth2Session(client=client, auto_refresh_url=token_url,
                                     auto_refresh_kwargs=auto_refresh_kwargs,
                                     token_updater=token_updater)
        # OAuth2Session must be initiated before inheritance inorder to process passed XMSession kwargs
        super(OAuth2Auth, self).__init__(self, **kwargs)
        self._set_token()

    def refresh_token(self):
        """
        Refreshes the session token.
        Token is automatically applied to the session and stored in token_storage (if defined).
        :return: token object
        :rtype: dict
        """

        refresh_token = self._refresh_token or self.token.get('refresh_token')
        token = self.session.refresh_token(token_url=self.session.auto_refresh_url, refresh_token=refresh_token,
                                           kwargs=self.session.auto_refresh_kwargs)
        self._update_storage()
        # Return in-case user wants it
        return token

    def fetch_token(self):
        """
        Fetches session token.
        Token is automatically applied to the session and stored in token_storage (if defined).
        :return: token object
        :rtype: dict
        """
        token = self.session.fetch_token(token_url=self.session.auto_refresh_url, username=self.username,
                                         password=self.password, include_client_id=True)
        self._update_storage()
        # Return in-case user wants it
        return token

    def _update_storage(self):
        if self.token_storage:
            self.token_storage.write_token(self.token)

    def _set_token(self):
        if self._token:
            self.token = self._token
            self._update_storage()
        elif self._refresh_token:
            self.refresh_token()
        elif None not in (self.username, self.password):
            self.fetch_token()
        elif self.token_storage and self.token_storage.read_token():
            self.token = self.token_storage.read_token()
        else:
            raise err.AuthorizationError('Unable to obtain token with provided arguments')

    @property
    def token(self):
        return self.session.token if self.session else self._token

    @token.setter
    def token(self, token):
        if self.session:
            self.session.token = token
        else:
            self._token = token

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class BasicAuth(Connection):
    """
    Used to authentication requests using basic authentication

    :param base_url: xMatters instance url or xMatters instance base url
    :type base_url: str
    :param username: xMatters username
    :type username: str
    :param password: xMatters password
    :type password: str
    """

    def __init__(self, api_base_url, username, password, **kwargs):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.api_base_url = api_base_url
        self.session.auth = (self.username, self.password)
        super(BasicAuth, self).__init__(self, **kwargs)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
