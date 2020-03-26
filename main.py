from bs4 import BeautifulSoup
import requests
import lxml
import re
import json
import discord
from discord.ext import commands
from datetime import datetime
import time

def get_token():
    with open('secret.json') as json_file:
        data = json.load(json_file)
    return data['token']

def get_free_deals(free_div, base_url):
    free_title = []
    free_link = []
    free_details = []
    free_pic = []

    for items in free_div:
        free_title.append(items.div.h2.a.span.get_text())
        free_link.append(base_url + items.div.h2.a['href'])
        free_details.append(items.find("div", {"class":"content"}).p.get_text())
        free_pic.append(items.findAll('a')[1].img['data-src'])

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

def get_data():
    base_url = "https://www.epicbundle.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url=base_url, headers=headers)
    soup = BeautifulSoup(res.text)
    free_div = soup.findAll("div", {"class":"article bundleItem blogArticle blog-shortnews blog-subtype-free"})
    bundle_div = soup.findAll("div", {"class": "article bundleItem blogArticle blog-bundle-new blog-subtype-"})
    free_deals = get_free_deals(free_div, base_url)
    bundle_deals = get_bundle_deals(bundle_div, base_url)
    deals = dict()
    deals['free'] = free_deals
    deals['bundle'] = bundle_deals

    for i in range(0, len(free_deals)):
        print(deals['free']['pic'][i])
        with open("img/free"+str(i)+".jpeg", "wb") as out_file:
            img = requests.get(deals['free']['pic'][i], verify=False)
            out_file.write(img.content)
    for i in range(0, len(bundle_deals)):
        print(deals['bundle']['pic'][i])
        with open("img/bundle"+str(i)+".jpeg", "wb") as out_file:
            img = requests.get(deals['bundle']['pic'][i], verify=False)
            out_file.write(img.content)
    return deals

def log(user, action):
    with open("logs/action.log", "a+") as log:
        log.write("\nDate:"+datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"User:"+user+"Action:"+action)
#----------------------------------------------------main
TOKEN = get_token()
client = commands.Bot(command_prefix='!')
#------------------------------------------------

@client.command()
async def free(ctx):
    result = ''
    free_deals = get_data()
    free_deals = free_deals['free']
    for i in range(0,len(free_deals)):
            result = '\nTitle: ' + free_deals['title'][i] + '\n' + 'Details: ' + free_deals['details'][i] + '\n' + 'Link: ' + free_deals['link'][i] + '\n'
            with open('img/free'+str(i)+'.jpeg', 'rb') as f:
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
                await ctx.send(result)
                await ctx.send(file=discord.File(f))
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
    await ctx.send('END')
    log(str(ctx.author),'Command:!free')

@client.command()
async def bundle(ctx):
    result = ''
    bundle_deals = get_data()
    bundle_deals = bundle_deals['bundle']
    for i in range(0,len(bundle_deals)):
            result = '\nTitle: ' + bundle_deals['title'][i] + '\n'+ 'Details: ' + bundle_deals['details'][i] + '\n'+ 'Link: ' + bundle_deals['link'][i] + '\n'
            with open('img/bundle'+str(i)+'.jpeg', 'rb') as f:
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
                await ctx.send(result)
                await ctx.send(file=discord.File(f))
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
    await ctx.send('END')
    log(str(ctx.author),'Command:!bundle')

@client.command()
async def deal(ctx):
    result = ''
    free_deals = get_data()
    free_deals = free_deals['free']
    bundle_deals = get_data()
    bundle_deals = bundle_deals['bundle']
    await ctx.send('\nFREE\n')
    for i in range(0,len(free_deals)):
            result = '\nTitle: ' + free_deals['title'][i] + '\n' + 'Details: ' + free_deals['details'][i] + '\n' + 'Link: ' + free_deals['link'][i] + '\n'
            with open('img/free'+str(i)+'.jpeg', 'rb') as f:
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
                await ctx.send(result)
                await ctx.send(file=discord.File(f))
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
    await ctx.send('\nBUNDLE\n')
    for i in range(0,len(bundle_deals)):
            result = '\nTitle: ' + bundle_deals['title'][i] + '\n'+ 'Details: ' + bundle_deals['details'][i] + '\n'+ 'Link: ' + bundle_deals['link'][i] + '\n'
            with open('img/bundle'+str(i)+'.jpeg', 'rb') as f:
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
                await ctx.send(result)
                await ctx.send(file=discord.File(f))
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
    await ctx.send('END')

@client.event
async def on_ready():
    print('Bot is Ready')
    await start_up(datetime.today())
    
async def start_up(last):
    now = datetime.today()
    now = datetime.date(2020,3,25)
    channel = client.get_channel(692103127947673605)
    if(now > last):
        result = ''
        free_deals = get_data()
        free_deals = free_deals['free']
        bundle_deals = get_data()
        bundle_deals = bundle_deals['bundle']
        await ctx.send('\nFREE\n')
        for i in range(0,len(free_deals)):
                result = '\nTitle: ' + free_deals['title'][i] + '\n' + 'Details: ' + free_deals['details'][i] + '\n' + 'Link: ' + free_deals['link'][i] + '\n'
                with open('img/free'+str(i)+'.jpeg', 'rb') as f:
                    await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
                    await ctx.send(result)
                    await ctx.send(file=discord.File(f))
                    await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
        await ctx.send('\nBUNDLE\n')
        for i in range(0,len(bundle_deals)):
                result = '\nTitle: ' + bundle_deals['title'][i] + '\n'+ 'Details: ' + bundle_deals['details'][i] + '\n'+ 'Link: ' + bundle_deals['link'][i] + '\n'
                with open('img/bundle'+str(i)+'.jpeg', 'rb') as f:
                    await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
                    await ctx.send(result)
                    await ctx.send(file=discord.File(f))
                    await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
        await ctx.send('END')
        time.sleep(18000)
        await start_up(now)
    else:
        time.sleep(18000)
        await start_up(last)

@client.event
async def on_command_error(ctx,error):
    print("Bot error: " + str(error))
    await ctx.send("Bot error: " + str(error))
    await ctx.send("Type the !help command to see available commands")

client.run(TOKEN)
