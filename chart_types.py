from enum import Enum


class ChartType(Enum):
    ChartAsk = 'asks'       # asks data
    ChartBids = 'bids'      # bids data
    ChartTrades = 'rt'      # recent trades
    ChartTrans = 'trans'    # buy/sell volumes
