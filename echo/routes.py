import webapp2
from handlers.event import EventIndexHandler


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


routes = [
    webapp2.Route('/echo/admin', handler=EventIndexHandler, name='echo-event-index'),
]


application = webapp2.WSGIApplication(routes, debug=False, config=config)
