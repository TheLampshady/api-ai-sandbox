import endpoints, logging
from protorpc import messages, remote
from cerebro import NUGGET_TYPE, ARTICLE_TYPE, CARD_TYPES, DEFAULT_LOCALE
from cerebro import search_client

log = logging.getLogger(__name__)

package = 'DataGallery'

CONTENT_TYPES = [NUGGET_TYPE, ARTICLE_TYPE]
DONUT_CART = "donut_chart"
RATIO = "ratio"
QUOTE = 'quote'
VARIATION = 'variation'
PLAIN_TEXT = 'plain_text'
TRENDING = 'trending'


class JsonField(messages.StringField):
    type = dict


class ListField(messages.StringField):
    type = list


class QueryTwG(messages.Message):
    query = messages.StringField(1)
    content_type = messages.StringField(2)
    locale = messages.StringField(3, default=DEFAULT_LOCALE)
    sort = messages.StringField(4)


class SearchResult(messages.Message):
    text = ListField(1)
    key_words = ListField(2)


SEARCH_RESOURCE = endpoints.ResourceContainer(
    query=messages.StringField(1, variant=messages.Variant.STRING),
    locale=messages.StringField(2, variant=messages.Variant.STRING, default=DEFAULT_LOCALE),
    content_type=messages.StringField(3, variant=messages.Variant.STRING, default=NUGGET_TYPE),
    sort=messages.StringField(4, variant=messages.Variant.STRING)
)
KEYWORD_RESOURCE = endpoints.ResourceContainer(
    locale=messages.StringField(1, variant=messages.Variant.STRING, default=DEFAULT_LOCALE)
)


@endpoints.api(
    name='twg_api',
    canonical_name='TwG API',
    version='v1',
    description="For Searching Think with Google.",
)
class SearchApi(remote.Service):
    @endpoints.method(SEARCH_RESOURCE, SearchResult,
                      http_method='GET', path='query', name='query')
    def query(self, request):
        content_type = (request.content_type or "").lower()

        if content_type not in CONTENT_TYPES:
            endpoints.BadRequestException("Invalid Content Type: Options [%s]" % CONTENT_TYPES)

        params = dict(query=request.query, locale=request.locale, count=False)
        if content_type:
            params['source_type'] = content_type

        params['sort_field'] = "relevance" if not request.sort else request.sort

        result = search_client.search(**params)
        text_list = self.format_text_results(result.get("search_response", []))

        return SearchResult(
            text=text_list,
            key_words=reduce(lambda x, y: x+y, result.get("facets_info").values())
        )

    @endpoints.method(KEYWORD_RESOURCE, SearchResult, http_method='GET', path='keyword', name='keyword')
    def get_facets(self, request):

        result = search_client.get_facets(request.locale)

        return SearchResult(
            key_words=reduce(lambda x,y: x+y, result.get("facets_info").values())
        )

    @staticmethod
    def format_text_results(entries):
        result = []
        for entry in entries:
            text = None
            if entry.get("source_type") == NUGGET_TYPE:
                card_type = entry.get("card_type")
                if card_type == DONUT_CART:
                    text = "%s percent %s" % (entry.get("percentage"), entry.get("body"))
                elif card_type == RATIO:
                    text = "%s of %s %s" % (entry.get("feature_text"), entry.get("feature_text_alt"), entry.get("body"))
                elif card_type == TRENDING:
                     text = "%s precent %s" % (entry.get("feature_text"), entry.get("body"))
                elif card_type == PLAIN_TEXT:
                    text = entry.get("body")

            else:
                if entry.get("title"):
                    text = entry.get("title")

            if text:
                    result.append(text)
        return result