import time
from machine import Pin, SPI
spi = SPI(2,30000000, sck=Pin(32), mosi=Pin(33), miso=Pin(35))
from gc9a01 import GC9A01
#lcd = ST7789(135, 240, spi,dc=Pin(25),cs=Pin(32),rst=Pin(33),rot=0,bgr=0)#横屏初始化
lcd = GC9A01(240, 240, spi, dc=Pin(26),cs=Pin(27),rst=Pin(25), rot=3, bgr=0)#横屏初始化
#bl=Pin(27,Pin.OUT)
#bl.value(1)
lcd.font_load("GB2312-24.fon")
#加载的字库是中文，可以选12，16，24，32四种中文
for count in range(20):
    lcd.fill(lcd.rgb(0,0,0))
    lcd.font_set(0x11,0,1,0)
    #字体(第一位1-4对应标准，方头，不等宽标准，不等宽方头，第二位1-4对应12，16，24，32高度)，旋转，放大倍数，反白显示
    lcd.text("Micro python中文甒甒%d"%count,0,0,lcd.rgb(255,0,0))
    lcd.font_set(0x12,0,1,1)
    lcd.text("micro拷贝甓甓",0,16,lcd.rgb(0,255,0))
    lcd.font_set(0x13,0,1,0)
    lcd.text("字符Mpy%3.3d"%count,0,32,lcd.rgb(255,255,255))
    #lcd.rgb()是方便设置显示颜色的小功能
    lcd.font_set(0x44,0,1,0)
    lcd.text("中文Mpy%3.3d"%count,0,48,lcd.rgb(0,0,255))
    lcd.font_set(0x44,0,1,0)
    lcd.text("中文Mpy%3.3d"%count,0,120,lcd.rgb(0,0,255))
    lcd.show()
lcd.fill(lcd.rgb(0,0,0))
lcd.show_bmp("logo-172.bmp",0,34,34) 
lcd.show()
lcd.save_bmp("1.bmp")
lcd.fill(lcd.rgb(0,0,0))
lcd.line(0,0,160,80,lcd.rgb(255,0,0))
lcd.line(0,0,160,80,lcd.rgb(255,0,0))
b=lcd.ToGBK("Micro python中文甒甒")
print(b)
lcd.ellipse(80,40,20,10,lcd.rgb(0,255,0))
import math
import array

for a in range(120):
    ll=array.array("h")
    lcd.fill(lcd.rgb(0,0,0))
    t=6
    for i in range(t*2):
        if i%2==0:
            l=60
        else:
            l=29
        ll.append(int(math.cos(math.pi/36*a+math.pi*2*i/(t*2))*l))
        ll.append(int(math.sin(math.pi/36*a+math.pi*2*i/(t*2))*l))
    lcd.poly(lcd.width//2,lcd.height//2,ll,lcd.rgb(0,0,255),1)
    lcd.show()
ll=array.array("b")
for i in range(640):
    ll.append(int(math.sin(math.pi*8*(i+a)/160)*127))
for a in range(100):
    lcd.fill(lcd.rgb(0,0,0))
    lcd.curve(ll[a:a+lcd.width-1],1,lcd.rgb(0,0,255),0,lcd.height//2,2)
    lcd.curve(ll[a+10:a+lcd.width-1+10],1,lcd.rgb(0,255,255),0,lcd.height//2,2)
    lcd.show()
lcd.font_free()
