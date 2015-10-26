import json
import logging
import webapp2
from echo.handlers import BaseEchoSecurityHandler

log = logging.getLogger(__name__)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('Echo Main Page! Test')


class HelloWorldHandler(BaseEchoSecurityHandler):

    def post(self):
        request_type = self.info['request']['type']

        if request_type == 'LaunchRequest':
            message = ''
        elif request_type == 'IntentRequest':
            intent = self.info['request']['intent']['name']
            if intent == 'WhoIs':
                name = self.info['request']['intent']['slots']['name']['value']

                if name.lower() == 'ryan':
                    message = 'Who? You mean Ryan? Fuck that guy.'
                elif name.lower() == 'levi':
                    message = 'A level 9 Jew.'
                else:
                    message = 'Sorry, do not know that name.'
            else:
                message = 'Sorry, do not understand that command.'

        response = {
          "version": "1.0",
          "sessionAttributes": {
            "supportedHoriscopePeriods": {
              "daily": True,
              "weekly": False,
              "monthly": False
            }
          },
          "response": {
            "outputSpeech": {
              "type": "PlainText",
              "text": message
            },
            "card": {
              "type": "Simple",
              "title": "Horoscope",
              "content": message
            },
            # "reprompt": {
            #   "outputSpeech": {
            #     "type": "PlainText",
            #     "text": "Can I help you with anything else?"
            #   }
            # },
            "shouldEndSession": True
          }
        }
        self.response.write(json.dumps(response))


_APP = webapp2.WSGIApplication([
    webapp2.Route('/echo', handler=MainHandler, name='echo-home'),
    webapp2.Route('/echo/hello-world', handler=HelloWorldHandler, name='echo-hello-world'),
], debug=True)
