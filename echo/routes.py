import json
import webapp2
from echo.models.eventLog import EventLog
from handlers.default import DefaultsHandler
from handlers.event import EventIndexHandler, EventDetailHandler
from handlers.intent import IntentIndexHandler, IntentDetailHandler


config = {'webapp2_extras.jinja2': {
    'template_path': 'echo/templates',
    'environment_args': {
        'autoescape': True,
        'extensions': [
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
            # 'jinja2.ext.i18n',
        ]
    }
    }
}


class DummyEventGenerateHandler(webapp2.RequestHandler):

    def get(self):
        request = json.dumps({'yay': 'request'})
        response = json.dumps({'yay': 'response'})
        el = EventLog.new(request, method='GET').get_result()
        el.close(response).get_result()
        self.response.write('done.')


routes = [
    webapp2.Route('/echo/admin', handler=EventIndexHandler, name='echo-event-index'),
    webapp2.Route('/echo/admin/default-intents', handler=DefaultsHandler),
    webapp2.Route('/echo/admin/dummy-event', handler=DummyEventGenerateHandler),
    webapp2.Route('/echo/admin/event/detail/<eventId:([A-Za-z0-9-]+)>',
                  handler=EventDetailHandler, name='echo-event-detail'),
    webapp2.Route('/echo/admin/intents',
                  handler=IntentIndexHandler, name='echo-intents'),
    webapp2.Route('/echo/admin/intent/<id:([A-Za-z0-9-]+)>',
                  handler=IntentDetailHandler, name='echo-intent'),
]


application = webapp2.WSGIApplication(routes, debug=False, config=config)
