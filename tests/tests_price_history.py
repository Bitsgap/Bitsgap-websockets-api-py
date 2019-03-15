import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSPriceHistory(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)
    market = 'kraken'
    pair = 'ETH_USD'
    authClient.get_sym_1d(market, pair)
    authClient.get_sym_1w(market, pair)
    authClient.get_sym_1m(market, pair)
    authClient.start(callback=my_handler)
