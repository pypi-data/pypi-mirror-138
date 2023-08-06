"""
Mini Nhentai Content Scraper by JohnLesterDev.
"""

from bs4 import BeautifulSoup
from random import randint
from json import dumps
from time import sleep
from tqdm import tqdm

import coloredevs as cl
import requests
import pickle
import click
import re
import os


class NHentai:

    def __init__(self, code):
        self.session = requests.Session()
        self.code = code
        self.url = "https://nhentai.net/g/" + str(self.code)
        self.raw = self.session.get(self.url).text
        self.source = BeautifulSoup(self.raw, 'lxml')

        self.info = {'code' : str(self.code)}


    def get_thumbnail(self, debug=False):
        div = self.source.find('div', {'id' : 'cover'})
        img = div.find('img', class_='lazyload')['data-src']

        self.info["cover"] = img

        if debug:
            print(cl.colorize("\n[1/5] : Getting thumbnail....", [randint(50, 255), randint(50, 255), randint(50, 255)]))

        return img


    def get_pages(self, debug=False):
        div = self.source.find_all(text=re.compile("Pages:"))[0].parent
        pages = div.find("span", {'class': 'name'}).contents[0]

        self.info["pages"] = int(pages)

        if debug:
            print(cl.colorize("[2/5] : Getting pages....", [randint(50, 255), randint(50, 255), randint(50, 255)]))

        return pages


    def get_tags(self, debug=False):
        ls = []
        div = self.source.find_all(text=re.compile("Tags:"))[0].parent

        if debug:
            print(cl.colorize("[4/5] : Getting all tags and images....\n", [randint(50, 255), randint(50, 255), randint(50, 255)]))
            for a in tqdm(div.find("span", {"class" : "tags"}), unit=" tags", colour=cl.rgb_to_hex([randint(50, 255), randint(50, 255), randint(50, 255)])):
                tag = str(a.find("span", {"class" : "name"}).contents[0])
                link_tag = tag.replace(" ", "-")
                ls.append(f'{tag}')
        else:
            for a in div.find("span", {"class" : "tags"}):
                tag = str(a.find("span", {"class" : "name"}).contents[0])
                link_tag = tag.replace(" ", "-")
                ls.append(f'{tag}')

        self.info["tags"] = ls

        return ls


    def get_title(self, debug=False):
        title = self.source.find_all("span", {'class' : "pretty"})[0].contents[0]

        self.info["title"] = str(title)

        if debug:
            print(cl.colorize("[3/5] : Getting title....", [randint(50, 255), randint(50, 255), randint(50, 255)]))

        return title


    def get_images(self, debug=False):
        self.info["contents"] = []
        if debug:
            for num in tqdm(range(int(self.info["pages"])), unit=" img", colour=cl.rgb_to_hex([randint(50, 255), randint(50, 255), randint(50, 255)])):
                num += 1
                r = self.session.get(self.url + f"/{num}").text
                s = BeautifulSoup(r, 'lxml')
                img = s.find_all("img")[1]['src']

                self.info["contents"].append(str(img))
        else:
            for num in range(int(self.info["pages"])):
                num += 1
                r = self.session.get(self.url + f"/{num}").text
                s = BeautifulSoup(r, 'lxml')
                img = s.find_all("img")[1]['src']

                self.info["contents"].append(str(img))

        return self.info["contents"]


    def fetch(self, debug=False):
        self.get_thumbnail(debug=debug)
        self.get_pages(debug=debug)
        self.get_title(debug=debug)
        self.get_tags(debug=debug)
        self.get_images(debug=debug)

        return self.info


    def save_images(self, path=None, debug=False):
        path = str(self.code)
        self.fetch(debug=debug)
        
        if not os.path.exists(path):
            os.mkdir(path)

        if debug:
            print(cl.colorize("\n[5/5] : Saving Images.....\n", [randint(50, 255), randint(50, 255), randint(50, 255)]))
            for img in tqdm(self.info["contents"], unit=" img", colour=cl.rgb_to_hex([randint(50, 255), randint(50, 255), randint(50, 255)])):
                filename = img.split('/')[-1]
                with open(os.path.join(path, filename), "wb") as file:
                    file.write(requests.get(img).content)
        else:
            for img in self.info["contents"]:
                filename = img.split('/')[-1]
                with open(os.path.join(path, filename), "wb") as file:
                    file.write(requests.get(img).content)

        tags_ = "\n\t".join(self.info["tags"])
        path_ = os.path.join(os.getcwd(), f"{self.code}")
        info = f"""
\nDoujin Name: {self.info["title"]}

Tags:\t{tags_}

Pages:\t{self.info["pages"]}

Images saved on:
>> {path_}

(Please look at info.jll)"""

        with open(os.path.join(os.path.join(os.getcwd(), "CODES"), "info.json"), "w") as file:
            file.write(json.dumps(self.info, indent=5))
        
        print(cl.colorize(info, [randint(50, 255), randint(50, 255), randint(50, 255)])+"\n")
