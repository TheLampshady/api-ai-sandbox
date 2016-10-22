import webapp2
import json
import os
import logging

from twg_assist.actions import handle_find, handle_filter, handle_download


log = logging.getLogger(__name__)


supported_actions = {
    '.find': handle_find,
    '.filter': handle_filter,
    'download': handle_download
}


class APIAIHandler(webapp2.RequestHandler):

    def post(self):
        content = json.loads(self.request.body)
        result = content.get("result")
        action = supported_actions.get(result.get('action'))
        log.info("Action: %s" % result.get('action'))
        data = action(result)

        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(json.dumps(data))
