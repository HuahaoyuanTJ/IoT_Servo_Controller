import network
import time
import urequests
import ujson
import sys
from machine import Pin, PWM


temperature = ""
Id = ""
name = ""
state = ""
valid = ""
pwm5 = PWM(Pin(14))      # create PWM object from a pin
pwm5.freq(50)
s1 = 180 #67-180
s2 = 67
'''
那么公式为
c / 180（最大角度） * 2（0°-180°高电平脉冲宽度） + 0.5（舵机角度0°时高电平脉冲宽度）/ 20ms(脉冲周期) * 1023
'''
up = int((s1 / 180 * 2 + 0.5) / 20 * 1023)
down = int((s2 / 180 * 2 + 0.5) / 20 * 1023)





def do_connect():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    s = sta_if.config('mac')
    mymac = ('%02x-%02x-%02x-%02x-%02x-%02x') %(s[0],s[1],s[2],s[3],s[4],s[5])
    print(mymac)
    sta_if.connect('ASK4 Wireless at Novel', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
        print(" Connected!")
        
def to_activate():
    while 1:
      re = urequests.get('http://47.94.221.76:8090/selectById?Id=001')
      print(str(re.text))
      res = re.json()
      valid = res[0]["valid"]
      print("valid："+ valid)
      re.close()
      if valid == "1":
          check_update():
          break;
      elif valid == "0":
          print("keep off")
          time.sleep(60)


def check_update():
  drive_servo()
  for i in range(0,110):
      re = urequests.get('http://47.94.221.76:8090/selectById?Id=001')
      print(str(re.text))
      res = re.json()
      valid = res[0]["valid"]
      print("valid："+ valid)
      re.close()
      if valid == "1":
          print("ON DUTY")
      elif valid == "F":
          print("valid："+ valid)
          print("用户未授权或授权失效")
          sys.exit(0)
      elif valid == "0":
          print("OFF DUTY")
          if i>60:
              drive_servo()
              time.sleep(10)
              drive_servo()
          elif i==0:
              print("off")
          else:
              drive_servo()
          to_activate()
      time.sleep(60)
          
    
def drive_servo():
    pwm5.duty(up)
    time.sleep(1)
    pwm5.duty(down)
    time.sleep(0.3)
    pwm5.duty(up)
    time.sleep(1)
    pwm5.duty(down)
    time.sleep(0.3)
    pwm5.duty(up)
    



do_connect()
while True:
  check_update()
