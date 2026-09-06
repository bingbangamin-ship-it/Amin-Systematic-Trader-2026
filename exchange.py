import os,ccxt
class ExchangeGateway:
    def __init__(self,exchange_id="binance",sandbox=True):
        cls=getattr(ccxt,exchange_id)
        self.exchange=cls({"apiKey":os.getenv("EXCHANGE_API_KEY",""),
                           "secret":os.getenv("EXCHANGE_SECRET",""),
                           "enableRateLimit":True})
        if sandbox:
            try:self.exchange.set_sandbox_mode(True)
            except:pass
    def ticker(self,symbol):return self.exchange.fetch_ticker(symbol)
    def balance(self):return self.exchange.fetch_balance()
    def ohlcv(self,symbol,timeframe="1h",limit=500):return self.exchange.fetch_ohlcv(symbol,timeframe,limit=limit)
    def order(self,symbol,side,amount,paper=True):
        if paper:return {"paper":True,"symbol":symbol,"side":side,"amount":amount}
        return self.exchange.create_order(symbol,"market",side,amount)
