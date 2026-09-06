"""Token safety gate. Read-only scanner; it never changes trading strategy."""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List
import time

@dataclass
class SafetyReport:
    chain: str
    address: str
    symbol: str = ""
    safety_score: float = 0.0
    verdict: str = "UNKNOWN"
    trade_allowed: bool = False
    honeypot_risk: str = "UNKNOWN"
    sell_tax_pct: Optional[float] = None
    buy_tax_pct: Optional[float] = None
    liquidity_usd: Optional[float] = None
    liquidity_locked: Optional[bool] = None
    lock_duration_days: Optional[int] = None
    top_holders_pct: Optional[float] = None
    owner_renounced: Optional[bool] = None
    blacklist_function: Optional[bool] = None
    mint_function: Optional[bool] = None
    proxy_contract: Optional[bool] = None
    warnings: List[str] = None
    checked_at: int = 0

    def json(self): return asdict(self)

def _risk_score(data: Dict[str, Any]):
    score = 100.0; warnings=[]
    def val(k): return data.get(k)
    if val('honeypot') is True: score -= 100; warnings.append('HONEYPOT_RISK')
    for key,label,penalty in [('sell_tax_pct','HIGH_SELL_TAX',1.2),('buy_tax_pct','HIGH_BUY_TAX',0.8)]:
        x=val(key)
        if x is not None and float(x)>10: score-=min(30,float(x)*penalty); warnings.append(label)
    liq=val('liquidity_usd')
    if liq is not None and float(liq)<10000: score-=25; warnings.append('LOW_LIQUIDITY')
    if val('liquidity_locked') is False: score-=20; warnings.append('LIQUIDITY_NOT_LOCKED')
    th=val('top_holders_pct')
    if th is not None and float(th)>50: score-=25; warnings.append('HIGH_HOLDER_CONCENTRATION')
    if val('blacklist_function') is True: score-=25; warnings.append('BLACKLIST_FUNCTION_PRESENT')
    if val('mint_function') is True: score-=15; warnings.append('MINT_FUNCTION_PRESENT')
    if val('owner_renounced') is False: score-=8; warnings.append('OWNER_NOT_RENOUNCED')
    if val('proxy_contract') is True: score-=5; warnings.append('PROXY_CONTRACT')
    score=max(0,min(100,score))
    if val('honeypot') is True: verdict='BLOCKED'
    elif score>=85: verdict='LOW_RISK'
    elif score>=65: verdict='CAUTION'
    else: verdict='HIGH_RISK'
    allowed=score>=80 and val('honeypot') is not True and val('blacklist_function') is not True
    return score,verdict,allowed,warnings

def scan(chain:str,address:str,symbol:str='',data:Optional[Dict[str,Any]]=None):
    data=data or {}
    score,verdict,allowed,warnings=_risk_score(data)
    return SafetyReport(chain=chain,address=address,symbol=symbol,safety_score=score,verdict=verdict,trade_allowed=allowed,
        honeypot_risk='HIGH' if data.get('honeypot') is True else ('LOW' if data.get('honeypot') is False else 'UNKNOWN'),
        sell_tax_pct=data.get('sell_tax_pct'),buy_tax_pct=data.get('buy_tax_pct'),liquidity_usd=data.get('liquidity_usd'),
        liquidity_locked=data.get('liquidity_locked'),lock_duration_days=data.get('lock_duration_days'),top_holders_pct=data.get('top_holders_pct'),
        owner_renounced=data.get('owner_renounced'),blacklist_function=data.get('blacklist_function'),mint_function=data.get('mint_function'),proxy_contract=data.get('proxy_contract'),warnings=warnings,checked_at=int(time.time()))
