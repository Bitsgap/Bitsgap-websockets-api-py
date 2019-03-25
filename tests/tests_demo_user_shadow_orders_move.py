import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSDemoShadowOrdersMove(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_shadow_orders_open_demo(market)

    id = 'f04a5830f14e4a3eae90e563dfbb549f'

    authClient.move_shadow_order_demo(market, id, "0.35")

    authClient.start(callback=my_handler)
