import webapp2


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('Huge Echo Main Page!')


application = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler, name='home'),
], debug=True)
