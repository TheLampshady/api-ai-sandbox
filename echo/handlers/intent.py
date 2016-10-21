import json
from base import BaseEchoHandler
from echo.models.intent import Intent
from google.appengine.ext import ndb


class IntentIndexHandler(BaseEchoHandler):

    def get(self):
        intents = Intent.query().fetch()
        self.context['intents'] = intents
        self.render('intentIndex.html')


class IntentDetailHandler(BaseEchoHandler):

    def get(self, id):
        self.context['json'] = json

        if id == 'new':
            intent = Intent()
        else:
            intent = ndb.Key(Intent, id).get()
        self.context['intent'] = intent
        self.render('intentDetail.html')

    def post(self, id):
        delete = self.request.POST.get('_method', None) == 'DELETE'
        if delete:
            ndb.Key(Intent, id).delete()
            return self.redirect(self.urlFor('echo-intents'))

        if id == 'new':
            intent = Intent()
        else:
            intent = ndb.Key(Intent, id).get()
        intent.type = self.request.POST['type']
        intent.term = self.request.POST['term']
        intent.message = self.request.POST['message']
        intent.put()
        self.redirect(self.urlFor('echo-intents'))

    def delete(self, id):
        ndb.Key(Intent, id).delete()
        self.redirect(self.urlFor('echo-intents'))
