from bs4 import BeautifulSoup
import requests
import json
import datetime
from calendar import monthrange


STARTING_DAY = datetime.date.today().day
MONTH = datetime.date.today().month
NEXTMONTH = MONTH+1
MAXDAYS = 30
INITIALCOUNT = 1
def scrap_by_month(day,month,count):
	max_days = monthrange(2018, month)[1]
	count = count
	for i in range(day, max_days+2):
		print(count)
		if(count == MAXDAYS):
			break
		elif (i == max_days+1):
			scrap_by_month(1,month+1,count)
		else:	
			scrap_that(i, month)
			count = count + 1

		
def scrap_that(day,month):
	url_template = f'https://br.hbomax.tv/ajax.programacion-canal.html?pid=4&cul=pt&oid=4&fecha={month}/{day}/2018'
	data = requests.get(url_template).text
	soup = BeautifulSoup(data,'lxml')
	main = soup.find_all('tbody')
	list_of_channels = ['HBO','HBO2','HBOPLUS','HBOPLUS','HBOFAMILY','HBOSIGNATURE','MAX','MAXUP','MAXPRIME','MAXPRIME']
	
	for i, channel in enumerate(main):
		movies = channel.find_all('tr')

		for movie_detail in movies:

			try:
				obj = {}
				obj['day'] = day
				obj['month'] = month
				obj['channel_name'] = list_of_channels[i]
				obj['title'] = movie_detail.find('h5', class_='estilo-titulo-gris').text.strip()
				obj['img'] = movie_detail.find('img').get('src')
				obj['hour_start'] = movie_detail.find('h5').text.strip()
				list_of_stuff.append(obj)
			except AttributeError:
				break
list_of_stuff=[]

scrap_by_month(STARTING_DAY,MONTH,INITIALCOUNT)

with open('hbos_info.json', 'w') as f:  
    json.dump(list_of_stuff, f)