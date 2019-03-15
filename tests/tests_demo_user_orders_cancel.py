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

    demo_key = 'bittrex@63d9a386-d083-11e7-9ac6-901b0edee5f6'

    authClient.subscribe_orders_open_demo(market)

    id = '282e68c79fd14c80ae1c67feb59691b2'

    authClient.cancel_order_demo(demo_key, id)

    id = '2b63c7f0b91441d890f37c10dd582b21'

    authClient.cancel_order_demo(demo_key, id)

    authClient.start(callback=my_handler)
