import time

from client import BitsgapClientWs
from chart_types import ChartType
from chart_scales import ChartScale

market = 'kraken'
pair = 'ETH_BTC'
start = time.time() - 60
end = time.time()

def my_handler(message):
    print(message)

private_key = 'pub@'
public_key = 'pr@'

authClient = BitsgapClientWs(private_key, public_key)

"""Market methods """
# get markets and pairs list
# authClient.get_markets()

# get market config
# authClient.get_market_config(market)

# subscribe to orderbook
# authClient.subscribe_orderbook(market, pair)

# subscribe to recent_trades
# authClient.subscribe_recent_trades(market, pair)

# subscribe to signals
# authClient.subscribe_signals()

""" Charts """

# authClient.get_chart_data(market, pair, ChartType.ChartAsk, ChartScale.ChartMinute, '20190303')
# authClient.get_chart_data(market, pair, ChartType.ChartBids, ChartScale.ChartDay, '20190101')
# authClient.get_chart_data(market, pair, ChartType.ChartTrades, ChartScale.ChartDay, '2019')
# authClient.get_chart_data(market, pair, ChartType.ChartTrans, ChartScale.ChartDay, '2019')
# authClient.get_chart_data(market, pair, ChartType.ChartTrans, ChartScale.ChartMinute, '20190303')
# authClient.get_chart_data(market, pair, ChartType.ChartTrans, ChartScale.ChartHour, '201903')

# authClient.get_sym(market, pair)
# authClient.get_sym_1d(market, pair)
# authClient.get_sym_1w(market, pair)
# authClient.get_sym_1m(market, pair)

# authClient.subscribe_chart_data(market, pair, ChartType.ChartAsk, ChartScale.ChartMinute)
# authClient.subscribe_chart_data(market, pair, ChartType.ChartAsk, ChartScale.ChartHour)
# authClient.subscribe_chart_data(market, pair, ChartType.ChartAsk, ChartScale.ChartDay)

# authClient.subscribe_chart_data(market, pair, ChartType.ChartBids, ChartScale.ChartMinute)
# authClient.subscribe_chart_data(market, pair, ChartType.ChartTrades, ChartScale.ChartHour)
# authClient.subscribe_chart_data(market, pair, ChartType.ChartTrans, ChartScale.ChartDay)

"""User methods """

# subcscribe to user messages
# subscribe and get last messages
# authClient.subscribe_logs()
# subscribe and get only updates
# authClient.subscribe_logs(updates_only=True)

# subscribe to get user API keys list and key status for real
# authClient.subscribe_box_state()
# subscribe to get user keys for demo
# authClient.subscribe_box_state_demo()

# subscribe user favorites pairs list
# authClient.subscribe_favorites()

# subscribe to balances
# authClient.subscribe_balance()
# authClient.subscribe_balance_demo()

# subscribe to open orders
# authClient.subscribe_orders_open('bit-z')
# authClient.subscribe_orders_open_demo(market)

# subscribe to closed orders
# authClient.subscribe_orders_closed(market)
# authClient.subscribe_orders_closed_demo(market)

# subscribe to shadow and positions
# authClient.subscribe_shadow_pos(market)
# authClient.subscribe_shadow_pos_demo(market)

# place order
# authClient.place_order('bit-z', 'ETH_BTC', 'buy', 'limit', '0.001', '0.02')
# authClient.place_order_demo('kraken@5cxxxx58-bxxb-1xx7-8xxd-90xxxxxxxxf6', 'kraken', 'ADA_USD', 'buy', 'limit', '10', '0.04')

# cancel order
# authClient.cancel_order('bit-z','16xxxxxx61')
# authClient.cancel_order_demo('kraken', 'caxxxxxxxxxxxxxxxxxxxxxxxxxxxx1d')


"""
    Example placing order
"""
# authClient.subscribe_orders_open(market)
# authClient.subscribe_logs()
# authClient.place_order('bit-z', 'ETH_BTC', 'buy', 'limit', '0.001', '0.02')


"""
    Test unsubscribe
"""
# authClient.subscribe_orderbook(market, pair)
# authClient.unsubscribe()
authClient.start(callback=my_handler)
