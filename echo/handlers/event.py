from base import BaseEchoHandler


class EventIndexHandler(BaseEchoHandler):

    def get(self):
        self.render('eventIndex.html')
