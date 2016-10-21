import logging
import json
from googleapiclient.discovery import build
from google.appengine.api import urlfetch

CEREBRO_ROOT = "https://cerebro-dot-gthink-dmx-dev.appspot.com"


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
            cache_discovery=False
        )

    @property
    def client(self):
        if self._client is None:
            logging.info("Loading Discovery URL.")
            self.reset_service()
        return self._client

    @classmethod
    def get_discovery_url(cls):
        """
        Returns a formatted discovery url
        :return:
        """
        search_root = "%s/_ah/api" % CEREBRO_ROOT
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

    @staticmethod
    def search_url(**kwargs):
        search_path = "/_ah/api/search_api/v1/search"
        url = CEREBRO_ROOT + search_path
        if kwargs:
            params = ["%s=%s" % (k,v) for k,v in kwargs.items()]
            url = "%s?%s" % (url, "&".join(params))

        result = urlfetch.fetch(url)
        return json.loads(result.content)

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
