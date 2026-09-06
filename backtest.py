import pandas as pd
from .strategy import technical_score,combined_score

def run(path,symbol="UNKNOWN",starting=300):
    df=pd.read_csv(path,parse_dates=["timestamp"]).sort_values("timestamp")
    curve=[];equity=starting;peak=starting;dd=0
    for i in range(200,len(df)):
        h=df.iloc[:i+1]
        t=technical_score(h)
        f=0
        score=combined_score(t,f)
        curve.append({"timestamp":h.timestamp.iloc[-1],"equity":equity,"technical":t,"fundamental":f,"combined":score})
        peak=max(peak,equity);dd=max(dd,(peak-equity)/peak)
    out=pd.DataFrame(curve);out.to_csv("backtest_curve.csv",index=False)
    return {"start":starting,"end":equity,"return_pct":0,"max_drawdown_pct":dd*100,"rows":len(out)}
