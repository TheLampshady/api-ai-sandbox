import json
from echo.models.eventLog import EventLog
from echo.tests.base import BaseTestCase


class TestEventLog(BaseTestCase):

    def setUp(self):
        super(TestEventLog, self).setUp()

    def test_new(self):
        test = json.dumps({'name': 'test'})
        el = EventLog.new(test).get_result()

        results = EventLog.query().fetch()
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual(u'{"name": "test"}', result.request)

    def test_close(self):
        test1 = json.dumps({'name': 'test1'})
        test2 = json.dumps({'name': 'test2'})
        el = EventLog.new(test1).get_result()
        el.close(test2).get_result()

        results = EventLog.query().fetch()
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual(u'{"name": "test1"}', result.request)
        self.assertEqual(u'{"name": "test2"}', result.response)
