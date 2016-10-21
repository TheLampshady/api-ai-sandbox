import json
import random
import urllib


def mine_data(data):
    nuggets = data.get('text')
    urls = data.get('urls')

    rand_index = random.randint(0, len(nuggets))

    return nuggets[rand_index], urls[rand_index]


def handle_filter(criterion):
    print('filtering by criterion: %s' % criterion)


def handle_find(query):
    base_url = 'https://huge-echo.appspot.com/_ah/api/twg_api/v1/query?query='
    twg_query = base_url + query
    res = urllib.request.urlopen(twg_query).read()

    return json.loads(str(res, 'utf-8'))


def handle_download(context):
    pass


def handle_show():
    pass
