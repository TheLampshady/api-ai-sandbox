import webapp2
from handlers.event import EventIndexHandler


routes = [
    webapp2.Route('/echo/admin', handler=EventIndexHandler, name='echo-event-index'),
]


application = webapp2.WSGIApplication(routes, debug=False)
