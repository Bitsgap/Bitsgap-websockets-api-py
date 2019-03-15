import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSMarkets(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)
    market = 'kraken'
    authClient.get_pairs_config(market)
    authClient.start(callback=my_handler)
