import asyncio
import gzip
import hashlib
import hmac
import json

from autobahn.asyncio.websocket import WebSocketClientFactory, WebSocketClientProtocol
import logging
from chart_types import ChartType

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s', level=logging.DEBUG)

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        logging.debug('socket onConnect')

    async def onOpen(self):
        logging.debug('socket onOpen')

    async def onMessage(self, message, isBinary):
        logging.debug(message)
        # prepare data to
        if isBinary:
            # compressed data by gzip
            if type(message) is bytes and \
                    message[0] == 31 and \
                    message[1] == 139:
                message = self.get_binary(message)
                self.factory.callback(message)
            return
        try:
            message_jsn = json.loads(message)

            if 'login' in message_jsn:
                verify_mess = message_jsn['login']
                if 'status' not in message_jsn:
                    # no status, send auth message
                    pub_key = self.factory.base_client.public_key
                    prv_key = self.factory.base_client.private_key
                    mess_for_crypt = pub_key + verify_mess
                    mess_hash = self.get_signature(mess_for_crypt, prv_key)

                    send_mess = {"login": mess_hash}
                    send_mess_str = json.dumps(send_mess)

                    self.sendMessage(send_mess_str.encode(), isBinary=False)
                else:
                    status = message_jsn['status']
                    # authorized
                    if status == 'valid':
                        if self.factory.base_client.requests:
                            if len(self.factory.base_client.requests)>0:
                                for request in self.factory.base_client.requests:
                                    self.sendMessage(request.encode(), isBinary=False)
                    else: # not authorized
                        logging.debug(message_jsn)
            else:
                self.factory.callback(message.decode())
        except Exception as ex:
            logging.warning(ex.args)

    async def onClose(self, wasClean, code, reason):
        logging.debug('socket onClose')

    def get_signature(self, message, private_key):
        sign = hmac.new(private_key.encode(), message.encode(), digestmod=hashlib.sha512).hexdigest()
        return sign

    def convert_nested_list_to_dict(self, in_items):
        out_dict = in_items
        if type(in_items) is list:
            out_dict = {}
            out_dict = self.convert_list_to_dict(in_items)
        for key, val in out_dict.items():
            if type(val) is list:
                out_dict[key] = self.convert_list_to_dict(val)
        return out_dict

    def convert_list_to_dict(self, in_list):
        out_dict = {}
        m = 0
        for in_l in in_list:
            out_dict[str(m)] = in_l
            m = m + 1
        return out_dict

    def get_binary(self, mess_gzip):
        ob_m_str = gzip.decompress(mess_gzip)
        ob_m_dict = json.loads(ob_m_str)
        ob_m_value = ob_m_dict['value']
        ob_m_value = self.convert_nested_list_to_dict(ob_m_value)
        return ob_m_value

class BitsgapClientWs:
    public_key = None
    private_key = None
    requests = []

    def __init__(self, key, secret):
        self.public_key = key
        self.private_key = secret

    def start(self, **kwargs):
        host = 'var.bitsgap.com'
        port = 443
        ssl = True
        conn_str = f'wss://{host}/ws/?wsguid={self.public_key}'
        factory = WebSocketClientFactory(conn_str)
        factory.protocol = MyClientProtocol
        if 'callback' in kwargs:
            factory.callback = kwargs['callback']
        factory.base_client = self
        loop = asyncio.get_event_loop()
        try:
            coro = loop.create_connection(factory, host, port, ssl=ssl)
            loop.run_until_complete(coro)
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    """
        Create message for sending to system
    """
    def send_message(self, proc, **kwargs):
        message = {
            'type': 'push_subs',
            'skey': {
                'proc': proc
            }
        }

        """
            Subscription type
            push_subs - public data
            users_push_subs - user data
        """
        if 'is_user' in kwargs:
            message['type'] = 'users_push_subs'

        """
            Request params
        """
        if 'market' in kwargs:
            message['skey']['market'] = kwargs['market']
        if 'pair' in kwargs:
            message['skey']['pair'] = kwargs['pair']
        if 'trade' in kwargs:
            message['skey']['trade'] = kwargs['trade']

        """
            Subscribe  
            1 - subscribe and get last result
            10 - subscribe and get only new results(updates)
        """
        if 'is_sub' in kwargs:
            message['subs'] = '1'
        if 'updates_only' in kwargs:
            if kwargs['updates_only']:
                message['subs'] = '10'

        """
            Unsubscribe 
            0 - unsubscribe from selected skey
            kill - unsubscribe from all subscriptions
        """
        if 'is_unsub' in kwargs:
            if proc:
                message['subs'] = '0'
            else:
                message.pop('skey')
                message['subs'] = 'kill'
                message['type'] = 'subs'

        logging.debug(message)
        return json.dumps(message)
    
    """
        Create control message for sending to system
    """
    def send_control_message(self, proc, **kwargs):

        message = {
            'type': 'users_push',
            'skey': {
                'proc': 'action.wstask'
            },
            'value': {
                'key': proc
            }
        }
        if 'params' in kwargs:
            params = kwargs['params']
            message['value'].update(params)

        logging.debug(message)
        return json.dumps(message)
    
    """ 
        Market methods         
    """

    # Get markets and pairs list
    def get_markets(self):
        self.requests.append(self.send_message('v_conf_pairs_to', is_sub=False))

    # Get pairs config
    def get_pairs_config(self, market):
        self.requests.append(self.send_message('v_conf_pairs', is_sub=False, market=market))

    # Get recent trades for selected market and pair
    def subscribe_recent_trades(self, market, pair):
        self.requests.append(self.send_message('rt', is_sub=True, market=market, pair=pair))

    # Get orderbook for selected market and pair
    def subscribe_orderbook(self, market, pair):
        self.requests.append(self.send_message('ob', is_sub=True, market=market, pair=pair))

    # Subscribe to get last ask and bid price for market
    def subscribe_sym(self, market, pair):
        self.requests.append(self.send_message('sym', is_sub=True,  market=market, pair=pair))

    # get pair price for market 1 day ago
    def get_sym_1d(self, market, pair):
        self.requests.append(self.send_message('sym.1d', market=market, pair=pair))

    # get pair price for market 1 week ago
    def get_sym_1w(self, market, pair):
        self.requests.append(self.send_message('sym.1w', market=market, pair=pair))

    # get pair price for market 1 month ago
    def get_sym_1m(self, market, pair):
        self.requests.append(self.send_message('sym.1m', market=market, pair=pair))

    # subscribe to get signals
    def subscribe_signals(self):
        self.requests.append(self.send_message('signal', is_sub=True))

    """ 
        User methods
        For using this methods need to add API keys for real markets
    """

    # Get user balance for real markets
    def subscribe_balance(self):
        self.requests.append(self.send_message('app.markets.balance', is_sub=True, is_user=True, trade="real"))

    # Get user balance for demo markets
    def subscribe_balance_demo(self):
        self.requests.append(self.send_message('app.markets.balance', is_sub=True, is_user=True, trade="demo"))

    # Subscribe to user open orders on real markets
    def subscribe_orders_open(self, market):
        self.requests.append(self.send_message('app.openorders', is_sub=True, is_user=True, market=market))

    # Subscribe to user open orders on demo markets
    def subscribe_orders_open_demo(self, market):
        market = market + ".demo"
        self.requests.append(self.send_message('app.openorders', is_sub=True, is_user=True, market=market))

    # Subscribe to user closed orders on real markets
    def subscribe_orders_closed(self, market):
        self.requests.append(self.send_message('app.ordershistory.current', is_sub=True, is_user=True, market=market))

    # Subscribe to user closed orders on demo markets
    def subscribe_orders_closed_demo(self, market):
        market = market + ".demo"
        self.requests.append(self.send_message('app.ordershistory.current', is_sub=True, is_user=True, market=market))

    """
        Subscribe to get real markets API keys and status
    """
    def subscribe_keys(self):
        self.requests.append(self.send_message('box.state', is_sub=True, is_user=True))

    """ 
        Subscribe to get demo keys
    """
    def subscribe_box_state_demo(self):
        self.requests.append(self.send_message('demo.keys', is_sub=True, is_user=True))

    # Subscribe to user closed orders on demo markets
    def subscribe_shadow_pos(self, market):
        self.requests.append(self.send_message('shadow.pos', is_sub=True, is_user=True, market=market))

    # Subscribe to user closed orders on demo markets
    def subscribe_shadow_pos_demo(self, market):
        market = market + ".demo"
        self.requests.append(self.send_message('shadow.pos', is_sub=True, is_user=True, market=market))

    """ 
        Subscribe to user messages
        If updates_only = True user will get only new messages after subscription
        Otherwise user will get last message
    """
    def subscribe_logs(self, updates_only=False):
        self.requests.append(self.send_message('q.messages', is_sub=True, is_user=True, updates_only=updates_only))

    # Get chart data
    def get_chart_data(self, market, pair, chart_type, chart_scale, chart_date):
        ws_key = 'chart'
        if chart_type != ChartType.ChartAsk:
            ws_key = f'{ws_key}.{chart_type.value}'
        ws_key = f'{ws_key}.{chart_scale.value}.{chart_date}'
        self.requests.append(self.send_message(ws_key, market=market, pair=pair))

    """
        Subscribe to get chart data updates
    """
    def subscribe_chart_data(self, market, pair, chart_type, chart_scale):
        if chart_type == ChartType.ChartAsk:
            ws_key = 'candle'
        if chart_type == ChartType.ChartBids:
            ws_key = 'candlebids'
        if chart_type == ChartType.ChartTrans:
            ws_key = 'candletrans'
        if chart_type == ChartType.ChartTrades:
            ws_key = 'trans'
        ws_key = f'{ws_key}.{chart_scale.value}.0'
        self.requests.append(self.send_message(ws_key, is_sub=True, market=market, pair=pair))

    """ 
        Trading methods 
    """

    """ 
        Place demo order 
        To track the status of an order, you must subscribe to a list of open orders and user messages.
    """
    def place_order_demo(self, market, pair, side, order_type, amount, price):
        send_struct = {
             "params": {
                 "market": market,
                 "pair": pair,
                 "side": side,
                 "type": order_type,
                 "amount": amount,
                 "price": price
             }
        }
        self.requests.append(self.send_control_message('demo@order_place', params=send_struct))

    """
        Place real order
        To track the status of an order, you must subscribe to a list of open orders and user messages.
    """
    def place_order(self, market, pair, side, order_type, amount, price):
        send_struct = {
             "params": {
                 "market": market,
                 "pair": pair,
                 "side": side,
                 "type": order_type,
                 "amount": amount,
                 "price": price
             }
        }
        self.requests.append(self.send_control_message('trade@order_place', params=send_struct))

    """ 
        Cancel demo order        
    """
    def cancel_order_demo(self, market, id):
        send_struct = {
             "params": {
                 "market": market,
                 "id": id
             }
        }
        self.requests.append(self.send_control_message('demo@order_cancel', params=send_struct))

    """ 
        Cancel real order        
    """
    def cancel_order(self, market, id):
        send_struct = {
             "params": {
                 "market": market,
                 "id": id
             }
        }
        self.requests.append(self.send_control_message('trade@order_cancel', params=send_struct))

    """ 
        Move demo order 
    """
    def move_order_demo(self, market, id, price):
        send_struct = {
             "params": {
                 "market": market,
                 "price": price,
                 "id": id
             }
        }
        self.requests.append(self.send_control_message('demo@order_move', params=send_struct))

    """ 
        Move real order 
    """
    def move_order(self, market, id, price):
        send_struct = {
             "params": {
                 "market": market,
                 "price": price,
                 "id": id
             }
        }
        self.requests.append(self.send_control_message('trade@order_move', params=send_struct))

    """ 
        Subscribe and request real balance 
    """
    def get_market_balance(self, market):
        send_struct = {
             "params": {
                 "market": market
             }
        }
        self.requests.append(self.send_control_message('trade@balance', params=send_struct))

    def unsubscribe(self, key=None):
        self.requests.append(self.send_message(key, is_unsub=True))
