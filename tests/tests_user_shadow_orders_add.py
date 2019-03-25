import logging
from unittest import TestCase
from client import BitsgapClientWs
from tests.keys import public_key,private_key


class TestWSShadowOrdersAdd(TestCase):

    def my_handler(message):
        logging.info(message)

    authClient = BitsgapClientWs(public_key, private_key)

    authClient.subscribe_logs()

    market = 'bittrex'

    authClient.subscribe_shadow_orders_open(market)

    pair = 'EDR_USD'
    side = 'sell'
    order_type = 'limit'
    amount = '150'
    price = '0.25'

    authClient.place_shadow_order(market, pair, side, order_type,amount, price)
    
    authClient.start(callback=my_handler)
