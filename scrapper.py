from bs4 import BeautifulSoup
import requests
import lxml
from datetime import datetime

def get_free_deals(free_div, base_url):
    free_title = []
    free_link = []
    free_details = []
    free_pic = []

    for items in free_div:
        free_title.append(items.div.h2.a.span.get_text())
        free_link.append(base_url + items.div.h2.a['href'])
        free_details.append(items.find("div", {"class":"content"}).p.get_text())
        try:
            free_pic.append(items.findAll('a')[1].img['data-src'])
        except: 
            free_pic.append(items.findAll('a')[1].img['src'])

    free_deals = dict()
    free_deals['title'] = (free_title)
    free_deals['details'] = (free_details)
    free_deals['link'] = (free_link)
    free_deals['pic'] = (free_pic)
    return free_deals

def get_bundle_deals(bundle_div, base_url):
    bundle_title = []
    bundle_link = []
    bundle_details = []
    bundle_pic = []
    for items in bundle_div:
        bundle_title.append(items.div.h2.a.span.get_text())
        bundle_link.append(base_url + items.div.h2.a['href'])
        bundle_details.append(items.find("div", {"class":"content"}).findAll("p")[1].get_text())
        try:
            bundle_pic.append(items.findAll('a')[1].img['data-src'])
        except: 
            bundle_pic.append(items.findAll('a')[1].img['src'])

    bundle_deals = dict()
    bundle_deals['title'] = (bundle_title)
    bundle_deals['details'] = (bundle_details)
    bundle_deals['link'] = (bundle_link)
    bundle_deals['pic'] = (bundle_pic)
    return bundle_deals

class scrapper:

    def get_data():
        base_url = "https://www.epicbundle.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url=base_url, headers=headers)
        soup = BeautifulSoup(res.text, features="lxml")
        free_div = soup.findAll("div", {"class":"article bundleItem blogArticle blog-shortnews blog-subtype-free"})
        bundle_div = soup.findAll("div", {"class": "article bundleItem blogArticle blog-bundle-new blog-subtype-"})
        free_deals = get_free_deals(free_div, base_url)
        bundle_deals = get_bundle_deals(bundle_div, base_url)
        deals = dict()
        deals['free'] = free_deals
        deals['bundle'] = bundle_deals

        print(len(deals['free']))

        for i in range(0, len(deals['free']['pic'])):
            print(deals['free']['pic'][i])
            with open("img/free"+str(i)+".jpeg", "wb") as out_file:
                img = requests.get(deals['free']['pic'][i], verify=False)
                out_file.write(img.content)
        for i in range(0, len(deals['bundle']['pic'])):
            print(deals['bundle']['pic'][i])
            with open("img/bundle"+str(i)+".jpeg", "wb") as out_file:
                img = requests.get(deals['bundle']['pic'][i], verify=False)
                out_file.write(img.content)
        return deals