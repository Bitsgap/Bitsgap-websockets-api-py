import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSOrderbook(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)
    market = 'kraken'
    pair = 'ETH_USD'
    authClient.subscribe_orderbook(market, pair)
    authClient.start(callback=my_handler)
