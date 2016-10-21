import uuid
from google.appengine.ext import ndb


class Intent(ndb.Model):
    requestType = ndb.StringProperty(default='IntentRequest')
    type = ndb.StringProperty()
    term = ndb.StringProperty()

    message = ndb.StringProperty()
    # event timestamp
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    def _pre_put_hook(self):
        if not self.key.id():
            self.key = ndb.Key(Intent, unicode(uuid.uuid4()))

    def getAnswer(self, info):
        slots = info['request']['intent']['slots']
        fields = {key: value['value'] for key, value in slots.iteritems()}
        return self.message.format(**fields)
