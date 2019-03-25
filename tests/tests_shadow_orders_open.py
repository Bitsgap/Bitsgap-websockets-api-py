import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSShadowOrdersOpen(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    market = 'bittrex'

    authClient.subscribe_shadow_orders_open(market)

    authClient.subscribe_shadow_orders_open_demo(market)

    authClient.start(callback=my_handler)
