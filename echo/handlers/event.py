from base import BaseEchoHandler
from echo.models.eventLog import EventLog


class EventIndexHandler(BaseEchoHandler):

    def get(self):
        eventLogs = EventLog.query().order(-EventLog.created).fetch(20)
        self.context['eventLogs'] = eventLogs
        self.render('eventIndex.html')
