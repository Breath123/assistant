import requests
import bs4
import re
import os
from selenium import webdriver
os.environ["http_proxy"] = "10.144.1.10:8080"
os.environ["https_proxy"] = "10.144.1.10:8080"
'''
r = requests.get('http://www.weather.com.cn/data/sk/101210101.html')
print(r.status_code)
weather = r.content.decode('utf-8')
print(weather)

#weather = r.json()
#weather['weatherinfo']['city'].decode('utf-8')
#print(weather)
#print(weather.weatherinfo)
#print(weather.items())
#weather.weatherinfo.city = weather.weatherinfo.city.decode('utf-8')
#print(weather)
'''
# use Chrome because requests can't fetch all elements
driver = webdriver.Chrome('C://Tools/chromedriver.exe')
url = 'http://www.weather.com.cn/weather1d/101210101.shtml'
driver.get(url)
soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
overall = soup.find('div', class_='today clearfix').find_all('input')
detail = soup.find('div', class_='curve_livezs')
weather = {}
for content in str(overall).split('/>, <'):
    if re.search('hidden_title', content):
        info_list = content.split('value="')[1] \
                           .split() # Split by one or more spaces
        date = info_list[0]
        day = info_list[1]
        weather_day = info_list[2]
        temp = info_list[3][0:-1]
        temp_high = temp.split('/')[0]
        temp_low = temp.split('/')[1][:-2]

        weather['date'] = date
        weather['day'] = day
        weather['weather'] = weather_day
        weather['temp'] = temp
        weather['temp_high'] = temp_high
        weather['temp_low'] = temp_low

detail_time = detail.find('div', class_='time').find_all('em')
detail_time_list = re.findall(r'[\d]{2}时', str(detail_time))
print(detail_time_list)

detail_wpic = detail.find('div', class_='wpic').find_all('div')
detail_wpic_list = re.findall(r'\"[\u4e00-\u9fff]+\"', str(detail_wpic))
print(detail_wpic_list)

detail_temp = detail.find('div', class_='tem').find_all('em')
detail_temp_list = re.findall(r'[\w]+℃', str(detail_temp))
print(detail_temp_list)

detail_winf = detail.find('div', class_='winf').find_all('em')
detail_winf_list = re.findall(r'[\u4e00-\u9fff]+', str(detail_winf))
print(detail_winf_list)

detail_winl = detail.find('div', class_='winl').find_all('em')
detail_winl_list = re.findall(r'[\d]+级', str(detail_winl))
print(detail_winl_list)

for index, hour in enumerate(detail_time_list):
    weather[hour + '_' + 'wpic'] = detail_wpic_list[index]
    weather[hour + '_' + 'temp'] = detail_temp_list[index]
    weather[hour + '_' + 'winf'] = detail_winf_list[index]
    weather[hour + '_' + 'winl'] = detail_winl_list[index]


driver.quit()
# {'date': '03月29日08时', 'day': '周五',
# 'weather': '阵雨转多云', 'temp': '19/11°C',
# 'temp_high': '19', 'temp_low': '11',
# '08时_wpic': '"阴"', '08时_temp': '13℃',
# '08时_winf': '东北风', '08时_winl': '3级',
# '11时_wpic': '"阵雨"', '11时_temp': '17℃',
# '11时_winf': '东北风', '11时_winl': '3级',
# '14时_wpic': '"阵雨"', '14时_temp': '18℃',
# '14时_winf': '东北风', '14时_winl': '3级',
# '17时_wpic': '"阴"', '17时_temp': '17℃',
# '17时_winf': '东北风', '17时_winl': '3级',
# '20时_wpic': '"阴"', '20时_temp': '14℃',
# '20时_winf': '东北风', '20时_winl': '3级',
# '23时_wpic': '"多云"', '23时_temp': '13℃',
# '23时_winf': '西南风', '23时_winl': '3级',
# '02时_wpic': '"多云"', '02时_temp': '12℃',
# '02时_winf': '西南风', '02时_winl': '3级',
# '05时_wpic': '"多云"', '05时_temp': '11℃',
# '05时_winf': '西南风', '05时_winl': '3级'}
print(weather)
#print(detail)
#print(detail_time)

from pymongo import MongoClient
import pandas as pd
import pytz
current_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d:%H-%M')
weather['insert_time'] = current_time

client = MongoClient('localhost', 27017)
db = client['weather']
collection = db['weather_info']
collection.insert_one(weather)
