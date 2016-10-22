import logging
from base import BaseEchoSecurityHandler
from cerebro import search_client
from cerebro.search_api import SearchApi
from echo.models.context import Context
from echo.models.intent import Intent
from google.appengine.ext import ndb
from random import randint

log = logging.getLogger(__name__)


@ndb.tasklet
def load(requestType, intentType, intentTerm):
    intent = Intent.query(
        Intent.requestType == requestType,
        Intent.type == intentType,
        Intent.term == intentTerm,
    )
    context = Context.query()
    intent, context = yield intent.get_async(), context.get_async()

    if not context:
        context = Context()
    raise ndb.Return(intent, context)


def buildResponse(message, reprompt=None):
    result = {
        "version" : "1.0",
        # "sessionAttributes": {
        #     "supportedHoriscopePeriods": {
        #         "daily"  : True,
        #         "weekly" : False,
        #         "monthly": False
        #     }
        # },
        "response": {
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

    if reprompt is not None:
        result['response']["shouldEndSession"] = False
        result['response']['reprompt'] = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt,
            }
        }

    return result


CONTINUE_LIST = ('yes', 'sure', 'please', 'yeah', 'go for it', 'shoot', 'go', 'yes please', 'more', 'again', 'another')


class DataGalleryHandler(BaseEchoSecurityHandler):

    def post(self):
        message = 'Sorry, if millennials do not know about this it cannot be a thing.'
        request_type = self.info['request']['type']
        newSession = self.info['session']['new']
        searchResult = None
        field = None
        intentStr = None
        reprompt = None

        if request_type == 'LaunchRequest':
            message = 'Hello huge! Bow to your new master!'
        else:
            try:
                intentStr = self.info['request']['intent']['name']
            except:
                return self.answer(buildResponse(message='Ending.'))

            if intentStr == 'WhoIs':
                field = self.info['request']['intent']['slots']['name']['value'].lower()
            elif intentStr == 'HelpIntent':
                context = Context.query().get()
                context.lastIntentType = None
                context.lastField = None
                context.sessionCount = 0
                context.put()
                return self.answer(buildResponse(
                    message='I provide small bits of marketing information. For example say stats about youtube.',
                    reprompt='Say stats about youtube.',
                ))
            elif intentStr == 'Seinfeld':
                joke = self.info['request']['intent']['slots']['search']['value']
                return self.answer(buildResponse(
                    message="What's the deal with {search}? I don't get it.".format(search=joke)
                ))
            elif intentStr == 'SearchFor':
                field = self.info['request']['intent']['slots']['search'].get('value', '')\
                    .lower().replace('the', '').replace('and', '').replace('you tube', 'youtube')\
                    .replace('super bowl', 'superbowl').replace("'", "")
                if not field:
                    return self.answer(buildResponse(message='Missing search term.'))

            intent, context = load(
                requestType=request_type,
                intentType=intentStr,
                intentTerm=field
            ).get_result()

            if newSession:
                context.sessionCount = 0
            else:
                if hasattr(context, 'sessionCount'):
                    context.sessionCount += 1
                else:
                    context.sessionCount = 1

            if intentStr == 'YesIntent':
                if hasattr(context, 'lastField') and context.lastField:
                        field = context.lastField
            elif intentStr == 'NoIntent':
                if getattr(context, 'sessionCount', 0) > 1:
                    context.lastIntentType = None
                    context.lastField = None
                    context.sessionCount = 0
                    context.put()
                    return self.answer(buildResponse(message='Was that good for you too?'))
                else:
                    return self.answer(buildResponse(message='ok'))

            if intentStr == 'Execute':
                command = self.info['request']['intent']['slots']['action']['value'].lower()
                if command in ('repeat', 'say again', 'say that again'):
                    context = Context.query().get()
                    if hasattr(context, 'lastResponse') and context.lastResponse:
                        return self.answer(buildResponse(message=context.lastResponse))
                    else:
                        return self.answer(buildResponse(message='Sorry I could not find a previous response.'))
                elif command in ('another one', 'another 1'):
                    if hasattr(context, 'lastField') and context.lastField:
                        field = context.lastField
                    else:
                        return self.answer(buildResponse(message='Sorry I cannot find a previous search to repeat.'))
                else:
                    return self.answer(buildResponse(message='Sorry I do not know the command {c}.'.format(c=command)))

            if field:
                from cerebro import NUGGET_TYPE, DEFAULT_LOCALE
                searchResult = search_client.search(
                    query=field,
                    locale=DEFAULT_LOCALE,
                    count=False,
                    limit=40,
                    sort_field='relevance',
                    source_type=NUGGET_TYPE
                )

            if intent:
                message = intent.getAnswer(self.info)
            elif searchResult:
                results, urls = SearchApi.format_text_results(searchResult.get("search_response", []))
                if results:
                    message = results[randint(0, len(results) - 1)].replace('&', 'and')
                    log.info(results)
                    log.info(message)

                    if len(results) > 1:
                        reprompt = 'I found more than {c} results. Would you like to hear another?'.format(
                            c=(len(results) - 1))
                    else:
                        reprompt = 'Anything else?'
            else:
                return self.answer(buildResponse(message='Huge could not find a matching command.'))

        context.lastIntentType = intentStr
        context.lastField = field
        context.lastResponse = message
        context.put()
        self.answer(buildResponse(message=message, reprompt=reprompt))
