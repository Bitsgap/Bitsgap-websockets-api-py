import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSDemoOrdersCancel(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)


    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_orders_open_demo(market)

    id = '606d836e8ef44497bc81c3ae08edb95d'

    authClient.cancel_order_demo(market, id)

    authClient.start(callback=my_handler)
