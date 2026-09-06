
from dataclasses import dataclass,asdict
from typing import Optional

@dataclass
class Asset:
    symbol:str
    layer:str
    motor:int
    chain:str
    entry:float=0
    current:float=0
    invested:float=0
    fundamental:float=0
    technical:float=0
    liquidity_usd:float=0
    status:str="WATCH"
    @property
    def pnl(self): return (self.current-self.entry)/self.entry*self.invested if self.entry else 0
    @property
    def pnl_pct(self): return (self.current/self.entry-1)*100 if self.entry else 0
    def json(self):
        d=asdict(self);d.update(pnl=self.pnl,pnl_pct=self.pnl_pct);return d

ASSETS=[]
