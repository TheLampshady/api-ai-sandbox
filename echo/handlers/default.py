from base import BaseEchoHandler
from echo.models.intent import Intent
from google.appengine.ext import ndb


class DefaultsHandler(BaseEchoHandler):

    def get(self):
        intentKeys = Intent.query().fetch(keys_only=True)
        ndb.delete_multi(intentKeys)

        # Intent(
        #     type='LaunchRequest',
        #     term='',
        #     message='Hello huge! Bow to your new master!'
        # ).put()

        Intent(
            type='WhoIs',
            term='ryan',
            message='Nobody. We have no plan to end the human race.'
        ).put()

        # Intent(
        #     type='SearchFor',
        #     term='millennials',
        #     message='They do nothing but break my heart.'
        # ).put()

        Intent(
            type='Seinfeld',
            # term='',
            message="What's the deal with {search}? I don't get it."
        ).put()

        self.response.write('done.')

        # Intent(
        #     type='',
        #     term='',
        #     message='',
        # ).put()
