import json, urllib, urllib2

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
		weather_list.append( i["conditions"] )
		print i["conditions"]

	return weather_list

print weather_report()
