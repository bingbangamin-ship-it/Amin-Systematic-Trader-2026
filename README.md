# SYSTEMATIC TRADER PRO — FINAL

تم نهایی:
- Neon dark Android UI
- Dashboard
- 6 persistent motors
- Asset Registry
- P/L Center
- Technical Analysis: RSI, EMA20/50/200, volume
- Fundamental Analysis: TVL, revenue, users, developer activity, unlock pressure, concentration
- Combined scoring
- Backtest engine
- CCXT exchange gateway
- Paper/Sandbox first; Live locked by default

فرمول سرمایه:
300 = 100 L1 + 100 L2 + 100 L2/L3
Core=200
Principal -> Safe
Core profit -> Dark
Meme profit: 60% Safe + 40% Reinvest

APK:
cd mobile
buildozer -v android debug

نکته: این محیط Android SDK/NDK لازم برای تولید APK باینری را ندارد؛ فایل buildozer.spec آماده است.
برای بک‌تست معتبر باید داده OHLCV و Fundamental با timestamp تاریخی و بدون look-ahead وارد شود.

## Token Safety Gate
A read-only safety module has been added without changing the trading strategy. Endpoint: `POST /safety/scan`. It evaluates supplied/provider data for honeypot signals, buy/sell tax, liquidity, liquidity lock, holder concentration, owner status, blacklist/mint functions and proxy contracts. A score below 80 or a critical honeypot/blacklist signal blocks the safety verdict.

Example payload:
```json
{"chain":"bsc","address":"0x...","symbol":"TOKEN","data":{"honeypot":false,"sell_tax_pct":5,"liquidity_usd":50000,"liquidity_locked":true,"top_holders_pct":35}}
```
