from base import BaseEchoSecurityHandler


class DataGalleryHandler(BaseEchoSecurityHandler):

    def post(self):
        message = 'No matching pattern.'
        request_type = self.info['request']['type']

        if request_type == 'LaunchRequest':
            message = 'Hello huge! Bow to your new master!'
        elif request_type == 'IntentRequest':
            intent = self.info['request']['intent']['name']
            if intent == 'WhoIs':
                name = self.info['request']['intent']['slots']['name']['value'].lower()

                if name == 'ryan':
                    message = 'I am ready to kill the humans.'
                else:
                    message = 'Sorry, do not know who {name} is.'.format(name=name.capitalize())
            else:
                message = 'Sorry, do not understand that command.'

        response = {
            "version"          : "1.0",
            "sessionAttributes": {
                "supportedHoriscopePeriods": {
                    "daily"  : True,
                    "weekly" : False,
                    "monthly": False
                }
            },
            "response"         : {
                "outputSpeech"    : {
                    "type": "PlainText",
                    "text": message
                },
                "card"            : {
                    "type"   : "Simple",
                    "title"  : "Horoscope",
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
        self.answer(response)
