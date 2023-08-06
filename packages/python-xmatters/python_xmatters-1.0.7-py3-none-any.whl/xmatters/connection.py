import json
import warnings
from urllib import parse

from requests.adapters import HTTPAdapter
from requests_oauthlib.oauth2_session import TokenUpdated
from urllib3.util.retry import Retry

import xmatters.errors as err
import xmatters.utils as util
import xmatters.auth

# ignore TokenUpdated warning
# only occurs when token_updater isn't defined in OAuth2Session
warnings.simplefilter('always', TokenUpdated)


class Connection(object):
    def __init__(self, auth, **kwargs):
        self.auth = auth
        self.base_url = self.auth.base_url
        p_url = parse.urlparse(self.base_url)
        self.api_path = p_url.path
        self.instance_url = 'https://{}'.format(p_url.netloc)
        self.timeout = kwargs.get('timeout', 1)
        self.max_retries = kwargs.get('max_retries', 3)
        self.limit_per_request = kwargs.get('limit_per_request', util.MAX_API_LIMIT)

    def get(self, url, params=None):
        return self.request('GET', url=url, params=params)

    def post(self, url, data):
        return self.request('POST', url=url, data=data)

    def delete(self, url):
        return self.request('DELETE', url=url)

    def request(self, method, url, data=None, params=None):
        if params:
            # set number of items returned per request
            if 'limit' in params.keys() and params.get('limit') is None:
                params['limit'] = self.limit_per_request
            # remove all None values
            params = {k: v for k, v in params.items() if v is not None}

        r = self.auth.session.request(method=method, url=url, params=params, json=data, timeout=self.timeout)

        # xMatters token likely expired when preparing call
        if r.status_code == 401 and isinstance(self.auth, xmatters.auth.OAuth2Auth):
            self.auth.refresh_token()
            r = self.auth.session.request(method=method, url=url, params=params, json=data, timeout=self.timeout)

        if not r.ok or r.status_code == 204:
            raise err.ErrorFactory.compose(r.status_code, data)

        try:
            data = r.json()
        except json.decoder.JSONDecodeError:
            raise err.ApiError(r.status_code, r.text)

        return data

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, retries):
        self._max_retries = retries
        retry = Retry(total=retries,
                      backoff_factor=0.5,
                      status_forcelist=[500, 502, 503, 504])
        retry_adapter = HTTPAdapter(max_retries=retry)
        self.auth.session.mount('https://', retry_adapter)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ApiBridge(object):
    """ Base for api objects that need to make requests """

    def __init__(self, parent, data=None):
        if hasattr(parent, 'con') and not parent.con:
            raise err.AuthorizationError('authentication not provided')

        self.con = parent.con
        self.self_url = None
        self_link = data.get('links', {}).get('self') if data else None
        self.self_url = '{}{}'.format(self.con.instance_url, self_link) if self_link else None

    def build_url(self, endpoint):
        # don't do anything if endpoint is full path
        if self.con.instance_url in endpoint:
            return endpoint

        if endpoint.startswith(self.con.api_path):
            url_prefix = self.con.instance_url
        elif self.self_url:
            url_prefix = self.self_url
        else:
            url_prefix = self.con.base_url
        return '{}{}'.format(url_prefix, endpoint)

    # TODO: update to handle datetime objects
    @staticmethod
    def process_time_param(param):
        """
        Formats iso-formatted date (or date and time) from provided timezone to UTC timezone.
        If no timezone is specified, local timezone is used.
        :param param: iso-formatted date, or date and time
        :type param: str
        :return: date & time with utc offset applied
        :rtype: str or None
        """
        return util.TimeAttribute(param).isoformat_utc() if isinstance(param, str) else param

    # TODO: Test
    @staticmethod
    def process_search_param(param):
        return ' '.join([str(p) for p in param]) if isinstance(param, list) else param
