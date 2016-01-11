import requests
from bs4 import BeautifulSoup
import re

r = requests.get('http://www.amc.com/full-episodes-archive')
soup = BeautifulSoup(r.text, 'html.parser')
#myre = re.compile(r'show\s')
#mystr = open('test.html').read()
#print(mystr)
#p = re.compile(r'show( [a-z]+)+')
#print(p.findall(mystr))
#mystr = "show into-the-badlands featured first even"
res_soup = soup.findAll("div", {"class": 'shows'})
#res_soup = soup.findAll('div', class_=re.compile(r'show'))
#print(res_soup)
fs = BeautifulSoup(str(res_soup), "html.parser")

episode_res = fs.findAll('div', class_='show')
for i in episode_res:
    print(i.img['src'])
    print(i.img['alt'])
    serl_url = i.a['href']
    print(serl_url)
    serial = requests.get(serl_url+'/exclusives/about')
    serial_soup = BeautifulSoup(serial.text, 'html.parser')
    print(serial_soup.find('div', {"class": 'about-detail-float-desc'}).getText())
    for z in i.findAll("a", {"class": 'episode '}):
        print(z['href'])
    
#es = BeautifulSoup(str(episode_res), "html.parser")
#print(type(fs))
#tag = fs.div
#tag = es.a
#print(es)

