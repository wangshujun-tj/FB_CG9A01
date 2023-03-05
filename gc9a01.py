from time import sleep_ms
from ustruct import pack
from machine import SPI,Pin
from micropython import const
import framebuf


class GC9A01(framebuf.FrameBuffer):
    def __init__(self, width, height, spi, dc, rst, cs, rot=0, bgr=0):
        if dc is None:
            raise RuntimeError('LCD must be initialized with a dc pin number')
        dc.init(dc.OUT, value=0)
        if cs is None:
            raise RuntimeError('LCD must be initialized with a cs pin number')
        cs.init(cs.OUT, value=1)
        if rst is not None:
            rst.init(rst.OUT, value=1)
            self.rst = rst
        else:
            self.rst =None
        self.spi = spi
        self.dc = dc
        self.cs = cs
        self.rot = rot
        if self.rot==0 or self.rot==2:
            self.height = height
            self.width = width
        else:
            self.height = width
            self.width = height
        self.buffer = bytearray(self.height * self.width*2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565SW)
        self.reset() 
        #Bit D7- MY
        #Bit D6- MX
        #Bit D5- MV
        #Bit D4- ML
        #Bit D3- RGB/BGR Order
        #Bit D2- MH
        if rot==0:
            madctl=0xC0
        elif rot==1:
            madctl=0xA0
        elif rot==2:
            madctl=0x00
        elif rot==3:
            madctl=0x60
        if bgr==0:
            madctl|=0x08            
            
        self._write(0x11)
        sleep_ms(120)
        command =(
            (0x11,None),                 #Sleep out
            (0xEF,None),              
            (0xEB,b'\x14'),              #Interface pixel format
            (0xFE,None),              #Interface pixel format
            (0xEF,None),              #Interface pixel format
            (0xEB,b'\x14'),              #Interface pixel format
            (0x84,b'\x40'),
            (0x85,b'\xFF'),
            (0x86,b'\xFF'),
            (0x87,b'\xFF'),
            (0x88,b'\x0A'),
            (0x89,b'\x21'),
            (0x8A,b'\x00'),
            (0x8B,b'\x80'),
            (0x8C,b'\x01'),
            (0x8D,b'\x01'),
            (0x8E,b'\xFF'),
            (0x8F,b'\xFF'),
            (0xB6,b'\x00\x20'),
            (0x36,pack('>B', madctl)),   #Memory data access control
            (0x3A,b'\x05'),
            (0x90,b'\x08\x08\x08\x08'),
            (0xBD,b'\x06'),
            (0x8C,b'\x00'),
            (0xFF,b'\x60\x01\x04'),
            (0xC3,b'\x13'),
            (0xC4,b'\x13'),
            (0xBE,b'\x11'),
            (0xE1,b'\x10\x0E'),
            (0xDF,b'\x21\x0C\x02'),
            #f0-4SET_GAMMA
            (0xF0,b'\x45\x09\x08\x08\x26\x2A'),
            (0xF1,b'\x43\x70\x72\x36\x37\x6F'),
            (0xF2,b'\x45\x09\x08\x08\x26\x2A'),
            (0xF3,b'\x43\x70\x72\x36\x37\x6F'),
            (0xED,b'\x1B\x0B'),
            (0xAE,b'\x77'),
            (0xCD,b'\x63'),
            (0x70,b'\x07\x07\x04\x0E\x0F\x09\x07\x08\x03'),
            (0x62,b'\x18\x0D\x71\xED\x70\x70\x18\x0F\x71\xEF\x70\x70'),
            (0x63,b'\x18\x11\x71\xF1\x70\x70\x18\x13\x71\xF3\x70\x70'),
            (0x64,b'\x28\x29\xF1\x01\xF1\x00\x07'),
            (0x66,b'\x3C\x00\xCD\x67\x45\x45\x10\x00\x00\x00'),
            (0x67,b'\x00\x3C\x00\x00\x00\x01\x54\x10\x32\x98'),
            (0x74,b'\x10\x85\x80\x00\x00\x4E\x00'),
            (0x98,b'\x3E\x07'),
            (0x35,None),    #Tearing Effect Line on 
            (0x21,None),     #Display inversion on
            )
        for cmd,dat in command:
            self._write(cmd,dat)
        self.fill(0)
        self.show()
        sleep_ms(10)
        self._write(0x29,None)
        sleep_ms(10)
    def reset(self):
        if self.rst is None:
            self._write(0x01)
            sleep_ms(10)
            return
        self.rst.off()
        sleep_ms(10)
        self.rst.on()
        sleep_ms(10)
    def _write(self, command, data = None):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([command]))
        self.cs.on()
        if data is not None:
            self.cs.off()
            self.dc.on()
            self.spi.write(data)
            self.cs.on()
    def show(self):
        self._write(0x2A,pack(">HH", 0, 239))
        self._write(0x2B,pack(">HH", 0, 239))
        self._write(0x2C,self.buffer)

    def rgb(self,r,g,b):
        return ((r&0xf8)<<8)|((g&0xfc)<<3)|((b&0xf8)>>3)


        

        
