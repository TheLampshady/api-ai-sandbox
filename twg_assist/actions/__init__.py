import json
import random
import logging

from cerebro import search_client
from cerebro.search_api import SearchApi
from cerebro import DEFAULT_LOCALE, NUGGET_TYPE


DOWNLOAD_CONTEXT = "nugget"

def mine_data(data):
    nuggets = data.get('text')
    urls = data.get('urls')

    if nuggets and urls:
        rand_index = random.randint(0, len(nuggets-1))

        return nuggets[rand_index], urls[rand_index]

    return [], []


def handle_filter(criterion):
    print('filtering by criterion: %s' % criterion)


def locale_query(query, source_type=NUGGET_TYPE):
    params = dict(
        sort_field="relevance",
        source_type=source_type,
        locale=DEFAULT_LOCALE,
        count=False,
        limit=40,
        query=query
    )

    result = search_client.search_url(**params)
    text_list, url_list = SearchApi.format_text_results(result.get("search_response", []))
    return dict(text=text_list, urls=url_list)


def handle_find(result):
    query = result.get("parameters").get("any")
    # query = urllib.urlencode(dict(query=query))
    # base_url = 'https://huge-echo.appspot.com/_ah/api/twg_api/v1/query?'
    # twg_query = base_url + query
    # logging.info("Calling: %s" % twg_query)
    # res = urlfetch.fetch(twg_query)
    #
    # data = json.loads(res.content)

    data = locale_query(query)
    nugget_text, nugget_url = mine_data(data)

    return {
        'speech': nugget_text,
        'displayText': nugget_text,
        'data': {
            'slack': nugget_text
        },
        'contextOut': [
            {
                'name': 'nugget',
                'lifespan': 5,
                'parameters': {
                    'nugget_text': nugget_text,
                    'nugget_url': nugget_url
                }
            }
        ],
        "source": 'twg-webhook-processor'
    }


def handle_download(result):
    nugget_url = ""
    for context in result.get("contexts", []):
        if context.get("name", "") == DOWNLOAD_CONTEXT:
            nugget_url = context.get("parameters", {}).get("nugget_url")
            logging.info("Download Link Found: %s" % nugget_url)
            break

    share_url = nugget_url.replace("/detail/", "/share/")

    return {
        'speech': share_url,
        'displayText': 1,
        'data': {
            'slack': 1
        },
        "source": 'twg-webhook-processor'
    }
