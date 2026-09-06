from dataclasses import dataclass,field
from .config import *

@dataclass
class Motor:
    id:int
    l1:float=100
    l2:float=100
    l2_l3:float=100
    safe:float=0
    dark:float=0
    dark_reinvest:float=0
    core_profit:float=0
    meme_profit:float=0
    active:bool=True
    @property
    def equity(self):
        return self.l1+self.l2+self.l2_l3+self.safe+self.dark

@dataclass
class Ledger:
    motors:list=field(default_factory=lambda:[Motor(1)])
    cash:float=0
    @property
    def equity(self):
        return self.cash+sum(m.equity for m in self.motors)
    def core_close(self,motor_id,l2_end,l2l3_end):
        m=self.motors[motor_id-1]
        value=max(0,l2_end)+max(0,l2l3_end)
        safe=min(200,value); profit=max(0,value-200)
        m.l2=m.l2_l3=0
        m.safe+=safe; m.dark+=profit; m.core_profit+=profit
        return {"safe":safe,"dark_profit":profit}
    def meme_split(self,motor_id,start,end):
        m=self.motors[motor_id-1]; profit=end-start
        if profit<=0:
            m.dark=max(0,end); return {"profit":profit,"safe":0,"reinvest":0}
        safe=profit*.60; reinvest=profit*.40
        m.safe+=safe; m.dark=reinvest; m.dark_reinvest+=reinvest; m.meme_profit+=profit
        return {"profit":profit,"safe":safe,"reinvest":reinvest}
    def create_motor(self):
        if len(self.motors)>=6 or self.cash<300:return False
        self.cash-=300; self.motors.append(Motor(len(self.motors)+1)); return True
