
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from .capital_engine import Ledger
from .exchange import ExchangeGateway
from .assets import ASSETS
app=FastAPI(title="Systematic Trader Pro Final")
ledger=Ledger()

@app.get("/status")
def status():
    return {"equity":ledger.equity,"cash":ledger.cash,"paper":True,
            "motors":[m.__dict__|{"equity":m.equity} for m in ledger.motors]}

@app.get("/assets")
def assets():
    return {"count":len(ASSETS),"assets":[a.json() for a in ASSETS]}

@app.get("/pnl")
def pnl():
    rows=[a.json() for a in ASSETS]
    return {"total_pnl":sum(x["pnl"] for x in rows),"assets":rows}

@app.post("/motor/{mid}/core-close")
def core(mid:int,l2_end:float,l2l3_end:float):return ledger.core_close(mid,l2_end,l2l3_end)

@app.post("/motor/{mid}/meme-split")
def meme(mid:int,start:float,end:float):return ledger.meme_split(mid,start,end)

@app.post("/motor/create")
def create():return {"created":ledger.create_motor(),"count":len(ledger.motors)}

class Req(BaseModel):
    exchange:str="binance";symbol:str="BTC/USDT"

@app.post("/market/ticker")
def ticker(r:Req):
    try:return ExchangeGateway(r.exchange,True).ticker(r.symbol)
    except Exception as e:raise HTTPException(400,str(e))

# User-command priority layer: explicit user commands override automated decisions.
class UserCommand(BaseModel):
    command: str
    priority: str = "USER_OVERRIDE"

user_override = {"active": False, "command": "", "priority": "AUTOMATION", "history": []}

@app.post("/command")
def set_user_command(r: UserCommand):
    cmd = r.command.strip()
    if not cmd:
        raise HTTPException(400, "Command cannot be empty")
    user_override["active"] = True
    user_override["command"] = cmd
    user_override["priority"] = "USER_OVERRIDE"
    user_override["history"].append(cmd)
    user_override["history"] = user_override["history"][-20:]
    return {"ok": True, **user_override}

@app.post("/command/clear")
def clear_user_command():
    user_override["active"] = False
    user_override["command"] = ""
    user_override["priority"] = "AUTOMATION"
    return {"ok": True, **user_override}

@app.get("/command")
def get_user_command():
    return user_override

# ---------------- TOKEN SAFETY GATE (read-only, does not alter strategy) ----------------
from typing import Optional, Dict, Any
from .token_safety import scan

class SafetyRequest(BaseModel):
    chain: str
    address: str
    symbol: str = ""
    # Optional provider results. A future provider adapter can populate these automatically.
    data: Dict[str, Any] = {}

@app.post('/safety/scan')
def safety_scan(r: SafetyRequest):
    return scan(r.chain, r.address, r.symbol, r.data).json()

@app.get('/safety/health')
def safety_health():
    return {'scanner':'TOKEN_SAFETY_GATE','version':'1.0','strategy_modified':False,
            'checks':['honeypot','buy_sell_tax','liquidity','liquidity_lock','holder_concentration','owner','blacklist','mint','proxy']}
