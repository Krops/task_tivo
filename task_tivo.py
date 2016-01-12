#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime

r = requests.get('http://www.amc.com/full-episodes-archive')
soup = BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
res_soup = soup.findAll("div", {"class": 'shows'})
fs = BeautifulSoup(str(res_soup), "html.parser")
episode_res = fs.findAll('div', class_='show')

serials_json = []
episode_json = []
for i in episode_res:

    ser_uid = i.find("div", {"class": "heading"}).a["name"]
    serl_url = i.a['href']
    serial = requests.get(serl_url + '/exclusives/about')
    serial_soup = BeautifulSoup(serial.text, 'html.parser')
    # collect serial info to list
    serials_json.append({})
    serials_json[-1]['mtype'] = 'series'
    serials_json[-1]['provider'] = 'amctv'
    serials_json[-1]['title'] = i.img['alt']
    serials_json[-1]['uid'] = 'amctv-series-{0}'.format(ser_uid)
    serials_json[-1]['thumbnails'] = [i.img['src']]
    serials_json[-1]['desc'] = serial_soup.find(
        'div', {"class": 'about-detail-float-desc'}).getText()
    for z in i.findAll("a", {"class": 'episode '}):
        ep_url = z['href']
        epsoup = BeautifulSoup(requests.get(ep_url).text, 'html.parser')
        ep_subtitle = epsoup.find("p", {"class": "subtitle"}).getText()
        ep_info = re.compile(r"Season (\d)+, Episode (\d)+\s+(\d)+ days left")
        numb_info = ep_info.findall(ep_subtitle)
        dateexpires = datetime.datetime.now(
        ) + datetime.timedelta(days=int(numb_info[0][2]))
        ep_id = epsoup.article['id'][5:]
        # collect episode info to list
        episode_json.append({})
        episode_json[-1]['auxdata'] = {'sprintfUriParams': {'url': ep_url}}
        episode_json[-1]['thumbnails'] = [epsoup.find(
            "div", {"class": "img-placeholder"}).img['src']]
        episode_json[-1]['title'] = epsoup.find(
            "h1", {"class": "episode-title"}).a.getText().strip()
        episode_json[-1]['desc'] = epsoup.find(
            "div", {"class": "short-description"}).getText().strip()
        episode_json[-1]['season'] = numb_info[0][0]
        episode_json[-1]['episode'] = numb_info[0][1]
        episode_json[-1]['uid'] = u'amctv-episode-{0}'.format(ep_id)
        episode_json[-1]['mtype'] = 'episode'
        episode_json[-1]['provider'] = 'amctv'
        episode_json[-1]['videos'] = [
            {'dateexpires': dateexpires.strftime("%Y-%m-%d"), 'url': ep_url}]
        episode_json[-1]['_parents'] = {u'amctv-series-{0}'.format(
            ser_uid): {'child': u'amctv-episode-{0}'.format(ep_id)}}
parsed_ser_json = json.loads(json.dumps(serials_json))
parsed_eps_json = json.loads(json.dumps(episode_json))
print(json.dumps(parsed_ser_json, indent=4, sort_keys=True))
print(json.dumps(parsed_eps_json, indent=4, sort_keys=True))
