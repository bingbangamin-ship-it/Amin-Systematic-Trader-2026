
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem
API="http://127.0.0.1:8000"

class UI(TabbedPanel):
    def __init__(self,**kw):
        super().__init__(do_default_tab=False,**kw)
        for title,fn in [("◉ DASH",self.dash),("⚡ MOTORS",self.motors),
                         ("◇ ASSETS",self.assets),("⌁ P/L",self.pnl),
                         ("◈ ANALYSIS",self.analysis),("⇄ EXCHANGE",self.exchange),
                         ("◈ BACKTEST",self.backtest), ("★ COMMAND",self.command_tab)]:
            tab=TabbedPanelItem(text=title); box=BoxLayout(orientation="vertical",padding=12,spacing=8)
            if title == "★ COMMAND":
                self.command_panel(box)
            else:
                lab=Label(text=fn(),font_size=17);box.add_widget(lab)
                btn=Button(text="⟳ REFRESH",size_hint_y=.10)
                btn.bind(on_press=lambda *_ ,l=lab,f=fn:setattr(l,"text",f()))
                box.add_widget(btn)
            tab.add_widget(box);self.add_widget(tab)
    def get(self,path):
        try:return requests.get(API+path,timeout=3).json()
        except:return None
    def dash(self):
        d=self.get("/status")
        return "SYSTEMATIC TRADER PRO\n\nTOTAL EQUITY\n$"+f"{d['equity']:,.2f}" if d else "SYSTEM OFFLINE"
    def motors(self):
        d=self.get("/status")
        return "\n\n".join(f"MOTOR {m['id']}  ${m['equity']:,.2f}\nL1 ${m['l1']:,.2f} | L2 ${m['l2']:,.2f} | L2/L3 ${m['l2_l3']:,.2f}\nSAFE ${m['safe']:,.2f} | DARK ${m['dark']:,.2f}" for m in d["motors"]) if d else "OFFLINE"
    def assets(self):
        d=self.get("/assets")
        if not d:return "ASSET REGISTRY OFFLINE"
        return f"ASSETS: {d['count']}\n\n"+"\n".join(f"{a['symbol']} | {a['layer']} | M{a['motor']} | {a['status']}" for a in d["assets"])
    def pnl(self):
        d=self.get("/pnl")
        return f"P/L CENTER\n\nTOTAL P/L ${d['total_pnl']:,.2f}\n\n"+"\n".join(f"{a['symbol']}: {a['pnl_pct']:+.2f}%" for a in d["assets"]) if d else "P/L OFFLINE"
    def analysis(self):
        return "ANALYSIS CENTER\n\nTECHNICAL: RSI • EMA20/50/200 • Volume\nFUNDAMENTAL: TVL • Revenue • Users • Developers • Unlocks • Concentration\n\nCombined score = 55% Technical + 45% Fundamental\n\nOnly timestamp-aligned historical data is valid for backtests."
    def exchange(self):return "EXCHANGE CENTER\n\n● PAPER\n● SANDBOX\n○ LIVE LOCKED\n\nCCXT gateway • server-side API secrets"
    def command_tab(self):
        return "USER COMMAND PRIORITY\n\nAny command you send is marked USER_OVERRIDE and takes priority over automated decisions."
    def command_panel(self, box):
        status=Label(text=self.command_status(),font_size=15,size_hint_y=.35)
        inp=TextInput(hint_text="Type your command for the bot...",multiline=True,size_hint_y=.35)
        send=Button(text="SEND USER PRIORITY COMMAND",size_hint_y=.15)
        clear=Button(text="CLEAR OVERRIDE / RETURN TO AUTOMATION",size_hint_y=.15)
        def submit(*_):
            try:
                r=requests.post(API+"/command",json={"command":inp.text},timeout=3).json()
                status.text="USER OVERRIDE ACTIVE\n\n"+r.get("command","")
            except Exception:
                status.text="COMMAND SERVER OFFLINE"
        def reset(*_):
            try:
                requests.post(API+"/command/clear",timeout=3)
                status.text="AUTOMATION MODE ACTIVE"
                inp.text=""
            except Exception:
                status.text="COMMAND SERVER OFFLINE"
        send.bind(on_press=submit); clear.bind(on_press=reset)
        for w in (status,inp,send,clear): box.add_widget(w)
    def command_status(self):
        d=self.get("/command")
        if not d:return "COMMAND SERVER OFFLINE"
        return ("USER OVERRIDE ACTIVE\n\n"+d.get("command","")) if d.get("active") else "AUTOMATION MODE ACTIVE"

    def backtest(self):return "BACKTEST LAB\n\n3-year OHLCV pipeline + timestamp-aligned fundamentals\nFees + slippage + drawdown + equity curve\n\nRun backend backtest with your historical dataset."

class TraderApp(App):
    def build(self):return UI()
if __name__=="__main__":TraderApp().run()
