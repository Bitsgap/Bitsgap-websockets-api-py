import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSShadowOrdersCancel(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_shadow_orders_open(market)

    id = '090c3d4dc9884a58bfd971384bf33ebd'

    authClient.cancel_shadow_order(market, id)

    authClient.start(callback=my_handler)
