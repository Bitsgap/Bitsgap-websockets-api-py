from enum import Enum


class ChartType(Enum):
    ChartAsks = 'asks'      # asks data
    ChartBids = 'bids'      # bids data
    ChartTrades = 'rt'      # recent trades
    ChartTrans = 'trans'    # buy/sell volumes
