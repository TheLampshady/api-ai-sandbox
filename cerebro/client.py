import httplib2, json, endpoints, logging
from googleapiclient.discovery import build
from oauth2client.contrib.appengine import AppAssertionCredentials
from google.appengine.api import memcache
from google.appengine.ext import ndb
from settings import settings


class SearchClient(object):
    _client = None
    TIMEOUT_DEADLINE = 30
    api = 'search_api'
    version = 'v1'
    discovery_url = '{root}/discovery/{v}/apis/{api}/{v}/rest'

    def reset_service(self):
        self._client = build(
            self.api, self.version,
            discoveryServiceUrl=self.get_discovery_url(),
            http=self.get_credentials(),
            cache_discovery=False
        )

    @property
    def client(self):
        if self._client is None:
            logging.info("Loading Discovery URL.")
            self.reset_service()
        return self._client

    @staticmethod
    def get_credentials():
        """
        fetch oAuth2 credentials for communication with cerebro
        :return: http object
        """
        credentials = AppAssertionCredentials(endpoints.EMAIL_SCOPE)
        http = credentials.authorize(httplib2.Http(memcache))
        return http

    @classmethod
    def get_discovery_url(cls):
        """
        Returns a formatted discovery url
        :return:
        """
        search_root = "%s/_ah/api" % settings.CEREBRO_ROOT
        return cls.discovery_url.format(root=search_root, api=cls.api, v=cls.version)

    def search(self, **kwargs):
        """
        fetch a list of cards
        :param kwargs: search arguments
        :return: response object
        """
        # service = build(api, version, discoveryServiceUrl=cls.get_discovery_url())
        try:
            return self.client.search(**kwargs).execute()
        except Exception as e:
            logging.warning(e.message)
            self.reset_service()
            return self.client.search(**kwargs).execute()

    def get_facets(self, locale):
        """
        Calls search API for facets. ON failure reloads discovery api
        :param locale:
        :return:
        """
        try:
            return self.client.facet(locale=locale).execute()
        except Exception as e:
            logging.warning(e.message)
            self.reset_service()
            return self.client.facet(locale=locale).execute()
