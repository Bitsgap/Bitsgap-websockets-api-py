import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSDemoOrdersAdd(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_orders_open_demo(market)

    pair = 'EDR_USD'
    side = 'sell'
    order_type = 'limit'
    amount = '150'
    price = '0.25'

    authClient.place_order_demo(market, pair, side, order_type, amount, price)

    authClient.start(callback=my_handler)
