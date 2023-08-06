import urllib.parse

import xmatters.auth
import xmatters.connection
import xmatters.endpoints
import xmatters.errors


class XMSession(object):
    """
    Starting class used to interact with xMatters API.

    :param str xm_url: Name of xMatters instance, xMatters instance url, or xMatters instance API base url
    :type base_url: str
    :keyword timeout: timeout (in seconds) for requests. Defaults to 5.
    :type timeout: int
    :keyword max_retries: maximum number of request retries to attempt. Defaults to 3.
    :type max_retries: int
    """

    _endpoints = {'audits': xmatters.endpoints.AuditsEndpoint,
                  'conference-bridges': xmatters.endpoints.ConferenceBridgesEndpoint,
                  'device-names': xmatters.endpoints.DeviceNamesEndpoint,
                  'device-types': xmatters.endpoints.DeviceTypesEndpoint,
                  'devices': xmatters.endpoints.DevicesEndpoint,
                  'dynamic-teams': xmatters.endpoints.DynamicTeamsEndpoint,
                  'events': xmatters.endpoints.EventsEndpoint,
                  'forms': xmatters.endpoints.FormsEndpoint,
                  'imports': xmatters.endpoints.ImportsEndpoint,
                  'groups': xmatters.endpoints.GroupsEndpoint,
                  'incident': xmatters.endpoints.IncidentsEndpoint,
                  'on-call': xmatters.endpoints.OnCallEndpoint,
                  'on-call-summary': xmatters.endpoints.OnCallSummaryEndpoint,
                  'people': xmatters.endpoints.PeopleEndpoint,
                  'plans': xmatters.endpoints.PlansEndpoint,
                  'roles': xmatters.endpoints.RolesEndpoint,
                  'scenarios': xmatters.endpoints.ScenariosEndpoint,
                  'services': xmatters.endpoints.ServicesEndpoint,
                  'sites': xmatters.endpoints.SitesEndpoint,
                  'subscriptions': xmatters.endpoints.SubscriptionsEndpoint,
                  'subscription-forms': xmatters.endpoints.SubscriptionFormsEndpoint,
                  'temporary-absences': xmatters.endpoints.TemporaryAbsencesEndpoint}

    def __init__(self, xm_url, **kwargs):
        p_url = urllib.parse.urlparse(xm_url)
        if '.' not in xm_url:
            instance_url = 'https://{}.xmatters.com'.format(p_url.path)
        else:
            instance_url = 'https://{}'.format(p_url.netloc) if p_url.netloc else 'https://{}'.format(p_url.path)
        self._api_base_url = '{}/api/xm/1'.format(instance_url)
        self.con = None
        self._kwargs = kwargs

    def set_authentication(self, username=None, password=None, client_id=None, **kwargs):
        """
        Set the authentication method when interacting with the API.
        OAuth2 authentication is used if a client_id is provided; otherwise basic authentication is used.

        :param username: xMatters username
        :type username: str
        :param password: xMatters password
        :type password: str
        :param client_id: xMatters instance client id
        :type client_id: str
        :keyword token: token object
        :type token: dict
        :keyword refresh_token: refresh token
        :type refresh_token: str
        :keyword token_storage: Class instance used to store token.
            Any class instance should work as long is it has *read_token* and *write_token* methods.
        :type token_storage: object
        :return: self
        :rtype: :class:`xmatters.XMSession`

        """

        # add init kwargs inorder to pass to Connection init
        kwargs.update(self._kwargs)

        if client_id:
            self.con = xmatters.auth.OAuth2Auth(self._api_base_url, client_id, username, password, **kwargs)
        elif None not in (username, password):
            self.con = xmatters.auth.BasicAuth(self._api_base_url, username, password, **kwargs)
        else:
            raise xmatters.errors.AuthorizationError('unable to determine authentication method')

        # return self so method can be chained
        return self

    def get_endpoint(self, endpoint):
        """
        Get top-level endpoint.

        :param endpoint: top-level endpoint
        :type endpoint: str
        :return: Endpoint object
        :rtype: object

        """
        endpoint_object = self._endpoints.get(endpoint.strip('/'))
        if not endpoint_object:
            raise NotImplementedError('{} endpoint is not implemented'.format(endpoint))
        return endpoint_object(self)

    def audits_endpoint(self):
        """
        Get the '/audits' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.AuditsEndpoint`
        """
        return xmatters.endpoints.AuditsEndpoint(self)

    def conference_bridges_endpoint(self):
        """
        Get the '/conference-bridges' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.ConferenceBridgesEndpoint`
        """
        return xmatters.endpoints.ConferenceBridgesEndpoint(self)

    def device_names_endpoint(self):
        """
        Get the '/device-names' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.DeviceNamesEndpoint`
        """
        return xmatters.endpoints.DeviceNamesEndpoint(self)

    def device_types_endpoint(self):
        """
        Get the '/device-types' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.DeviceTypesEndpoint`
        """
        return xmatters.endpoints.DeviceTypesEndpoint(self)

    def devices_endpoint(self):
        """
        Get the '/device' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.DevicesEndpoint`
        """
        return xmatters.endpoints.DevicesEndpoint(self)

    def dynamic_teams_endpoint(self):
        """
        Get the '/dynamic-teams' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.DynamicTeamsEndpoint`
        """
        return xmatters.endpoints.DynamicTeamsEndpoint(self)

    def events_endpoint(self):
        """
        Get the '/events' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.EventsEndpoint`
        """
        return xmatters.endpoints.EventsEndpoint(self)

    def event_suppressions_endpoint(self):
        """
        Get the '/event-suppressions' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.EventSuppressionsEndpoint`
        """
        return xmatters.endpoints.EventSuppressionsEndpoint(self)

    def forms_endpoint(self):
        """
        Get the '/forms' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.FormsEndpoint`
        """
        return xmatters.endpoints.FormsEndpoint(self)

    def imports_endpoint(self):
        """
        Get the '/import-jobs' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.ImportsEndpoint`
        """
        return xmatters.endpoints.ImportsEndpoint(self)

    def groups_endpoint(self):
        """
        Get the '/groups' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.GroupsEndpoint`
        """
        return xmatters.endpoints.GroupsEndpoint(self)

    def incidents_endpoint(self):
        """
        Get the '/incidents' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.IncidentsEndpoint`
        """
        return xmatters.endpoints.IncidentsEndpoint(self)

    def oncall_endpoint(self):
        """
        Get the '/on-call' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.OnCallEndpoint`
        """
        return xmatters.endpoints.OnCallEndpoint(self)

    def oncall_summary_endpoint(self):
        """
        Get the '/on-call-summary' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.OnCallSummaryEndpoint`
        """
        return xmatters.endpoints.OnCallSummaryEndpoint(self)

    def people_endpoint(self):
        """
        Get the '/people' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.PeopleEndpoint`
        """
        return xmatters.endpoints.PeopleEndpoint(self)

    def plans_endpoint(self):
        """
        Get the '/plans' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.PlansEndpoint`
        """
        return xmatters.endpoints.PlansEndpoint(self)

    def roles_endpoint(self):
        """
        Get the '/roles' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.RolesEndpoint`
        """
        return xmatters.endpoints.RolesEndpoint(self)

    def scenarios_endpoint(self):
        """
        Get the '/scenarios' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.ScenariosEndpoint`
        """
        return xmatters.endpoints.ScenariosEndpoint(self)

    def services_endpoint(self):
        """
        Get the '/services' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.ServicesEndpoint`
        """
        return xmatters.endpoints.ServicesEndpoint(self)

    def sites_endpoint(self):
        """
        Get the '/sites' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.SitesEndpoint`
        """
        return xmatters.endpoints.SitesEndpoint(self)

    def subscriptions_endpoint(self):
        """
        Get the '/subscriptions' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.SubscriptionsEndpoint`
        """
        return xmatters.endpoints.SubscriptionsEndpoint(self)

    def subscription_forms_endpoint(self):
        """
        Get the '/subscription-forms' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.SubscriptionFormsEndpoint`
        """
        return xmatters.endpoints.SubscriptionFormsEndpoint(self)

    def temporary_absences_endpoint(self):
        """
        Get the '/temporary-absences' top-level endpoint.

        :return: Endpoint
        :rtype: :class:`xmatters.endpoints.TemporaryAbsencesEndpoint`
        """
        return xmatters.endpoints.TemporaryAbsencesEndpoint(self)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
