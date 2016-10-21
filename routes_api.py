import endpoints
from cerebro.search_api import SearchApi


APPLICATION = endpoints.api_server([
    SearchApi,
])
