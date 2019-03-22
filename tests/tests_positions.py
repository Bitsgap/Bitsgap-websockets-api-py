import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSPositions(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    market = 'bittrex'

    authClient.subscribe_smart_positions(market)

    authClient.subscribe_smart_positions_demo(market)

    authClient.start(callback=my_handler)
