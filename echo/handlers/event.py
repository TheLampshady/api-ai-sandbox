import json
from base import BaseEchoHandler
from echo.models.eventLog import EventLog
from google.appengine.ext import ndb


class EventIndexHandler(BaseEchoHandler):

    def get(self):
        eventLogs = EventLog.query().order(-EventLog.created).fetch(20)
        self.context['eventLogs'] = eventLogs
        self.render('eventIndex.html')


class EventDetailHandler(BaseEchoHandler):

    def get(self, eventId):
        self.context['json'] = json
        eventLog = ndb.Key(EventLog, eventId).get()
        self.context['eventLog'] = eventLog
        self.render('eventDetail.html')
