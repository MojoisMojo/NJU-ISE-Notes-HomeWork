from typing import List
from math import gcd
import sys

SLOW_START,CONG_AVOID,FAST_RECOVERY = 0,1,2
time = 0
STEP_TIME = 1
class Host: pass
class Channel: pass
class Message: pass

class Host:
    def __init__(self,name:str,cwnd:int,state:int,interval:int,channel: Channel):
        self.cwnd,self.state,self.interval = cwnd,state,interval
        self.channel:Channel = channel
        self.name = name
    def messageArrive(self,msg: Message):
        if(self.state != CONG_AVOID): return # TBC
        if(msg.is_dropped):
            self.cwnd = max(1,self.cwnd // 2)
        else:
            self.cwnd += 1
        self.sendMessage()
    def sendMessage(self):
        msg = Message(self.cwnd,self.interval,self)
        print("a message sent: ({})".format(msg),end="; ")
        channel.addMsg(msg)

class Message:
    def __init__(self, size:int, left_time: int, host: Host):
        self.size,self.left_time = size,left_time
        self.host:Host = host
        self.rate = 1000 * self.size / self.host.interval
        self.is_dropped = False
    def update(self):
        self.left_time -= STEP_TIME
    def Cong(self):
        self.is_dropped = True
    def __repr__(self) -> str:
        return "size:{},rate:{},host:{}".format(self.size,self.rate,self.host.name)

class Channel:
    def __init__(self,max_rate:float,curr_msg:List[Message]=[]):
        self.max_rate = max_rate
        self.curr_msgs:List[Message] = curr_msg
    def update(self):
        if self.isCong():
            for msg in self.curr_msgs: msg.Cong()
        tmp = self.curr_msgs
        self.curr_msgs:List[Message] = []
        for msg in tmp:
            msg.update()
            if(msg.left_time <= 0): msg.host.messageArrive(msg)
            else: self.trasportMsg(msg)
    def isCong(self)->bool:
        return sum(msg.rate for msg in self.curr_msgs) > self.max_rate
    def trasportMsg(self,msg: Message):
        self.curr_msgs.append(msg)
    def addMsg(self,msg:Message):
        self.curr_msgs.append(msg)
if __name__ == "__main__":
    f = open("output.txt", "w")
    sys.stdout = f
    channel = Channel(30)
    c1,c2 = Host("C1",10,CONG_AVOID,50,channel),Host("C2",10,CONG_AVOID,100,channel)
    STEP_TIME = gcd(c1.interval,c2.interval)
    print("------------time {}-----------".format(time))
    c1.sendMessage()
    c2.sendMessage()
    print("")
    time += STEP_TIME
    while time <= 1000:
        print("------------time {}-----------".format(time))
        channel.update()
        time += STEP_TIME
        print("")
    f.close()