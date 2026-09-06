
import pandas as pd
import numpy as np

def rsi(close,n=14):
    d=close.diff(); g=d.clip(lower=0).rolling(n).mean()
    l=(-d.clip(upper=0)).rolling(n).mean()
    return 100-100/(1+g/l.replace(0,np.nan))

def technical_analysis(df):
    c=df["close"]
    e20=c.ewm(span=20,adjust=False).mean().iloc[-1]
    e50=c.ewm(span=50,adjust=False).mean().iloc[-1]
    e200=c.ewm(span=200,adjust=False).mean().iloc[-1]
    rr=float(rsi(c).iloc[-1])
    av=df["volume"].rolling(20).mean().iloc[-1]
    price=float(c.iloc[-1])
    volume_ratio=float(df["volume"].iloc[-1]/max(av,1e-12))
    score=(
        20*(price>e20)+20*(e20>e50)+20*(e50>e200)+
        20*(50<=rr<=68)+20*(volume_ratio>1.2)
    )
    return {
        "score":float(score),"price":price,"rsi":rr,
        "ema20":float(e20),"ema50":float(e50),"ema200":float(e200),
        "volume_ratio":volume_ratio
    }

def fundamental_score(record):
    """
    Expected time-aligned fields:
    market_cap, volume_24h, tvl, revenue, active_users,
    developer_activity, token_unlock_pressure, concentration_risk.
    Missing fields are neutral, not invented.
    """
    weights={
        "market_cap":.12,"volume_24h":.10,"tvl":.18,"revenue":.15,
        "active_users":.12,"developer_activity":.15,
        "token_unlock_pressure":-.09,"concentration_risk":-.09
    }
    vals=[]
    for k,w in weights.items():
        v=record.get(k)
        if v is not None:
            vals.append((float(v),w))
    if not vals:return 0.0
    # Inputs are assumed pre-normalized to 0..100 by the data pipeline.
    return max(0,min(100,sum(v*w for v,w in vals)/sum(abs(w) for _,w in vals)*1.0))

def combined_score(technical,fundamental,tw=.55):
    return tw*technical+(1-tw)*fundamental
