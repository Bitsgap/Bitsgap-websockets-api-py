import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSUserKeys(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    market = 'bittrex'

    authClient.get_market_balance(market)

    authClient.start(callback=my_handler)
