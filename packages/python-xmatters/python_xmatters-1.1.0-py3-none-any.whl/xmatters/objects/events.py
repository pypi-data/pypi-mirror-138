import xmatters.factories
import xmatters.utils as util
import xmatters.objects.forms as forms
from xmatters.connection import ApiBridge
from xmatters.objects.common import Recipient, Pagination, SelfLink
from xmatters.objects.event_supressions import EventSuppression
from xmatters.objects.people import PersonReference
from xmatters.objects.plans import PlanReference


class Message(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.message_type = data.get('messageType')
        self.subject = data.get('subject')
        self.body = data.get('body')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.subject)

    def __str__(self):
        return self.__repr__()


class UserDeliveryResponse(object):
    def __init__(self, data):
        self.text = data.get('text')
        self.notification = data.get('notification')
        received = data.get('received')
        self.received = util.TimeAttribute(received) if received else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Conference(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.bridge_id = data.get('bridgeId')
        self.bridge_number = data.get('bridgeNumber')
        self.type = data.get('type')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class VoicemailOptions(object):
    def __init__(self, data):
        self.retry = data.get('retry')
        self.every = data.get('every')
        self.leave = data.get('leave')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Translation(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.language = data.get('language')
        self.text = data.get('text')
        self.prompt = data.get('prompt')
        self.description = data.get('description')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ResponseOption(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.number = data.get('number')
        self.text = data.get('text')
        self.description = data.get('description')
        self.prompt = data.get('prompt')
        self.action = data.get('action')
        self.contribution = data.get('contribution')
        self.join_conference = data.get('joinConference')
        self.allow_comments = data.get('allowComments')
        self.redirect_rul = data.get('redirectUrl')
        translations = data.get('translations', {}).get('data', [])
        self.translations = [Translation(t) for t in translations]

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferencePointer(object):
    def __init__(self, data):
        self.bridge_id = data.get('bridgeId')
        self.type = data.get('type')
        self.bridge_number = data.get('bridgeNumber')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventReference(ApiBridge):
    def __init__(self, parent, data):
        super(EventReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.event_id = data.get('eventId')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Notification(ApiBridge):
    def __init__(self, parent, data):
        super(Notification, self).__init__(parent, data)
        self.id = data.get('id')
        self.recipient = Recipient(self, data.get('recipient'))
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None
        delivered = data.get('delivered')
        self.delivered = util.TimeAttribute(delivered) if delivered else None
        responded = data.get('responded')
        self.responded = util.TimeAttribute(responded) if responded else None
        self.delivery_status = data.get('deliveryStatus')
        responses = data.get('responses')
        self.responses = [UserDeliveryResponse(r) for r in responses] if responses.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.recipient.target_name)

    def __str__(self):
        return self.__repr__()


class UserDeliveryData(ApiBridge):
    def __init__(self, parent, data):
        super(UserDeliveryData, self).__init__(parent, data)
        event = data.get('event')
        self.event = EventReference(self, event) if event else None
        person = data.get('person')
        self.person = PersonReference(self, person) if person else None
        self.delivery_status = data.get('deliveryStatus')
        notifications = data.get('notifications', {}).get('data')
        self.notifications = [Notification(self, n) for n in notifications] if notifications else []
        response = data.get('response')
        self.response = UserDeliveryResponse(response) if response else None
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.person.target_name)

    def __str__(self):
        return self.__repr__()


class Annotation(ApiBridge):
    def __init__(self, parent, data):
        super(Annotation, self).__init__(parent, data)
        self.id = data.get('id')
        event = data.get('event')
        self.event = EventReference(self, event)
        author = data.get('author')
        self.author = PersonReference(self, author)
        self.comment = data.get('comment')
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Event(ApiBridge):
    _endpoints = {'messages': '?embed=messages',
                  'get_annotations': '/annotations',
                  'get_annotation_by_id': '/annotations/{ann_id}',
                  'properties': '?embed=properties',
                  'recipients': '?embed=recipients',
                  'response_options': '?embed=responseOptions&responseOptions.translations',
                  'get_user_delivery_data': '/user-deliveries',
                  'get_audits': '{base_url}/audits',
                  'update_status': '{base_url}/events',
                  'targeted_recipients': '?embed=recipients&targeted=true',
                  'get_suppressions': '{base_url}/event-suppressions'}

    def __init__(self, parent, data):
        super(Event, self).__init__(parent, data)
        self.bypass_phone_intro = data.get('bypassPhoneIntro')
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None
        conference = data.get('conference')
        self.conference = Conference(conference) if conference else None
        self.escalation_override = data.get('escalationOverride')
        self.event_id = data.get('eventId')
        self.event_type = data.get('eventType')
        self.expiration_in_minutes = data.get('expirationInMinutes')
        self.flood_control = data.get('floodControl')
        plan = data.get('plan')
        self.plan = PlanReference(plan) if plan else None
        form = data.get('form')
        self.form = forms.FormReference(form) if form else None
        self.id = data.get('id')
        self.incident = data.get('incident')
        self.override_device_restrictions = data.get('overrideDeviceRestrictions')
        self.other_response_count = data.get('otherResponseCount')
        self.other_response_count_threshold = data.get('otherResponseCountThreshold')
        self.priority = data.get('priority')
        self.require_phone_password = data.get('requirePhonePassword')
        self.response_count_enabled = data.get('responseCountsEnabled')
        submitter = data.get('submitter')
        self.submitter = PersonReference(self, submitter) if submitter else None
        self.status = data.get('status')
        terminated = data.get('terminated')
        self.terminated = util.TimeAttribute(terminated) if terminated else None
        voicemail_options = data.get('voicemailOptions')
        self.voicemail_options = VoicemailOptions(voicemail_options) if voicemail_options else None
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def annotations(self):
        return self.get_annotations()

    @property
    def messages(self):
        return self.get_messages()

    @property
    def properties(self):
        return self.get_properties()

    @property
    def recipients(self):
        return self.get_recipients()

    @property
    def response_options(self):
        return self.get_response_options()

    @property
    def suppressions(self):
        return self.get_suppressions()

    @property
    def targeted_recipients(self):
        return self.get_targeted_recipients()

    def get_recipients(self):
        url = self.get_url(self._endpoints.get('recipients'))
        data = self.con.get(url)
        recipients = data.get('recipients')
        return Pagination(self, recipients, Message) if recipients.get('data') else []

    def get_response_options(self):
        url = self.get_url(self._endpoints.get('response_options'))
        data = self.con.get(url)
        response_options = data.get('responseOptions', {}).get('data')
        return [ResponseOption(r) for r in response_options] if response_options else []

    def get_targeted_recipients(self):
        url = self.get_url(self._endpoints.get('targeted_recipients'))
        data = self.con.get(url)
        recipients = data.get('recipients')
        return Pagination(self, recipients, Message) if recipients.get('data') else []

    def get_properties(self):
        url = self.get_url(self._endpoints.get('properties'))
        data = self.con.get(url)
        return data.get('properties', {})

    def get_messages(self):
        url = self.get_url(self._endpoints.get('messages'))
        data = self.con.get(url)
        messages = data.get('messages')
        return Pagination(self, messages, Message) if messages.get('data') else []

    def get_audits(self, params=None, **kwargs):
        url = self._endpoints.get('get_audits').format(base_url=self.con.api_base_url)
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, xmatters.factories.AuditFactory) if data.get('data') else []

    def get_user_delivery_data(self, params=None, **kwargs):
        url = self.get_url(self._endpoints.get('get_user_delivery_data'))
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, UserDeliveryData) if data.get('data') else []

    def get_annotations(self, params=None, **kwargs):
        url = self.get_url(self._endpoints.get('get_annotations'))
        data = self.con.get(url, params=params, **kwargs)
        annotations = data.get('annotations', {})
        return Pagination(self, annotations, Annotation) if annotations.get('data') else []

    def get_annotation_by_id(self, annotation_id):
        url = self.get_url(self._endpoints.get('get_annotation_by_id').format(ann_id=annotation_id))
        data = self.con.get(url)
        return Annotation(self, data) if data else None

    def add_annotation(self, comment):
        data = {'comment': comment}
        url = self.get_url(self._endpoints.get('get_annotations'))
        data = self.con.post(url, data=data)
        return Annotation(self, data) if data else None

    def update_status(self, status):
        data = {'id': self.id,
                'status': status}

        url = self._endpoints.get('update_status').format(base_url=self.con.api_base_url)
        data = self.con.post(url, data=data)
        return Event(self, data) if data else None

    def get_suppressions(self, params=None, **kwargs):
        url = self._endpoints.get('get_suppressions').format(base_url=self.con.api_base_url)
        suppressions = self.con.get(url, params=params, **kwargs)
        return Pagination(self, suppressions, EventSuppression) if suppressions.get('data') else []

    def __repr__(self):
        return '<{} Created: {} Type: {}>'.format(self.__class__.__name__, self.created, self.event_type)

    def __str__(self):
        return self.__repr__()
