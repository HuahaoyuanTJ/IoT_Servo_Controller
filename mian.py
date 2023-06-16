from machine import Pin, PWM
import time


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
 
# 输出
while(1):
    pwm5.duty(up)
    time.sleep(1)
    pwm5.duty(down)
    time.sleep(0.3)
    pwm5.duty(up)
    time.sleep(1)
    pwm5.duty(down)
    time.sleep(0.3)
    pwm5.duty(up)
    for i in range(0,110):
        time.sleep(60)
    


