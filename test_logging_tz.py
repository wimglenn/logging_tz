import io
import logging
import pytz
import unittest

from freezegun import freeze_time
from mock import patch

from logging_tz import LocalFormatter, ChicagoFormatter


class ChicagoFormatterTest(unittest.TestCase):

    def setUp(self):
        super(ChicagoFormatterTest, self).setUp()
        self.logger = logging.getLogger('test')
        self.collector = io.BytesIO()
        handler = logging.StreamHandler(stream=self.collector)
        handler.setFormatter(ChicagoFormatter('%(asctime)s %(message)s'))
        self.logger.addHandler(handler)

    def test_chicago_formatter(self):
        with freeze_time('19 Mar 1982, 12:34:56'):
            self.logger.warning('your mom')
        val = self.collector.getvalue()
        assert val == '1982-03-19 06:34:56-0600 your mom\n'


class LocalFormatterTest(unittest.TestCase):

    def setUp(self):
        super(LocalFormatterTest, self).setUp()
        self.logger = logging.getLogger('test')

        self.collector_plus10 = io.BytesIO()
        handler_plus10 = logging.StreamHandler(stream=self.collector_plus10)
        with patch('logging_tz.tzlocal.get_localzone', lambda: pytz.timezone('Australia/Melbourne')):
            formatter_plus10 = LocalFormatter('%(asctime)s %(message)s')
        handler_plus10.setFormatter(formatter_plus10)

        self.collector_utc = io.BytesIO()
        handler_utc = logging.StreamHandler(stream=self.collector_utc)
        formatter_utc = LocalFormatter('%(asctime)s %(message)s', tz=pytz.UTC)
        handler_utc.setFormatter(formatter_utc)

        self.logger.addHandler(handler_plus10)
        self.logger.addHandler(handler_utc)

        with freeze_time('19 Mar 1982, 12:34:56'):
            self.logger.warning('your mum')

    def test_local_formatter_resolves_localzone(self):
        # tz was resolved in LocalFormatter.__init__
        val = self.collector_plus10.getvalue()
        assert val == '1982-03-19 22:34:56+1000 your mum\n'

    def test_local_formatter_with_localzone_passed_explicitly(self):
        # tz was passed explicitly when creating the formatter object
        val = self.collector_utc.getvalue()
        assert val == '1982-03-19 12:34:56+0000 your mum\n'
