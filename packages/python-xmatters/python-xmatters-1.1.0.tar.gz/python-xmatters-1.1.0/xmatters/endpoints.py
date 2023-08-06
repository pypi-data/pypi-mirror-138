import xmatters.factories as factory
import xmatters.objects.forms
from xmatters.connection import ApiBridge
from xmatters.objects.common import Pagination
from xmatters.objects.conference_bridges import ConferenceBridge
from xmatters.objects.device_types import DeviceTypes
from xmatters.objects.dynamic_teams import DynamicTeam
from xmatters.objects.event_supressions import EventSuppression
from xmatters.objects.events import Event
from xmatters.objects.groups import Group, GroupQuota
from xmatters.objects.import_jobs import Import
from xmatters.objects.incidents import Incident
from xmatters.objects.oncall import OnCall
from xmatters.objects.oncall_summary import OnCallSummary
from xmatters.objects.people import Person, UserQuota
from xmatters.objects.plans import Plan
from xmatters.objects.roles import Role
from xmatters.objects.scenarios import Scenario
from xmatters.objects.services import Service
from xmatters.objects.sites import Site
from xmatters.objects.subscription_forms import SubscriptionForm
from xmatters.objects.subscriptions import Subscription
from xmatters.objects.temporary_absences import TemporaryAbsence


class AuditsEndpoint(ApiBridge):
    """ Used to interact with '/audits' top-level endpoint """
    def __init__(self, parent):
        super(AuditsEndpoint, self).__init__(parent, '/audits')

    def get_audits(self, params=None, **kwargs):
        """
        | Get audit information.
        | See `xMatters REST API Reference <https://help.xmatters.com/xmapi/>`_ for valid query parameters.

        :return: Pagination of audit objects
        :rtype: :class:`xmatters.objects.common.Pagination`
        """
        url = self.get_url()
        data = self.con.get(url=url, params=params, **kwargs)
        return Pagination(self, data, xmatters.factories.AuditFactory) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DevicesEndpoint(ApiBridge):
    """ Used to interact with '/devices' top-level endpoint """

    def __init__(self, parent):
        super(DevicesEndpoint, self).__init__(parent, '/devices')

    def get_devices(self, params=None, **kwargs):
        """
        | Get devices.
        | See `xMatters REST API Reference <https://help.xmatters.com/xmapi/>`_ for valid query parameters.

        :return: Pagination of device objects
        :rtype: :class:`xmatters.objects.common.Pagination`
        """
        url = self.get_url()
        data = self.con.get(url=url, params=params, **kwargs)
        return Pagination(self, data, xmatters.factories.DeviceFactory) if data.get('data') else []

    def get_device_by_id(self, device_id, params=None, **kwargs):
        """
        | Get device by device's id.
        | See `xMatters REST API Reference <https://help.xmatters.com/xmapi/>`_ for valid query parameters.

        :return: Pagination of device objects
        :rtype: :class:`xmatters.objects.common.Pagination`
        """
        url = self.get_url(device_id)
        data = self.con.get(url=url, params=params, **kwargs)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def create_device(self, data):
        """
        | Create a device.
        | See `xMatters REST API Reference <https://help.xmatters.com/xmapi/>`_ for expected data.

        :return: device object
        :rtype: Dependent on device type
        """
        url = self.get_url()
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def update_device(self, data):
        """
        | Update a device.
        | See `xMatters REST API Reference <https://help.xmatters.com/xmapi/>`_ for expected data.

        :return: device object
        :rtype: Dependent on device type
        """
        url = self.get_url()
        data = self.con.post(url=url, data=data)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def delete_device(self, device_id):
        """
        | Delete a device.

        :param device_id: device id
        :type device_id: str
        :return: device object
        :rtype: Dependent on device type
        """
        url = self.get_url(device_id)
        data = self.con.delete(url=url)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceNamesEndpoint(ApiBridge):

    """ Used to interact with '/device-names' top-level endpoint """

    def __init__(self, parent):
        super(DeviceNamesEndpoint, self).__init__(parent, '/device-names')

    def get_device_names(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url=url, params=params, **kwargs)
        return Pagination(self, data, factory.DeviceNameFactory) if data.get('data') else []

    def create_device_name(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceNameFactory.compose(self, data) if data else None

    def update_device_name(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceNameFactory.compose(self, data) if data else None

    def delete_device_name(self, device_name_id):
        url = self.get_url(device_name_id)
        data = self.con.delete(url)
        return xmatters.factories.DeviceNameFactory.compose(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceTypesEndpoint(ApiBridge):

    def __init__(self, parent):
        super(DeviceTypesEndpoint, self).__init__(parent, '/device-types')

    def get_device_types(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return DeviceTypes(data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DynamicTeamsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(DynamicTeamsEndpoint, self).__init__(parent, '/dynamic-teams')

    def get_dynamic_teams(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, DynamicTeam) if data.get('data') else []

    def get_dynamic_team_by_id(self, dynamic_team_id, params=None, **kwargs):
        url = self.get_url(dynamic_team_id)
        data = self.con.get(url, params=params, **kwargs)
        return DynamicTeam(self, data) if data else None

    def create_dynamic_team(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    def update_dynamic_team(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    def delete_dynamic_team(self, dynamic_team_id):
        url = self.get_url(dynamic_team_id)
        data = self.con.delete(url=url)
        return DynamicTeam(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(EventsEndpoint, self).__init__(parent, '/events')

    def get_events(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Event) if data.get('data') else []

    def get_event_by_id(self, event_id, params=None, **kwargs):
        url = self.get_url(event_id)
        data = self.con.get(url, params=params, **kwargs)
        return Event(self, data) if data else None

    def change_event_status(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Event(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventSuppressionsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(EventSuppressionsEndpoint, self).__init__(parent, '/event-suppressions')

    def get_suppressions_by_event_id(self, event_id, params=None, **kwargs):
        url = self.get_url(event_id)
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, EventSuppression) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferenceBridgesEndpoint(ApiBridge):

    def __init__(self, parent):
        super(ConferenceBridgesEndpoint, self).__init__(parent, '/conference-bridges')

    def get_conference_bridges(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, ConferenceBridge) if data.get('data') else []

    def get_conference_bridge_by_id(self, bridge_id, params=None, **kwargs):
        url = self.get_url(bridge_id)
        data = self.con.get(url, params=params, **kwargs)
        return ConferenceBridge(self, data) if data else None

    def create_conference_bridge(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    def update_conference_bridge(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    def delete_conference_bridge(self, bridge_id):
        url = self.get_url(bridge_id)
        data = self.con.delete(url=url)
        return ConferenceBridge(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class FormsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(FormsEndpoint, self).__init__(parent, '/forms')

    def get_forms(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, xmatters.objects.forms.Form) if data.get('data') else []

    def get_form_by_id(self, form_id, params=None, **kwargs):
        url = self.get_url(form_id)
        data = self.con.get(url, params=params, **kwargs)
        return xmatters.objects.forms.Form(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class GroupsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(GroupsEndpoint, self).__init__(parent, '/groups')

    def get_groups(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Group) if data.get('data') else []

    def get_group_by_id(self, group_id, params=None, **kwargs):
        url = self.get_url(group_id)
        data = self.con.get(url, params=params, **kwargs)
        return Group(self, data) if data else None

    def get_license_quotas(self):
        url = self.get_url('/license-quotas')
        data = self.con.get(url)
        return GroupQuota(data) if data else None

    def create_group(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    def update_group(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    def delete_group(self, group_id):
        url = self.get_url(group_id)
        data = self.con.delete(url)
        return Group(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ImportsEndpoint(ApiBridge):
    def __init__(self, parent):
        super(ImportsEndpoint, self).__init__(parent, '/imports')

    def get_import_jobs(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs).get('data', {})
        return [Import(self, job) for job in data] if data else []

    def get_import_job_by_id(self, import_id, params=None, **kwargs):
        url = self.get_url(import_id)
        data = self.con.get(url, params=params, **kwargs)
        return Import(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(IncidentsEndpoint, self).__init__(parent, '/incidents')

    def get_incidents(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Incident) if data.get('data') else []

    def get_incident_by_id(self, incident_id, params=None, **kwargs):
        url = self.get_url(incident_id)
        data = self.con.get(url, params=params, **kwargs)
        return Incident(self, data) if data else None

    def update_incident(self, incident_id, data):
        url = self.get_url(incident_id)
        data = self.con.post(url, data=data)
        return Incident(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallEndpoint(ApiBridge):

    def __init__(self, parent):
        super(OnCallEndpoint, self).__init__(parent, '/on-call')

    def get_oncall(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, OnCall) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallSummaryEndpoint(ApiBridge):

    def __init__(self, parent):
        super(OnCallSummaryEndpoint, self).__init__(parent, '/on-call-summary')

    def get_oncall_summary(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return [OnCallSummary(self, summary) for summary in data] if data else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PeopleEndpoint(ApiBridge):

    def __init__(self, parent):
        super(PeopleEndpoint, self).__init__(parent, '/people')

    def get_people(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Person) if data.get('data') else []

    def get_person_by_id(self, person_id, params=None, **kwargs):
        url = self.get_url(person_id)
        data = self.con.get(url, params=params, **kwargs)
        return Person(self, data) if data else None

    def get_people_by_query(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Person) if data.get('data') else []

    def get_license_quotas(self):
        url = self.get_url('license-quotas')
        data = self.con.get(url)
        return UserQuota(data) if data else None

    def create_person(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    def update_person(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    def delete_person(self, person_id):
        url = self.get_url(person_id)
        data = self.con.delete(url)
        return Person(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PlansEndpoint(ApiBridge):

    def __init__(self, parent):
        super(PlansEndpoint, self).__init__(parent, '/plans')

    def get_plans(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Plan) if data.get('data') else []

    def get_plan_by_id(self, plan_id, params=None, **kwargs):
        url = self.get_url(plan_id)
        data = self.con.get(url, params=params, **kwargs)
        return Plan(self, data) if data else None

    def create_plan(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    def update_plan(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    def delete_plan(self, plan_id):
        url = self.get_url(plan_id)
        data = self.con.delete(url)
        return Plan(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RolesEndpoint(ApiBridge):

    def __init__(self, parent):
        super(RolesEndpoint, self).__init__(parent, '/roles')

    def get_roles(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Role) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenariosEndpoint(ApiBridge):

    def __init__(self, parent):
        super(ScenariosEndpoint, self).__init__(parent, '/scenarios')

    def get_scenarios(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Scenario) if data.get('data') else []

    def get_scenario_by_id(self, scenario_id, params=None, **kwargs):
        url = self.get_url(scenario_id)
        data = self.con.get(url, params=params, **kwargs)
        return Scenario(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ServicesEndpoint(ApiBridge):

    def __init__(self, parent):
        super(ServicesEndpoint, self).__init__(parent, '/services')

    def get_services(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Service) if data.get('data') else []

    def get_service_by_id(self, service_id, params=None, **kwargs):
        url = self.get_url(service_id)
        data = self.con.get(url, params=params, **kwargs)
        return Service(self, data) if data else None

    def create_service(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    def update_service(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    def delete_service(self, service_id):
        url = self.get_url(service_id)
        data = self.con.delete(url)
        return Service(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SitesEndpoint(ApiBridge):

    def __init__(self, parent):
        super(SitesEndpoint, self).__init__(parent, '/sites')

    def get_sites(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Site) if data.get('data') else []

    def get_site_by_id(self, site_id, params=None, **kwargs):
        url = self.get_url(site_id)
        data = self.con.get(url, params=params, **kwargs)
        return Site(self, data) if data else None

    def create_site(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    def update_site(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    def delete_site(self, site_id):
        url = self.get_url(site_id)
        data = self.con.delete(url)
        return Site(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(SubscriptionsEndpoint, self).__init__(parent, '/subscriptions')

    def get_subscriptions(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Subscription) if data else []

    def get_subscription_by_id(self, subscription_id, params=None, **kwargs):
        url = self.get_url(subscription_id)
        data = self.con.get(url, params=params, **kwargs)
        return SubscriptionForm(self, data) if data else None

    def get_subscribers(self, params=None, **kwargs):
        url = self.get_url('/subscribers')
        subscribers = self.con.get(url, params=params, **kwargs)
        return Pagination(self, subscribers, Person) if subscribers.get('data') else []

    def unsubscribe_person(self, person_id):
        url = self.get_url('/subscribers/{}'.format(person_id))
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

    def create_subscription(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    def update_subscription(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    def delete_subscription(self, subscription_id):
        url = self.get_url(subscription_id)
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormsEndpoint(ApiBridge):

    def __init__(self, parent):
        super(SubscriptionFormsEndpoint, self).__init__(parent, '/subscription-forms')

    def get_subscription_forms(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, SubscriptionForm) if data.get('data') else []

    def get_subscription_form_by_id(self, sub_form_id, params=None, **kwargs):
        url = self.get_url(sub_form_id)
        data = self.con.get(url, params=params, **kwargs)
        return SubscriptionForm(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class TemporaryAbsencesEndpoint(ApiBridge):

    def __init__(self, parent):
        super(TemporaryAbsencesEndpoint, self).__init__(parent, '/temporary-absences')

    def get_temporary_absences(self, params=None, **kwargs):
        url = self.get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, TemporaryAbsence) if data.get('data') else []

    def create_temporary_absence(self, data):
        url = self.get_url()
        data = self.con.post(url, data=data)
        return TemporaryAbsence(self, data) if data else None

    def delete_temporary_absence(self, temporary_absence_id):
        url = self.get_url(temporary_absence_id)
        data = self.con.delete(url)
        return TemporaryAbsence(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

# class UploadUsersEndpoint(ApiBridge):
#     _endpoints = {'upload_user_upload_file': '/uploads/users-v1',
#                   'upload_epic_zipsync_file': '/uploads/epic-v1'}
#
#     def __init__(self, parent):
#         super(UploadUsersEndpoint, self).__init__(parent)
#
#     def upload_user_upload_file(self, file_path):
#         pass
#
#     def upload_epic_zipsync_file(self, file_path):
#         pass
#
#     def __repr__(self):
#         return '<{}>'.format(self.__class__.__name__)
#
#     def __str__(self):
#         return self.__repr__()
