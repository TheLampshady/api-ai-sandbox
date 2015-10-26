import datetime
import json
import logging
import posixpath
import urlparse
import webapp2

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
