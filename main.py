from scrapper import scrapper
import requests
import json
import discord
from discord.ext import commands
from datetime import datetime
import time

def get_channel():
    with open('secret.json') as json_file:
        data = json.load(json_file)
    return data['channel']

def get_token():
    with open('secret.json') as json_file:
        data = json.load(json_file)
    return data['token']

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
    free_deals = scrapper.get_data()
    free_deals = free_deals['free']
    for i in range(0,len(free_deals['title'])):
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
    bundle_deals = scrapper.get_data()
    bundle_deals = bundle_deals['bundle']
    for i in range(0,len(bundle_deals['title'])):
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
    free_deals = scrapper.get_data()
    free_deals = free_deals['free']
    bundle_deals = scrapper.get_data()
    bundle_deals = bundle_deals['bundle']
    await ctx.send('\nFREE\n')
    for i in range(0,len(free_deals['title'])):
            result = '\nTitle: ' + free_deals['title'][i] + '\n' + 'Details: ' + free_deals['details'][i] + '\n' + 'Link: ' + free_deals['link'][i] + '\n'
            with open('img/free'+str(i)+'.jpeg', 'rb') as f:
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
                await ctx.send(result)
                await ctx.send(file=discord.File(f))
                await ctx.send('------------------------------------------------------------------------------------------------------------------------------')
    await ctx.send('\nBUNDLE\n')
    for i in range(0,len(bundle_deals['title'])):
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
    #start_up(datetime.date(datetime.now()))
    
async def start_up(last):
    now = datetime.date(datetime.now())
    channel = client.get_channel(get_channel())
    print("now: ")
    print(now)
    print("last: ")
    print(last)
    if(now > last):
        result = ''
        free_deals = scrapper.get_data()
        free_deals = free_deals['free']
        bundle_deals = scrapper.get_data()
        bundle_deals = bundle_deals['bundle']
        await channel.send('\nFREE\n')
        for i in range(0,len(free_deals['title'])):
                result = '\nTitle: ' + free_deals['title'][i] + '\n' + 'Details: ' + free_deals['details'][i] + '\n' + 'Link: ' + free_deals['link'][i] + '\n'
                with open('img/free'+str(i)+'.jpeg', 'rb') as f:
                    await channel.send('------------------------------------------------------------------------------------------------------------------------------')
                    await channel.send(result)
                    await channel.send(file=discord.File(f))
                    await channel.send('------------------------------------------------------------------------------------------------------------------------------')
        await channel.send('\nBUNDLE\n')
        for i in range(0,len(bundle_deals['title'])):
                result = '\nTitle: ' + bundle_deals['title'][i] + '\n'+ 'Details: ' + bundle_deals['details'][i] + '\n'+ 'Link: ' + bundle_deals['link'][i] + '\n'
                with open('img/bundle'+str(i)+'.jpeg', 'rb') as f:
                    await channel.send('------------------------------------------------------------------------------------------------------------------------------')
                    await channel.send(result)
                    await channel.send(file=discord.File(f))
                    await channel.send('------------------------------------------------------------------------------------------------------------------------------')
        await channel.send('END')
        time.sleep(20)
        log("Deal Bot", "Post Deals")
        await start_up(now)
    else:
        time.sleep(20)
        await start_up(last)

@client.event
async def on_command_error(ctx,error):
    print("Bot error: " + str(error))
    await ctx.send("Bot error: " + str(error))
    await ctx.send("Type the !help command to see available commands")

client.run(TOKEN)
