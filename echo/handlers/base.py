import datetime
import json
import logging
import posixpath
import urlparse
import webapp2
from echo.models.eventLog import EventLog
from webapp2_extras import jinja2

log = logging.getLogger(__name__)


class BaseEchoSecurityHandler(webapp2.RequestHandler):
    """
    base class covering all the security checks for an amazon echo action
    """

    def __init__(self, *args, **kwargs):
        super(BaseEchoSecurityHandler, self).__init__(*args, **kwargs)

        if self.request.method == 'GET':
            return

        url = urlparse.urlparse(self.request.headers.get('SignatureCertChainUrl', ''))
        scheme = url.scheme
        hostname = url.netloc
        path = posixpath.normpath(url.path)
        self.eventLog = EventLog.new(self.request.body, method=self.request.method).get_result()
        self.info = info = json.loads(self.request.body)

        # verify high level stuff about the request header cert URL
        if scheme != 'https':
            self.abort(400)
        elif hostname != 's3.amazonaws.com':
            self.abort(400)
        elif not path.startswith('/echo.api/'):
            self.abort(400)

        # verify the request was within 150 seconds of now
        now = datetime.datetime.utcnow()
        timestamp = datetime.datetime.strptime(info['request']['timestamp'], '%Y-%m-%dT%H:%M:%SZ')

        if (now - timestamp).seconds >= 150:
            self.abort(400)

        log.info(self.request)

    def abort(self, code, *args, **kwargs):
        log.error(self.request)
        super(BaseEchoSecurityHandler, self).abort(code, *args, **kwargs)

    def answer(self, response):
        msg = json.dumps(response)
        self.response.write(msg)
        self.eventLog.close(response=msg).get_result()


class BaseEchoHandler(webapp2.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseEchoHandler, self).__init__(*args, **kwargs)
        self.context = {
            'urlFor': self.urlFor
        }

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render(self, template):
        self.response.write(self.jinja2.render_template(template, **self.context))

    def urlFor(self, name, **kwargs):
        """
        get url by name
        :param name: name of URL
        :return: url
        """
        return webapp2.uri_for(name, self, **kwargs)
