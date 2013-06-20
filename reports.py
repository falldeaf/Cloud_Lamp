from bs4 import BeautifulSoup
import json
import urllib
import urllib2
import imaplib, re

def surf_report():
	wave_list = []

	url = 'http://magicseaweed.com/syndicate/index.php?action=content&licenseKey=1366048199_83523'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	values = {'name' : 'Michael Foord',
	          'location' : 'Northampton',
	          'language' : 'Python' }
	headers = { 'User-Agent' : user_agent }

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = response.read()

	soup = BeautifulSoup(the_page)

	table = soup.find('table', id='forecastDay')

	colnum = 0
	rows = table.findAll('tr')
	for tr in rows:
		cols = tr.findAll('td')
		for td in cols:
			if colnum >= 2 and td.find('span') is not None:
				if float( td.find('span').find(text=True) ) <= 1:
					wave_list.append( 0 )
				elif float( td.find('span').find(text=True) ) <= 3:
					wave_list.append( 1 )
				elif float( td.find('span').find(text=True) ) <= 6:
                                        wave_list.append( 2 )
				else:
                                        wave_list.append( 3 )
				break
			colnum += 1
		colnum = 0
	return wave_list

#import json, urllib, urllib2

def weather_report():

	weather_list = []

	#data_string = json.load(open('Port_St_Lucie.json', 'r'))

	url = 'http://api.wunderground.com/api/66bfd98a36225d8f/forecast10day/q/FL/Port_St_Lucie.json'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	values = {'name' : 'Michael Foord',
	          'location' : 'Northampton',
	          'language' : 'Python' }
	headers = { 'User-Agent' : user_agent }

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = response.read()
	
	#print the_page

	data_string = json.loads(the_page)

	#print json.dumps(data_string)

	for i in data_string["forecast"]["simpleforecast"]["forecastday"]:
		#weather_list.append( i["conditions"] )
		c = i["conditions"]
		if c == "Chance of Rain" or c == "Rain":
			weather_list.append(0)
		elif c == "Chance of a Thunderstorm" or c == "Chance of Thunderstorms" or c == "Thunderstorms" or c == "Thunderstorm":
			weather_list.append(1)
		elif c == "Sunny" or c == "Clear":
			weather_list.append(2)
		else: #cloudy-ish?
			weather_list.append(3)

	return weather_list

#import json, urllib, urllib2

def micasa_report():

	micasa_list = []

	mc_url = 'http://192.168.1.147:3480/data_request?id=sdata'
	mc_json = urllib.urlopen(mc_url).read()
	data_string = json.loads(mc_json)

	for i in data_string["devices"]:
		if i["category"] == 7:
			#print i["name"]
			#print i["state"]
			if i["locked"] == "0":
				micasa_list.append(0)
			else:
				micasa_list.append(1)

	for i in data_string["devices"]:
		if i["category"] == 4:
			#print i["name"]
			#print i["state"]
			if i["tripped"] == "0":
				micasa_list.append(2)
			else:
				micasa_list.append(3)


	return micasa_list

def netservice_report():
        netservice_list = []
	conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
	conn.login('falldeaf@gmail.com', 'qxxunaqcwvjpbopk')
	unreadCount = re.search("UNSEEN (\d+)", conn.status("INBOX", "(UNSEEN)")[1][0]).group(1)

	#print unreadCount
	if unreadCount > 0:
		netservice_list.append(1)
	else:
		netservice_list.append(0)

	return netservice_list
