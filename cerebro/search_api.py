import endpoints, logging
from protorpc import messages, remote

from cerebro import NUGGET_TYPE, ARTICLE_TYPE, CARD_TYPES, DEFAULT_LOCALE

from cerebro.client import SearchClient

log = logging.getLogger(__name__)

package = 'DataGallery'

CONTENT_TYPES = [NUGGET_TYPE, ARTICLE_TYPE]

class JsonField(messages.StringField):
    type = dict


class ListField(messages.StringField):
    type = list


SEARCH_RESOURCE_CONTAINER_FIELDS = {
    'sort_field': messages.StringField(3),
    'relevance': messages.StringField(4),
    'sort_desc': messages.IntegerField(5),
    'count': messages.BooleanField(9),
    'promote': messages.BooleanField(10, default=True),
}


class QueryTwG(messages.Message):
    query = messages.StringField(1, default="")
    content_type = messages.StringField(2)
    locale = messages.StringField(3, default=DEFAULT_LOCALE)
    sort = messages.StringField(4)


class SearchResult(messages.Message):
    text = messages.StringField(1)
    key_words = ListField(8)


@endpoints.api(
    name='search_api',
    canonical_name='Search API',
    version='v1',
    description="For Searching Think with Google.",
)
class SearchApi(remote.Service):
    SEARCH_RESOURCE = endpoints.ResourceContainer(QueryTwG)
    KEYWORD_RESOURCE = endpoints.ResourceContainer(
        locale=messages.StringField(1, variant=messages.Variant.STRING, default=DEFAULT_LOCALE)
    )

    @endpoints.method(SEARCH_RESOURCE, SearchResult, http_method='GET', path='query', name='query')
    def get(self, request):
        content_type = request.content_type.lower()

        if content_type and content_type not in CONTENT_TYPES:
            endpoints.BadRequestException("Invalid Content Type: Options [%s]" % CONTENT_TYPES)

        params = dict(query=request.query, locale=request.locale)
        if content_type:
            params['source_type'] = content_type

        params['sort_field'] = "relevance" if not request.sort else request.sort

        result = SearchClient.search(**params)

        return SearchResult(
            text="Millennial Dads is all you need to know about",
            key_words=reduce(lambda x,y: x+y, result.get("facets_info"))
        )

    @endpoints.method(KEYWORD_RESOURCE, SearchResult, http_method='GET', path='keyword', name='keyword')
    def get_facets(self, request):

        result = SearchClient.get_facets(request.locale)

        return SearchResult(
            text="Facets",
            key_words=reduce(lambda x,y: x+y, result.get("facets_info"))
        )
