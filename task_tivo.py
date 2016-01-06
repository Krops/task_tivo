import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.amc.com/full-episodes-archive')
soup = BeautifulSoup(r.text, 'html.parser')
soup.findAll("div", { "class" : "show imagine-john-lennon-75th-birthday-concert featured even" })

