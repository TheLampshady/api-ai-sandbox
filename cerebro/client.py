import logging
from googleapiclient.discovery import build

CEREBRO_ROOT = "https://gthink-dmx-dev.appspot.com"


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
