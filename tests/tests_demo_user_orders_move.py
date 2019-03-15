import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSDemoOrdersMove(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_orders_open_demo(market)

    id = 'ebff9720da944ab187680f4347e5ee03'
    demo_key = 'bittrex@63d9a386-d083-11e7-9ac6-901b0edee5f6'

    authClient.move_order_demo(demo_key, id, "0.035")

    authClient.start(callback=my_handler)
