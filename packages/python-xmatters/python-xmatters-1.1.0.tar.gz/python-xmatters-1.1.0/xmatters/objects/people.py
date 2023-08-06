import xmatters.factories
import xmatters.utils as utils
from xmatters.objects.common import Recipient, SelfLink, Pagination, QuotaItem
from xmatters.objects.roles import Role
from xmatters.connection import ApiBridge
import xmatters.objects.groups


class Person(Recipient):

    def __init__(self, parent, data):
        super(Person, self).__init__(parent, data)
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.license_type = data.get('licenseType')
        self.language = data.get('language')
        self.timezone = data.get('timezone')
        self.web_login = data.get('webLogin')
        self.phone_login = data.get('phoneLogin')
        self.phone_pin = data.get('phonePin')
        self.properties = data.get('properties', {})
        last_login = data.get('lastLogin')
        self.last_login = utils.TimeAttribute(last_login) if last_login else None
        when_created = data.get('whenCreated')
        self.when_created = utils.TimeAttribute(when_created) if when_created else None
        when_updated = data.get('whenUpdated')
        self.when_updated = utils.TimeAttribute(when_updated) if when_updated else None
        links = data.get('links')
        self.links = SelfLink(self, data) if links else None

    @property
    def full_name(self):
        """
        Get person's full name

        :return: person's full name
        :rtype: str
        """
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def roles(self):
        return self.get_roles()

    @property
    def devices(self):
        return self.get_devices()

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_roles(self):
        url = self.get_url('?embed=roles')
        data = self.con.get(url)
        roles = data.get('roles', {})
        return Pagination(self, roles, Role) if roles.get('data') else []

    def get_supervisors(self, params=None, **kwargs):
        url = self.get_url('/supervisors')
        s = self.con.get(url, params=params, **kwargs)
        return Pagination(self, s, Person) if s.get('data') else []

    def get_devices(self, params=None, **kwargs):
        url = self.get_url('/devices')
        devices = self.con.get(url, params=params, **kwargs)
        return Pagination(self, devices, xmatters.factories.DeviceFactory) if devices.get('data') else []

    def get_groups(self, params=None, **kwargs):
        url = self.get_url('/group-memberships')
        groups = self.con.get(url, params=params, **kwargs)
        return Pagination(self, groups, xmatters.objects.groups.GroupMembership) if groups.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class PersonReference(ApiBridge):
    def __init__(self, parent, data):
        super(PersonReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()



class UserQuota(object):
    def __init__(self, data):
        self.stakeholder_users_enabled = data.get('stakeholderUsersEnabled')
        stakeholder_users = data.get('stakeholderUsers')
        self.stakeholder_users = QuotaItem(stakeholder_users) if stakeholder_users else None
        full_users = data.get('fullUsers')
        self.full_users = QuotaItem(full_users) if full_users else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
