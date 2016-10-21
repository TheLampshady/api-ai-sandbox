from base import BaseEchoSecurityHandler
from echo.models.context import Context
from echo.models.intent import Intent
from google.appengine.ext import ndb


@ndb.tasklet
def load(requestType, intentType, intentTerm):
    intent = Intent.query(
        Intent.requestType == requestType,
        Intent.type == intentType,
        Intent.term == intentTerm,
    )
    context = Context.query()
    intent, context = yield intent.get_async(), context.get_async()
    raise ndb.Return(intent, context)


class DataGalleryHandler(BaseEchoSecurityHandler):

    def post(self):
        message = 'Sorry, if millennials do not know about this it cannot be a thing.'
        request_type = self.info['request']['type']

        if request_type == 'LaunchRequest':
            message = 'Hello huge! Bow to your new master!'
        else:
            intentStr = self.info['request']['intent']['name']
            field = None

            if intentStr == 'WhoIs':
                field = self.info['request']['intent']['slots']['name']['value'].lower()
            elif intentStr == 'SearchFor':
                field = self.info['request']['intent']['slots']['search']['value'].lower()

            intent, context = load(
                requestType=request_type,
                intentType=intentStr,
                intentTerm=field
            ).get_result()

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
