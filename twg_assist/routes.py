import webapp2
from twg_assist.handlers.apiai import APIAIHandler

_APP = webapp2.WSGIApplication([
    webapp2.Route('/webhooks', handler=APIAIHandler, name='webhook'),
], debug=True)
