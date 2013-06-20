from bs4 import BeautifulSoup

#soup = BeautifulSoup( urllib2.urlopen('http://magicseaweed.com/syndicate/index.php?action=content&licenseKey=1366048199_83523').read() )

import urllib
import urllib2

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

surf_array = surf_report()
print surf_array
print surf_array[2]
