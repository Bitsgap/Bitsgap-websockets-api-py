import logging
from unittest import TestCase

from chart_scales import ChartScale
from chart_types import ChartType
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSChartDataAsks(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)
    market = 'kraken'
    pair = 'ETH_USD'

    authClient.get_chart_data(market, pair, ChartType.ChartAsks, ChartScale.ChartMinute, '20190303')
    authClient.get_chart_data(market, pair, ChartType.ChartAsks, ChartScale.ChartHour, '201903')
    authClient.get_chart_data(market, pair, ChartType.ChartAsks, ChartScale.ChartDay, '2019')

    authClient.start(callback=my_handler)
