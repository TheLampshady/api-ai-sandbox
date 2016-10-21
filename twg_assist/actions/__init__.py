import json
import random
from google.appengine.api import urlfetch


def mine_data(data):
    nuggets = data.get('text')
    urls = data.get('urls')

    rand_index = random.randint(0, len(nuggets))

    return nuggets[rand_index], urls[rand_index]


def handle_filter(criterion):
    print('filtering by criterion: %s' % criterion)


def handle_find(result):
    query = result.get("parameters").get("any")
    base_url = 'https://huge-echo.appspot.com/_ah/api/twg_api/v1/query?query='
    twg_query = base_url + query
    res = urlfetch.fetch(twg_query)
    res.content

    data = json.loads(str(res, 'utf-8'))
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


def handle_download(context):
    pass


def handle_show():
    pass
