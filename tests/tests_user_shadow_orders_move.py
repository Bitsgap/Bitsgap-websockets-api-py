import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSShadowOrdersMove(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_shadow_orders_open(market)

    id = '4090ea9e9b704ae6ae87b2ecdcb22720'

    authClient.move_shadow_order(market, id, "0.35")

    authClient.start(callback=my_handler)
