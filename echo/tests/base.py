import os, sys, unittest, logging
from google.appengine.ext import testbed, ndb

os.environ.setdefault('APPLICATION_ID', 'localhost')
os.environ.setdefault('CURRENT_VERSION_ID', 'localhost.dev')
os.environ.setdefault('ENDPOINTS_AUTH_EMAIL', '')
os.environ.setdefault('ENDPOINTS_AUTH_DOMAIN', '')
path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../../libs')
sys.path.insert(0, path)

logging.basicConfig()


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        ### declare services we will be testing
        self.testbed.init_app_identity_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_logservice_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

        ndb.get_context().clear_cache()
        self.email = 'test@example.com'

    def tearDown(self):
        self.testbed.deactivate()

    def login(self):
        os.environ['ENDPOINTS_AUTH_EMAIL'] = self.email
