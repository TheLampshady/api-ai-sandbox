import json
import random
import logging

from cerebro import search_client
from cerebro.search_api import SearchApi
from cerebro import DEFAULT_LOCALE, NUGGET_TYPE, ARTICLE_TYPE


DOWNLOAD_CONTEXT = "nugget"

def mine_data(data):
    nuggets = data.get('text')
    urls = data.get('urls')

    if nuggets and urls:
        rand_index = random.randint(0, min(len(urls), len(nuggets)))

        return nuggets[rand_index], urls[rand_index]

    return "", ""


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

    return dict(text=text_list, urls=url_list) or None


def handle_find(result):
    query = result.get("parameters").get("any")
    # query = urllib.urlencode(dict(query=query))
    # base_url = 'https://huge-echo.appspot.com/_ah/api/twg_api/v1/query?'
    # twg_query = base_url + query
    # logging.info("Calling: %s" % twg_query)
    # res = urlfetch.fetch(twg_query)
    #
    # data = json.loads(res.content)
    preface = ""
    try:
        data = locale_query(query)
        if not data.get("text"):
            raise ValueError
    except Exception as e:
        data = locale_query(query, source_type=ARTICLE_TYPE)
        preface = "We have no nuggets for %s. Here\'s an editorial article: " % query

    nugget_text, nugget_url = mine_data(data)

    nugget_text = preface + nugget_text

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
            break

    share_url = nugget_url.replace("/detail/", "/share/")
    share_url = share_url.replace("/intl/en-us/", "/")
    if share_url:
        logging.info("Download Link Found: %s" % share_url)

    return {
        'speech': share_url,
        'displayText': 'I am downloading the file...',
        'data': {
            'slack': share_url
        },
        # 'contextOut': None,
        "source": 'twg-webhook-processor'
    }
