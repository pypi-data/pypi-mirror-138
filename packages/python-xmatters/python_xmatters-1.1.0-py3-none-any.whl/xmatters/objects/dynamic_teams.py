from xmatters.objects.common import Recipient, Pagination, SelfLink
from xmatters.objects.people import Person
from xmatters.objects.roles import Role
from xmatters.objects.subscriptions import SubscriptionCriteriaReference


class DynamicTeam(Recipient):

    def __init__(self, parent, data):
        super(DynamicTeam, self).__init__(parent, data)
        self.response_count = data.get('responseCount')
        self.response_count_threshold = data.get('responseCountThreshold')
        self.use_emergency_device = data.get('useEmergencyDevice')
        self.description = data.get('description')
        criteria = data.get('criteria')
        self.criteria = SubscriptionCriteriaReference(criteria) if criteria else None
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def observers(self):
        return self.get_observers()

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_members(self):
        url = self.get_url('/members')
        data = self.con.get(url)
        return Pagination(self, data, Person) if data.get('data') else None

    def get_observers(self):
        url = self.get_url('?embed=observers')
        observers = self.con.get(url).get('observers', {}).get('data')
        return [Role(role) for role in observers] if observers else []

    def get_supervisors(self):
        url = self.get_url('?embed=supervisors')
        supervisors = self.con.get(url).get('supervisors', {})
        return Pagination(self, supervisors, Person) if supervisors.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()
