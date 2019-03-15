import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSOrdersCancel(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)


    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_orders_open(market)

    id = 'e5ab1ef5-28c1-4689-b9c6-a3b5cc13f344'

    authClient.cancel_order(market, id)

    authClient.start(callback=my_handler)
