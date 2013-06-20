#!/usr/bin/env python

# Test code for Adafruit LED Pixels, uses hardware SPI

import RPi.GPIO as GPIO, time, os, datetime

DEBUG = 1
GPIO.setmode(GPIO.BCM)

def slowspiwrite(clockpin, datapin, byteout):
	GPIO.setup(clockpin, GPIO.OUT)
	GPIO.setup(datapin, GPIO.OUT)
	for i in range(8):
		if (byteout & 0x80):
			GPIO.output(datapin, True)
		else:
			GPIO.output(clockpin, False)
		byteout <<= 1
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)


SPICLK = 18
SPIDO = 17

ledpixels = [0] * 60

def writestrip(pixels):
	spidev = file("/dev/spidev0.0", "w")
	for i in range(len(pixels)):
		spidev.write(chr((pixels[i]>>16) & 0xFF))
		spidev.write(chr((pixels[i]>>8) & 0xFF))
		spidev.write(chr(pixels[i] & 0xFF))
	spidev.close()
	time.sleep(0.002)

def Color(r, g, b):
	return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def setpixelcolor(pixels, n, r, g, b):
	if (n >= len(pixels)):
		return
	pixels[n] = Color(r,g,b)

def setpixelcolor(pixels, n, c):
	if (n >= len(pixels)):
		return
	pixels[n] = c

def colorwipe(pixels, c, delay):
	for i in range(len(pixels)):
		setpixelcolor(pixels, i, c)
		writestrip(pixels)
		time.sleep(delay)		

def Wheel(WheelPos):
	if (WheelPos < 85):
   		return Color(WheelPos * 3, 255 - WheelPos * 3, 0)
	elif (WheelPos < 170):
   		WheelPos -= 85;
   		return Color(255 - WheelPos * 3, 0, WheelPos * 3)
	else:
		WheelPos -= 170;
		return Color(0, WheelPos * 3, 255 - WheelPos * 3)

def rainbowCycle(pixels, wait):
	for j in range(256): # one cycle of all 256 colors in the wheel
    	   for i in range(len(pixels)):
# tricky math! we use each pixel as a fraction of the full 96-color wheel
# (thats the i / strip.numPixels() part)
# Then add in j which makes the colors go around per pixel
# the % 96 is to make the wheel cycle around
      		setpixelcolor(pixels, i, Wheel( ((i * 256 / len(pixels)) + j) % 256) )
	   writestrip(pixels)
	   time.sleep(wait)

def clockdraw(pixels):
	hour = 60 / int(time.strftime('%l'))
	minute = int(time.strftime('%M'))
	second = int(time.strftime('%S'))
	one = 1
	quarter = 16
	half = 31
	threequarter = 46

        for i in range(len(pixels)):
        	
		c = Color(0,0,0)

		if i == one or i == quarter or i == half or i == threequarter:
			c = Color(0,0,255)
		if i == hour:
			c = Color(255,0,0)
		if i == minute:
			c = Color(255,0,255)
		if i == second:
			c = Color(255,255,255)

	
		setpixelcolor(pixels, i, c)


	#setpixelcolor(pixels, random.randint(0,len(pixels)), Color(r,g,b))
	writestrip(pixels)
	time.sleep(1)
	print(time.strftime('%l:%M%S'))


while True:	
	clockdraw(ledpixels)
