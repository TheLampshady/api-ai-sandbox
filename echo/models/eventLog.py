import uuid
from google.appengine.ext import ndb


class EventLog(ndb.Model):
    request = ndb.JsonProperty()
    response = ndb.JsonProperty()
    # event timestamp
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    def _pre_put_hook(self):
        if not self.key.id():
            self.key = ndb.Key(EventLog, unicode(uuid.uuid4()))

    @classmethod
    @ndb.tasklet
    def new(cls, request):
        el = EventLog(request=request)
        yield el.put_async()
        raise ndb.Return(el)

    @ndb.tasklet
    def close(self, response):
        self.response = response
        yield self.put_async()
