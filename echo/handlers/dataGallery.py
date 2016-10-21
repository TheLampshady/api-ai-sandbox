from base import BaseEchoSecurityHandler
from echo.models.intent import Intent


class DataGalleryHandler(BaseEchoSecurityHandler):

    def post(self):
        message = 'Sorry, if millennials do not know about this it cannot be a thing.'
        request_type = self.info['request']['type']

        if request_type == 'LaunchRequest':
            message = 'Hello huge! Bow to your new master!'
        else:
            intentStr = self.info['request']['intent']['name']

            if intentStr == 'WhoIs':
                field = self.info['request']['intent']['slots']['name']['value'].lower()
            elif intentStr == 'SearchFor':
                field = self.info['request']['intent']['slots']['search']['value'].lower()
            elif intentStr == 'Seinfeld':
                field = self.info['request']['intent']['slots']['search']['value'].lower()

            intent = Intent.query(
                Intent.requestType == request_type,
                Intent.type == intentStr,
                Intent.term == field,
            ).get()

            if intent:
                message = intent.getAnswer(self.info)

        response = {
            "version": "1.0",
            # "sessionAttributes": {
            #     "supportedHoriscopePeriods": {
            #         "daily"  : True,
            #         "weekly" : False,
            #         "monthly": False
            #     }
            # },
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
