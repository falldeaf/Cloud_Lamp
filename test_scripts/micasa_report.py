import json, urllib, urllib2

def micasa_report():

	micasa_list = []

	mc_url = 'http://192.168.1.147:3480/data_request?id=sdata'
	mc_json = urllib.urlopen(mc_url).read()
	data_string = json.loads(mc_json)

	for i in data_string["devices"]:
		if i["category"] == 7:
			print i["name"]
			print i["locked"]
			if i["locked"] == "0":
				micasa_list.append(0)
			else:
				micasa_list.append(1)

	for i in data_string["devices"]:
		if i["category"] == 4:
			print i["name"]
			print i["tripped"]
			if i["tripped"] == "0":
				micasa_list.append(2)
			else:
				micasa_list.append(3)


	return micasa_list

print micasa_report()
