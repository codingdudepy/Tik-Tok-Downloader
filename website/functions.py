from genericpath import exists
from bs4 import BeautifulSoup as bs
import calendar
import time
import codecs
import subprocess
import requests
import os

headers = {
    'Range': 'bytes=0-',
    'Referer': 'https://www.tiktok.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
}

def find_link(link):
    data = requests.get(link, headers=headers)
    soup = bs(data.content, features="html.parser")
    java_data = soup.find_all(id='sigi-persisted-data')
    for dp in str(java_data).split("},"):
        if "preloadList" in dp:
            for ud in dp.split('"'):
                if "https" in ud:
                    return codecs.decode(ud, 'unicode-escape')

def remove_watermark(file_directory):
    new_file_directory = file_directory.replace('dil', 'wr_dil')
    command = ['ffmpeg', '-i', file_directory, '-filter:v', 'crop=in_w:in_h-185', '-c:v', 'libx264', '-preset','superfast', new_file_directory]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    if exists(new_file_directory):
        os.remove(file_directory) 
    return new_file_directory

def download_video(link):
    content = requests.get(link, headers=headers).content
    fd = 'downloads/{}.mp4'.format("dillytok_" + str(calendar.timegm(time.gmtime())))
    open(fd, mode='wb+').write(content)
    return str(fd)