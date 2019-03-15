import logging
from unittest import TestCase

from chart_scales import ChartScale
from chart_types import ChartType
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSChartUpdateBids(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)
    market = 'kraken'
    pair = 'ETH_USD'

    authClient.subscribe_chart_data(market, pair, ChartType.ChartBids, ChartScale.ChartMinute)
    authClient.subscribe_chart_data(market, pair, ChartType.ChartBids, ChartScale.ChartHour)
    authClient.subscribe_chart_data(market, pair, ChartType.ChartBids, ChartScale.ChartDay)

    authClient.start(callback=my_handler)
