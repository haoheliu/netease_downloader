#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import threading
import os
import json
import re
from bs4 import BeautifulSoup

def load_json(fname):
    with open(fname,'r') as f:
        data = json.load(f)
        return data

Config = load_json("config.json")

save_root = Config['save_path']
urls = Config['urls']

class NeteaseDownloader(threading.Thread):
    musicData = []
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

    def __init__(self, threadID, name, counter):
        # 多线程
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.url_text = ""
        self.list_name = ""

        if not os.path.exists(save_root):
            raise ValueError(save_root+" does not exist!")
        # if(not save_root[-1] == '/'):
        #     raise ValueError("Error: Path should end with /")

    def __del__(self):
        pass

    def run(self):
        print("Start downloading...")
        self.get(self.musicData)

    def download(self,url):
        self.url_text = url
        self.musicData = []
        self.list_name = os.path.split(url)[1]
        self.musicData = self.getMusicData(self.url_text.replace("#/", ""))
        if len(self.musicData) > 1:
            self.start()

    def get(self, values):
        print(len(values))
        downNum = 0
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        for x in values:
            x['name'] = re.sub(rstr, "_", x['name'])
            if not os.path.exists(os.path.join(save_root,self.list_name)+"/"+ x['name'] + '.mp3'):
                print('***** ' + x['name'] + '.mp3 ***** Downloading...')

                url = 'http://music.163.com/song/media/outer/url?id=' + x['id'] + '.mp3'
                try:
                    # urllib.request.urlretrieve(url,'./music/' + x['name'] + '.mp3')
                    self.saveFile(url, os.path.join(save_root,self.list_name)+"/"+ x['name'] + '.mp3')
                    downNum = downNum + 1
                except:
                    x = x - 1
                    print(u'Download wrong~')
        print('Download complete ' + str(downNum) + ' files !\n')

    def getMusicData(self, url):
        headers = {'User-Agent': self.user_agent}
        # webData = requests.get(url, headers=headers).text
        webData = None
        with open(url,'r') as f :
            webData = f.read()
        soup = BeautifulSoup(webData, 'lxml')
        find_list = soup.find_all('div', class_="ttc")
        res_list = []
        for each in find_list:
            res_list.append(each.find('a'))
        find_list = res_list
        # self.list_name = soup.find_all(name='h2',attrs={"class":"f-ff2 f-brk"})
        # self.list_name = str(self.list_name).split('<')[-2].split('>')[-1]
        if(not os.path.exists(os.path.join(save_root,self.list_name))):
            os.mkdir(os.path.join(save_root,self.list_name))
        tempArr = []
        for a in find_list:
            music_id = a['href'].replace('/song?id=', '')
            music_name = a.text
            tempArr.append({'id': music_id, 'name': music_name})
        return tempArr

    def saveFile(self, url, path):
        headers = {'User-Agent': self.user_agent,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Upgrade-Insecure-Requests': '1'}
        response = requests.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(response.content)
            f.flush()


if(len(urls) == 0):
    print("Reminder: You must specify url in config.json")

for url in urls:
    frame = NeteaseDownloader(1, "Thread-1", 1)
    try:
        frame.download(url)
    except:
        print("Download ",url,"Failed!!!")
    