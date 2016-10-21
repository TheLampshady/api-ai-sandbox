import os
import webapp2
from webapp2_extras import jinja2
from google.appengine.api import app_identity

SERVER_SOFTWARE = os.environ.get('SERVER_SOFTWARE', 'Unknown')
VERSION = os.environ.get('CURRENT_VERSION_ID', 'dev').split('.')[0]
MODULE = os.environ.get('CURRENT_MODULE_ID', 'default')


class BaseHandler(webapp2.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.context = {}

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render(self, template):
        self.response.write(self.jinja2.render_template(template, **self.context))


class MainHandler(BaseHandler):

    def get(self):
        self.response.write('Huge Echo Main Page!')


class AdminHandler(BaseHandler):

    def get(self):
        self.context['api_explorer'] = \
            "https://apis-explorer.appspot.com/apis-explorer/?base=%s/_ah/api#p/" % \
            (self.host_url if self.host_url else self.request.host_url)

        self.render('admin.html')

    @property
    def host_url(self):
        """
        Gets the current host url or empty if local.
        :return: dict of variables
        """
        return '' if SERVER_SOFTWARE.startswith('Dev') else \
            "https://%s-dot-%s-dot-%s.appspot.com" % \
            (VERSION, MODULE, app_identity.get_application_id())

application = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route('/admin', handler=AdminHandler, name='admin'),
], debug=True)
