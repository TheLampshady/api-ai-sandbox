import webapp2
import json
import os
import logging

from twg_assist.actions import mine_data, handle_find, handle_filter, handle_download, handle_show


log = logging.getLogger(__name__)


supported_actions = {
    '.find': handle_find,
    '.filter': handle_filter,
    '.download': handle_download,
    '.show': handle_show
}


class APIAIHandler(webapp2.RequestHandler):

    def post(self):
        content = json.loads(self.request.body)
        result = content.get("result")
        action = supported_actions.get(result.get('action'))

        data = action(result)
        nugget_text, nugget_url = mine_data(data)

        res = curate_webhook_response(nugget_text, nugget_url)

        res = json.dumps(res, indent=4)
        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(json.dumps(res))


def process_request(request):
    action = supported_actions.get(request.get('action'))

    data = action(request)
    nugget_text, nugget_url = mine_data(data)

    return curate_webhook_response(nugget_text, nugget_url)


def curate_webhook_response(nugget_text, nugget_url):
    payload = {
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

    log.info('Payload: %s' % json.dumps(payload, indent=4))
    return payload
