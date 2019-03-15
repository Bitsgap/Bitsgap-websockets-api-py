import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSOrdersMove(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_orders_open(market)

    id = '1d6093f9-e44c-4cb1-88f3-2c763019208b'

    authClient.move_order(market, id, "0.05")

    authClient.start(callback=my_handler)
