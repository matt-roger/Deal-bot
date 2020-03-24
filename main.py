from bs4 import BeautifulSoup
import requests
import lxml
import re
import json
import discord
from discord.ext import commands

def get_token():
    with open('secret.json') as json_file:
        data = json.load(json_file)
    return data['token']

def get_free_deals(free_div, base_url):
    free_title = []
    free_link = []
    free_details = []
    for items in free_div:
        free_title.append(items.div.h2.a.span.get_text())
        free_link.append(base_url + items.div.h2.a['href'])
        free_details.append(items.find("div", {"class":"content"}).p.get_text())
    
    free_deals = dict()
    free_deals['title'] = (free_title)
    free_deals['details'] = (free_details)
    free_deals['link'] = (free_link)
    return free_deals

def get_bundle_deals(bundle_div, base_url):
    bundle_title = []
    bundle_link = []
    bundle_details = []
    for items in bundle_div:
        bundle_title.append(items.div.h2.a.span.get_text())
        bundle_link.append(base_url + items.div.h2.a['href'])
        bundle_details.append(items.find("div", {"class":"content"}).findAll("p")[1].get_text())

    bundle_deals = dict()
    bundle_deals['title'] = (bundle_title)
    bundle_deals['details'] = (bundle_details)
    bundle_deals['link'] = (bundle_link)
    return bundle_deals

def parse_data(param):
    base_url = "https://www.epicbundle.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url=base_url, headers=headers)
    soup = BeautifulSoup(res.text)
    free_div = soup.findAll("div", {"class":"article bundleItem blogArticle blog-shortnews blog-subtype-free"})
    bundle_div = soup.findAll("div", {"class": "article bundleItem blogArticle blog-bundle-new blog-subtype-"})
    free_deals = get_free_deals(free_div, base_url)
    bundle_deals = get_bundle_deals(bundle_div, base_url)
    result = ''

    if(param == 'free'):
        for i in range(0,len(free_deals)):
            result += '\nTitle: ' + free_deals['title'][i] + '\n'
            result += 'Details: ' + free_deals['details'][i] + '\n'
            result += 'Link: ' + free_deals['link'][i] + '\n\n'
    elif(param == 'bundle'):
        for i in range(0,len(bundle_deals)):
            result += '\nTitle: ' + bundle_deals['title'][i] + '\n'
            result += 'Details: ' + bundle_deals['details'][i] + '\n'
            result += 'Link: ' + bundle_deals['link'][i] + '\n\n'
    else:
        result = 'Free Deals\n'
        for i in range(0,len(free_deals)):
            result += '\nTitle: ' + free_deals['title'][i] + '\n'
            result += 'Details: ' + free_deals['details'][i] + '\n'
            result += 'Link: ' + free_deals['link'][i] + '\n\n'
        result += '--------------------------------------------------'
        result = 'Bundle Deals\n'
        for i in range(0,len(free_deals)):
            result += '\nTitle: ' + bundle_deals['title'][i] + '\n'
            result += 'Details: ' + bundle_deals['details'][i] + '\n'
            result += 'Link: ' + bundle_deals['link'][i] + '\n\n'

    return result
    
#----------------------------------------------------main
TOKEN = get_token()
client = commands.Bot(command_prefix='!')
#------------------------------------------------

@client.command()
async def free(ctx):
    await ctx.send(parse_data('free'))

@client.command()
async def bundle(ctx):
    await ctx.send(parse_data('bundle'))

@client.command()
async def deal(ctx):
    await ctx.send(parse_data('deal'))

@client.event
async def on_ready():
    print('Bot is Ready')

client.run(TOKEN)

