#!/usr/bin/env python

import RPi.GPIO as GPIO

import json, urllib, urllib2, time, os, datetime
from bs4 import BeautifulSoup
import reports
import cPickle as pickle

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File
import cgi

import socket

count = 0
conn = 0
addr = 0
BULB = 0
MODE = 0
BRIGHT = 100
STROBE = 50
DEBUG = 1
GPIO.setmode(GPIO.BCM)
power_pin = 17
GPIO.setup(power_pin, GPIO.OUT)

class lampAPI(Resource):
	def render_GET(self, request):
		global MODE
		global BULB
		global conn
		global addr
		global count
		if 'light' in request.args:
			if request.args['light'][0] == "off":
				GPIO.output(power_pin, False)
				BULB = 0
				return "<html> light off </html>"
			if request.args['light'][0] == "on":
				BULB = 1
				GPIO.output(power_pin, True)
				return "<html> light on </html>"
			if request.args['light'][0] == "toggle":
				if BULB == 1:
					BULB = 0
					GPIO.output(power_pin, False)
					return "<html> light off </html>"
				elif BULB == 0:
					BULB = 1
					GPIO.output(power_pin, True)
					return "<html> light on </html>"								

		elif 'mode' in request.args:
			count = 0
			if request.args['mode'][0] == "-1":
				MODE = -1
				return "<html> mode set to -1 </html>"
			if request.args['mode'][0] == "0":
				colorwipe(ledpixels, Color(0, 0, 0), 0)
				MODE = 0
				return "<html> mode set to 0 </html>"
			if request.args['mode'][0] == "1":
				MODE = 1
				return "<html> mode set to 1 </html>"
			if request.args['mode'][0] == "2":
				MODE = 2
				return "<html> mode set to 2 </html>"
			if request.args['mode'][0] == "3":
				colorwipe(ledpixels, Color(0, 0, 0), 0)
				MODE = 3
				return "<html> mode set to 3 </html>"
			if request.args['mode'][0] == "4":
				colorwipe(ledpixels, Color(0, 0, 0), 0)
				MODE = 4
				return "<html> mode set to 4 </html>"

		elif 'status' in request.args:
			if request.args['status'][0] == "1":
				return getStatus()

def getStatus():
	global MODE
	global BULB
	global STROBE
	global BRIGHT

	jsonString = ''
	jsonString += '{"lamp":{"bulb":'
	jsonString += str(BULB)
	jsonString += ',"strobefreq":'
	jsonString += str(STROBE)
	jsonString += ',"mode":'
	jsonString += str(MODE)
	jsonString += ',"brightness":'
	jsonString += str(BRIGHT)
	jsonString += '}}'
	#print jsonString
	return jsonString

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

		c = Color(0,10,10)

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
	#print(time.strftime('%l:%M%S'))

def infodisplay(pixels):
	infostring_delimiter = Color(4,4,4)

	#pixels 1-11
	#Surf report
	surf_offset = 2
	surf_color_array = [ Color(0,0,4), Color(0,4,2), Color(4,4,0), Color(4,2,0) ]
	#surf_report_array = surf_report()
	try:
		surf_report_array = pickle.load( open( "surf.p", "rb" ) )
		setpixelcolor(pixels, surf_offset - 1, infostring_delimiter)
		for i in range(len(surf_report_array)):
			setpixelcolor(pixels, i + surf_offset, surf_color_array[ surf_report_array[i] ])
	except Exception:
		pass

        #pixels 15-25
        #Weather report
        weather_offset = 17
        weather_color_array = [ Color(0,4,4), Color(0,0,4), Color(4,4,0), Color(4,4,4) ]
        #weather_report_array = weather_report()
	try:
		weather_report_array = pickle.load( open( "weather.p", "rb" ) )
		setpixelcolor(pixels, weather_offset - 1, infostring_delimiter)
	        for i in range(len(weather_report_array)):
        	        setpixelcolor(pixels, i + weather_offset, weather_color_array[ weather_report_array[i] ])
	except Exception:
		pass

	#pixels 30-40
        #micasa report
        micasa_offset = 32
        micasa_color_array = [ Color(4,0,4), Color(0,0,4), Color(0,4,0), Color(4,0,0) ]
	try:
	        micasa_report_array = reports.micasa_report()
		setpixelcolor(pixels, micasa_offset - 1, infostring_delimiter)
		for i in range(len(micasa_report_array)):
			setpixelcolor(pixels, i + micasa_offset, micasa_color_array[ micasa_report_array[i] ])
	except Exception:
		pass	

	writestrip(pixels)
	time.sleep(0.2)

def rainSim(pixels):
	global count	

	if count == 0:
		for i in range(len(pixels)):
			setpixelcolor(pixels, i, Color(0,0,0))
	elif count == 1:
		for i in range(len(pixels)):
			setpixelcolor(pixels, i, Color(255,255,255))
		count = -1

	writestrip(pixels)
	time.sleep(0.03)
	count += 1

def datastream(pixels):
	global MODE

	print "waiting for connec" + str(MODE)

	HOST = ''                 # Symbolic name meaning the local host
	PORT = 50007              # Arbitrary non-privileged port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	conn, addr = s.accept()

	while(1):
		try:
			data = conn.recv(1024)
		except Exception:
			colorwipe(ledpixels, Color(0, 0, 0), 0)
			MODE = 0
			print "Client left" + str(MODE)
			break
			#conn, addr = s.accept()
		LVarray = data.split(',')
		#print LVarray
		count = 0
	        for i in range(len(pixels)):
			try:
				setpixelcolor(pixels, i, Color(int(LVarray[count]), int(LVarray[count + 1]), int(LVarray[count +2])) )
			except Exception:
				setpixelcolor(pixels, i, Color(0,0,0) )
			#print LVarray[count]+ ":" +LVarray[count + 1]+ ":" +LVarray[count +2]+ " | "
			#setpixelcolor(pixels, i, Color(244,0,244) )
			count += 3

		writestrip(pixels)

#root = Resource()
root = File("lampwww")
#root.putChild("", File("lampwww"))
root.putChild("API", lampAPI())

factory = Site(root)
reactor.listenTCP(80, factory)
reactor.startRunning(False)

while True:
        reactor.iterate()
	if MODE == -1:
		datastream(ledpixels)
	if MODE == 1:
		rainSim(ledpixels)
	if MODE == 2:
		clockdraw(ledpixels)
	if MODE == 3:
		rainbowCycle(ledpixels, 0.00)
	if MODE == 4:
		infodisplay(ledpixels)

