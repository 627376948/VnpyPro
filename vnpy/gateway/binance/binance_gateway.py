# encoding: UTF-8
"""
"""

import hashlib
import hmac
import sys
import time
from copy import copy
from datetime import datetime
from threading import Lock
from urllib.parse import urlencode

from requests import ConnectionError

from vnpy.api.rest import Request, RestClient
from vnpy.api.websocket import WebsocketClient
from vnpy.trader.constant import (
    Direction,
    Exchange,
    OrderType,
    Product,
    Status,
)
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.object import (
    TickData,
    OrderData,
    TradeData,
    PositionData,
    AccountData,
    ContractData,
    OrderRequest,
    CancelRequest,
    SubscribeRequest,
)

REST_HOST = "https://www.binance.com"
WEBSOCKET_HOST = "wss://stream.binance.com:9443/ws"
WEBSOCKET_STREAM_HOST = "wss://stream.binance.com:9443/stream?streams="

TESTNET_REST_HOST = "https://testnet.bitmex.com/api/v1"
TESTNET_WEBSOCKET_HOST = "wss://testnet.bitmex.com/realtime"

STATUS_BITMEX2VT = {
    "New": Status.NOTTRADED,
    "Partially filled": Status.PARTTRADED,
    "Filled": Status.ALLTRADED,
    "Canceled": Status.CANCELLED,
    "Rejected": Status.REJECTED,
}

DIRECTION_VT2BITMEX = {Direction.LONG: "Buy", Direction.SHORT: "Sell"}
DIRECTION_BITMEX2VT = {v: k for k, v in DIRECTION_VT2BITMEX.items()}

ORDERTYPE_VT2BITMEX = {OrderType.LIMIT: "Limit", OrderType.MARKET: "Market"}


class BinanceGateway(BaseGateway):
    """
    VN Trader Gateway for Binance connection.
    """

    default_setting = {
        "key": "Fuq7glzRmQk0p3mw56yCaF1Io2BKZrc13SUGPtxw1tcMstKwdV1jmRevt7eEZfwa",
        "secret": "O8mXvn14rfMVjlEDkZnNigvOOWIRYq7R9a0ARNTTchQKTDv4mYWZxSMc1Xf8eCBm",
        "session_number": 3,
        "server": ["REAL", "TESTNET"],
        "proxy_host": "127.0.0.1",
        "proxy_port": 1080,
    }

    def __init__(self, event_engine):
        """Constructor"""
        super(BinanceGateway, self).__init__(event_engine, "BINANCE")

        self.rest_api = BinanceRestApi(self)
        self.ws_api = BinanceWebsocketApi(self)

    def connect(self, setting: dict):
        """"""
        key = setting["key"]
        secret = setting["secret"]
        session_number = setting["session_number"]
        server = setting["server"]
        proxy_host = setting["proxy_host"]
        proxy_port = setting["proxy_port"]

        self.rest_api.connect(key, secret, session_number,
                              server, proxy_host, proxy_port)

        self.ws_api.connect(key, secret, server, proxy_host, proxy_port)
        # websocket will push all account status on connected, including asset, position and orders.

    def subscribe(self, req: SubscribeRequest):
        """"""
        self.ws_api.subscribe(req)

    def send_order(self, req: OrderRequest):
        """"""
        return self.rest_api.send_order(req)

    def cancel_order(self, req: CancelRequest):
        """"""
        self.rest_api.cancel_order(req)

    def query_account(self):
        """"""
        self.rest_api.query_account(self)

    def query_position(self):
        """"""
        pass

    def close(self):
        """"""
        self.rest_api.stop()
        self.ws_api.stop()


class BinanceRestApi(RestClient):
    """
    Binance REST API
    """

    def __init__(self, gateway: BaseGateway):
        """"""
        super(BinanceRestApi, self).__init__()

        self.gateway = gateway
        self.gateway_name = gateway.gateway_name

        self.key = ""
        self.secret = ""

        self.signed = None
        self.stream = None

        self.order_count = 1_000_000
        self.order_count_lock = Lock()

        self.connect_time = 0

    def sign(self, request):
        """
        Generate Binance signature.
        """
        # Sign
        if not self.signed:
            url = REST_HOST + path
            headers = {}
        else:
            if not self.stream:
                request.params['recvWindow'] = self.recvWindow
                request.params['timestamp'] = int(time()*1000)
                query = urlencode(sorted(request.params.items()))
                 
                signature = hmac.new(self.secret, query.encode('utf-8'),
                                     hashlib.sha256).hexdigest()
                query += "&signature={}".format(signature)
                
                url = REST_HOST + path + '?' + query
                request.params = None
            else:
                if request.params:
                    query = urlencode(sorted(request.params.items()))
                    url = REST_HOST + path + '?' + query
                    request.params = None
                else:
                    url = REST_HOST + path
            
        # Add headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
             "Accept": "application/json",
            "X-MBX-APIKEY": self.apiKey
        }
        request.headers = headers
        return request

    def connect(
        self,
        key: str,
        secret: str,
        session_number: int,
        server: str,
        proxy_host: str,
        proxy_port: int,
    ):
        """
        Initialize connection to REST server.
        """
        self.apiKey = key
        self.secretKey = secret.encode()

        self.connect_time = (
            int(datetime.now().strftime("%y%m%d%H%M%S")) * self.order_count
        )

        self.init(REST_HOST, proxy_host, proxy_port)

        self.start(session_number)

        self.gateway.write_log("REST API启动成功")

    # Test connectivity to the Rest API.
    def query_ping(self):
        path = '/api/v1/ping'
        return self.add_request(
            "GET",
            path,
            callback = self.on_query_ping)

    # Test connectivity to the Rest API and get the current server time.
    def query_time(self):
        path = '/api/v1/time'
        return self.add_request(
            "GET",
            path,
            callback = self.on_query_time)

    # Current exchange trading rules and symbol information.
    def query_exchangeInfo(self):
        path = '/api/v1/exchangeInfo'
        return self.add_request(
            "GET",
            path,
            callback = self.on_query_exchangeInfo)

    # Order book.
    def query_depth(self, req: Request):
        path = '/api/v1/depth'
        params = {
            "symbol": req.symbol
        }
        limit = req.limit
        if limit:
            params['limit'] = limit
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_depth)

    # Order book.
    def query_trades(self, req: Request):
        path = '/api/v1/trades'
        params = {
            "symbol": req.symbol
        }
        limit = req.limit
        if limit:
            params['limit'] = limit
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_trades)

    def query_historicalTrades(self, req: Request):
        path = '/api/v1/historicalTrades'
        params = {
            "symbol": req.symbol
        }
        limit = req.limit
        fromId = req.fromId
        if limit:
            params['limit'] = limit
        if fromId:
            params['fromId'] = fromId
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_historical_trades)

    def query_aggTrades(self, req: Request):
        path = '/api/v1/aggTrades'
        params = {
            "symbol": req.symbol
        }
        limit = req.limit
        fromId = req.fromId
        startTime = req.starTime
        endTime = req.endTime
        if limit:
            params['limit'] = limit
        if fromId:
            params['fromId'] = fromId
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_aggTrades)

    def query_klines(self, interval, req: Request):
        path = '/api/v1/klines'
        params = {
            "symbol": req.symbol,
            'interval': interval
        }
        limit = req.limit
        fromId = req.fromId
        startTime = req.starTime
        endTime = req.endTime
        if limit:
            params['limit'] = limit
        if fromId:
            params['fromId'] = fromId
        if not all([startTime, endTime]):
            params['startTime'] = startTime
            params['endTime'] = endTime
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_klines)

    def query_avgPrice(self, req: Request):
        path = '/api/v3/avgPrice'
        params = {
            "symbol": req.symbol
        }
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_avgPrice)

    def query_ticker24hr(self, req: Request):
        path = '/api/ticker/24hr'
        params = {
            "symbol": req.symbol
        }
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_ticker24hr)

    def query_tickerPrice(self, req: Request):
        path = '/api/ticker/price'
        params = {
            "symbol": req.symbol
        }
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_tickerPrice)

    def _new_order_id(self):
        with self.order_count_lock:
            self.order_count += 1
            return self.order_count

    def send_order(self, req: OrderRequest):
        """"""
        orderid = str(self.connect_time + self._new_order_id())
        self.signed = True
        data = {
            "symbol": req.symbol,
            "side": req.direction,
            "type": req.price_type,
            "price": req.price,
            "quantity": int(req.volume),
            "newClientOrderId": orderid,
        }

        # Only add price for limit order.
        if req.price_type == OrderType.LIMIT:
            data["price"] = req.price

        order = req.create_order_data(orderid, self.gateway_name)

        self.add_request(
            "POST",
            "/api/v3/order",
            callback=self.on_send_order,
            data=data,
            extra=order,
            on_failed=self.on_send_order_failed,
            on_error=self.on_send_order_error,
        )

        self.gateway.on_order(order)
        return order.vt_orderid

    def query_order(self, req: OrderRequest):
        """"""
        orderid = str(self.connect_time + self._new_order_id())
        self.signed = True
        data = {
            "symbol": req.symbol,
            "side": req.direction,
            "type": req.price_type,
            "price": req.price,
            "quantity": int(req.volume),
            "newClientOrderId": orderid,
        }

        # Only add price for limit order.
        if req.price_type == OrderType.LIMIT:
            data["price"] = req.price

        order = req.create_order_data(orderid, self.gateway_name)

        self.add_request(
            "GET",
            "/api/v3/order",
            callback=self.on_query_order,
            data=data,
            extra=order,
            on_failed=self.on_send_order_failed,
            on_error=self.on_send_order_error,
        )

        self.gateway.on_order(order)
        return order.vt_orderid

    def cancel_order(self, req: CancelRequest):
        """"""
        self.signed = True
        orderid = req.orderid

        if orderid.isdigit():
            params = {"clOrdID": orderid}
        else:
            params = {"orderID": orderid}

        self.add_request(
            "DELETE",
            "/api/v3/order",
            callback=self.on_cancel_order,
            params=params,
            on_error=self.on_cancel_order_error,
        )

    def query_openOrders(self, req: Request):
        self.signed = True
        path = '/api/v3/openOrders'
        params = {
            "symbol": req.symbol
        }
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_openOrders)

    def query_allOrders(self, req: Request):
        self.signed = True
        path = '/api/v3/allOrders'
        params = {
            "symbol": req.symbol
        }
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_allOrders)
    
    def query_account(self):
        self.signed = True
        path = '/api/v3/account'
        params = {
            "symbol": req.symbol
        }
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_account)

    def query_myTrades(self, req: Request):
        self.signed = True
        path = '/api/v3/myTrades'
        params = {
            "symbol": req.symbol
        }
        return self.add_request(
            "GET",
            path,
            params,
            callback = self.on_query_myTrades)

    def on_send_order_failed(self, status_code: str, request: Request):
        """
        Callback when sending order failed on server.
        """
        order = request.extra
        order.status = Status.REJECTED
        self.gateway.on_order(order)

        msg = f"委托失败，状态码：{status_code}，信息：{request.response.text}"
        self.gateway.write_log(msg)

    def on_send_order_error(
        self, exception_type: type, exception_value: Exception, tb, request: Request
    ):
        """
        Callback when sending order caused exception.
        """
        order = request.extra
        order.status = Status.REJECTED
        self.gateway.on_order(order)

        # Record exception if not ConnectionError
        if not issubclass(exception_type, ConnectionError):
            self.on_error(exception_type, exception_value, tb, request)

    def on_send_order(self, data, request):
        """Websocket will push a new order status"""
        pass

    def on_cancel_order_error(
        self, exception_type: type, exception_value: Exception, tb, request: Request
    ):
        """
        Callback when cancelling order failed on server.
        """
        # Record exception if not ConnectionError
        if not issubclass(exception_type, ConnectionError):
            self.on_error(exception_type, exception_value, tb, request)

    def on_cancel_order(self, data, request):
        """Websocket will push a new order status"""
        pass

    def on_failed(self, status_code: int, request: Request):
        """
        Callback to handle request failed.
        """
        msg = f"请求失败，状态码：{status_code}，信息：{request.response.text}"
        self.gateway.write_log(msg)

    def on_error(
        self, exception_type: type, exception_value: Exception, tb, request: Request
    ):
        """
        Callback to handler request exception.
        """
        msg = f"触发异常，状态码：{exception_type}，信息：{exception_value}"
        self.gateway.write_log(msg)

        sys.stderr.write(
            self.exception_detail(exception_type, exception_value, tb, request)
        )


class BinanceWebsocketApi(WebsocketClient):
    """"""

    def __init__(self, gateway):
        """"""
        super(BinanceWebsocketApi, self).__init__()

        self.gateway = gateway
        self.gateway_name = gateway.gateway_name

        self.key = ""
        self.secret = ""

        self.callbacks = {
            "trade": self.on_tick,
            "orderBook10": self.on_depth,
            "execution": self.on_trade,
            "order": self.on_order,
            "position": self.on_position,
            "margin": self.on_account,
            "instrument": self.on_contract,
        }

        self.ticks = {}
        self.accounts = {}
        self.orders = {}
        self.trades = set()

    def connect(
        self, key: str, secret: str, server: str, proxy_host: str, proxy_port: int
    ):
        """"""
        self.apiKey = key
        self.secretKey = secret.encode()

        base = "wss://stream.binance.com:9443"
        self.init(f'{base}/stream?streams=ETHBTC@aggTrade', proxy_host, proxy_port)

        self.start()

    def subscribe(self, req: SubscribeRequest):
        """
        Subscribe to tick data upate.
        """
        tick = TickData(
            symbol=req.symbol,
            exchange=req.exchange,
            name=req.symbol,
            datetime=datetime.now(),
            gateway_name=self.gateway_name,
        )
        self.ticks[req.symbol] = tick

    def on_connected(self):
        """"""
        self.gateway.write_log("Websocket API连接成功")
        #self.authenticate()

    def on_disconnected(self):
        """"""
        self.gateway.write_log("Websocket API连接断开")

    def on_packet(self, packet: dict):
        """"""
        if "error" in packet:
            self.gateway.write_log("Websocket API报错：%s" % packet["error"])

            if "not valid" in packet["error"]:
                self.active = False

        elif "request" in packet:
            req = packet["request"]
            success = packet["success"]

            if success:
                if req["op"] == "authKey":
                    self.gateway.write_log("Websocket API验证授权成功")
                    self.subscribe_topic()

        elif "table" in packet:
            name = packet["table"]
            callback = self.callbacks[name]

            if isinstance(packet["data"], list):
                for d in packet["data"]:
                    callback(d)
            else:
                callback(packet["data"])

    def on_error(self, exception_type: type, exception_value: Exception, tb):
        """"""
        msg = f"触发异常，状态码：{exception_type}，信息：{exception_value}"
        self.gateway.write_log(msg)

        sys.stderr.write(self.exception_detail(
            exception_type, exception_value, tb))

    def authenticate(self):
        """
        Authenticate websockey connection to subscribe private topic.
        """
        expires = int(time.time())
        method = "GET"
        path = "/realtime"
        msg = method + path + str(expires)
        signature = hmac.new(
            self.secret, msg.encode(), digestmod=hashlib.sha256
        ).hexdigest()

        req = {"op": "authKey", "args": [self.key, expires, signature]}
        self.send_packet(req)

    def subscribe_topic(self):
        """
        Subscribe to all private topics.
        """
        req = {
            "op": "subscribe",
            "args": [
                "instrument",
                "trade",
                "orderBook10",
                "execution",
                "order",
                "position",
                "margin",
            ],
        }
        self.send_packet(req)

    def on_tick(self, d):
        """"""
        symbol = d["symbol"]
        tick = self.ticks.get(symbol, None)
        if not tick:
            return

        tick.last_price = d["price"]
        tick.datetime = datetime.strptime(
            d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.gateway.on_tick(copy(tick))

    def on_depth(self, d):
        """"""
        symbol = d["symbol"]
        tick = self.ticks.get(symbol, None)
        if not tick:
            return

        for n, buf in enumerate(d["bids"][:5]):
            price, volume = buf
            tick.__setattr__("bid_price_%s" % (n + 1), price)
            tick.__setattr__("bid_volume_%s" % (n + 1), volume)

        for n, buf in enumerate(d["asks"][:5]):
            price, volume = buf
            tick.__setattr__("ask_price_%s" % (n + 1), price)
            tick.__setattr__("ask_volume_%s" % (n + 1), volume)

        tick.datetime = datetime.strptime(
            d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.gateway.on_tick(copy(tick))

    def on_trade(self, d):
        """"""
        # Filter trade update with no trade volume and side (funding)
        if not d["lastQty"] or not d["side"]:
            return

        tradeid = d["execID"]
        if tradeid in self.trades:
            return
        self.trades.add(tradeid)

        if d["clOrdID"]:
            orderid = d["clOrdID"]
        else:
            orderid = d["orderID"]

        trade = TradeData(
            symbol=d["symbol"],
            exchange=Exchange.BITMEX,
            orderid=orderid,
            tradeid=tradeid,
            direction=DIRECTION_BITMEX2VT[d["side"]],
            price=d["lastPx"],
            volume=d["lastQty"],
            time=d["timestamp"][11:19],
            gateway_name=self.gateway_name,
        )

        self.gateway.on_trade(trade)

    def on_order(self, d):
        """"""
        if "ordStatus" not in d:
            return

        sysid = d["orderID"]
        order = self.orders.get(sysid, None)
        if not order:
            if d["clOrdID"]:
                orderid = d["clOrdID"]
            else:
                orderid = sysid

            # time = d["timestamp"][11:19]

            order = OrderData(
                symbol=d["symbol"],
                exchange=Exchange.BINANCE,
                orderid=orderid,
                direction=DIRECTION_BITMEX2VT[d["side"]],
                price=d["price"],
                volume=d["orderQty"],
                time=d["timestamp"][11:19],
                gateway_name=self.gateway_name,
            )
            self.orders[sysid] = order

        order.traded = d.get("cumQty", order.traded)
        order.status = STATUS_BITMEX2VT.get(d["ordStatus"], order.status)

        self.gateway.on_order(copy(order))

    def on_position(self, d):
        """"""
        position = PositionData(
            symbol=d["symbol"],
            exchange=Exchange.BINANCE,
            direction=Direction.NET,
            volume=d["currentQty"],
            gateway_name=self.gateway_name,
        )

        self.gateway.on_position(position)

    def on_account(self, d):
        """"""
        accountid = str(d["account"])
        account = self.accounts.get(accountid, None)
        if not account:
            account = AccountData(accountid=accountid,
                                  gateway_name=self.gateway_name)
            self.accounts[accountid] = account

        account.balance = d.get("marginBalance", account.balance)
        account.available = d.get("availableMargin", account.available)
        account.frozen = account.balance - account.available

        self.gateway.on_account(copy(account))

    def on_contract(self, d):
        """"""
        if "tickSize" not in d:
            return

        if not d["lotSize"]:
            return

        contract = ContractData(
            symbol=d["symbol"],
            exchange=Exchange.BINANCE,
            name=d["symbol"],
            product=Product.FUTURES,
            pricetick=d["tickSize"],
            size=d["lotSize"],
            gateway_name=self.gateway_name,
        )

        self.gateway.on_contract(contract)