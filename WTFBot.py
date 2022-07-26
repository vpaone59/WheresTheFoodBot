# Vincent Paone
# Project began 6/30/2022 --
# WTFBot - What the food bot  - main file
#

from array import array
from ast import alias
import os
import json
import asyncio
from tokenize import String
from discord.ext import commands
from discord.utils import get
import random
import googlemaps
import requests
import discord


current_directory = os.getcwd()
print(current_directory)
# search for the config.json file in the current directory and load the file
if os.path.exists(os.getcwd() + "/FoodBot/config.json"):
    print("CONFIG.JSON PATH EXISTS")
    with open("./FoodBot/config.json") as f:
        configData = json.load(f)
        print("CONFIG.JSON OPENED")
# if the config.json file doesn't exist within the current directory, use the template to create the file
else:
    print("CONFIG PATH DOES NOT EXIST")
    configTemplate = {"TOKEN": "", "PREFIX": "", "GOOGLE": ""}
    with open(os.getcwd() + "/config.json", "w+") as f:
        # dump the configTemplate to the new config.json
        json.dump(configTemplate, f)
        print("NEW CONFIG.JSON CREATED USING PROVIDED TEMPLATE")
# grab some info from the config file
TOKEN = configData["TOKEN"]
prefix = configData["PREFIX"]
googlekey = configData["GOOGLE"]
gmaps = googlemaps.Client(key=googlekey)

# search for the foodlist.json file in the current directory and load the file
if os.path.exists(os.getcwd() + "/FoodBot/foodlist.json"):
    print("FOODLIST.JSON PATH EXISTS")
    with open("./FoodBot/foodlist.json") as f:
        foodData = json.load(f)
        print("FOODLIST.JSON OPENED")
# if the foodlist.json file doesn't exist within the currenty directory, use the template to create the file
else:
    foodTemplate = {"FOOD": []}
    with open(os.getcwd() + "/FoodBot/foodlist.json", "w+") as f:
        # dump the foodTemplate to the new foodlist.json
        json.dump(foodTemplate, f)
        print("NEW FOOD.JSON CREATED USING PROVIDED TEMPLATE")
# grab the FOOD data from the foodlist.json
foodlist = foodData["FOOD"]

# we need to assign the prefix to the bot and denote the bot as 'client'
# 'client' can be called anything it is just a placeholder to refer to the bot
client = commands.Bot(command_prefix=prefix)

# we need this to check the bot connected properly in the on_ready fxn
full_ready = False


# wait for the bot to FULLY connect to the server
# once bot connects print message in local terminal
@client.event
async def on_ready():
    print('$$$$$ We have logged in as {0.user} $$$$$'.format(client))
    print(f'$$$$$ {client} $$$$$')


# every time there is a message in any channel in any guild, this runs
# param: message - The message content that was last sent
@client.event
async def on_message(message):

    # grabs username, user unique id, and the user message
    messageAuthor = message.author
    user_id = str(message.author.id)
    user_message = str(message.content)

    # cleaned up username without # id
    username = str(message.author).split('#')[0]

    # channel name the message was sent from
    channel = str(message.channel.name)
    # server name the message was sent from
    guild = str(message.guild.name)

    # on every message print it to the terminal
    # print the username, the message, the channel it was sent in and the server (guild)
    # print(f'{username}: {user_message} [userid= {user_id} (channel= {channel})]')
    print(f'{username}: {user_message} \t(channel= {channel} on server= {guild})')
    # ignore messages sent from the bot itself
    # prevents infinite replying
    if message.author == client.user:
        return
    # if message starts with 'hello'
    if user_message.lower().startswith('hello'):
        await message.channel.send(f'Hello {messageAuthor.mention}!')
        return
    # necessary to process anything the bot will do
    await client.process_commands(message)


def isempty():

    if len(foodlist) == 0:
        return 0
    else:
        return len(foodlist)

# print a random food item from the foodlist to the channel the command was run in


@client.command()
async def food(ctx):
    if isempty() == 1:
        randfood = foodlist[0]
        await ctx.send(f"```{randfood}```")
    elif isempty() is not 0:
        randindex = random.randint(0, len(foodlist)-1)
        randfood = foodlist[randindex]
        await ctx.send(f"```{randfood}```")
    else:
        await ctx.send("```NO ITEMS IN THE FOOD LIST. PLEASE ADD ITEMS USING !addfood **```")


@client.command()
async def foodsearch(ctx, *keywords):
    kw = ' '.join(keywords)
    googlefoods(kw)

    with open("./FoodBot/google_results.json", "r+") as f:
        data = json.load(f)

    name = data["results"][0]["name"]
    address = data["results"][0]["formatted_address"]
    status = data["results"][0]["business_status"]
    open_now = data["results"][0]["opening_hours"]
    photo_ref_id = data["results"][0]["photos"][0]["photo_reference"]
    if open_now["open_now"] == True:
        open_status = "open"
    else:
        open_status = "closed"
    await ctx.send(f"```We found a result near you for {name}. It's located at {address} and is currently {open_status}.```")

    googlefoodphoto(photo_ref_id)

    await ctx.send(file=discord.File(os.getcwd() + "/FoodBot/photo.jpg"))


# print out all of the items in foodlist to the channel the command was run in
@client.command()
async def getfoodlist(ctx):

    if isempty() == 0:
        await ctx.send("```NO ITEMS IN FOOD LIST```")
    else:
        x = ''
        for f in foodlist:
            f_but_string = str(f)
            x += f_but_string + '\n'
        await ctx.send(f"```{x}```")


# add a food item to the foodlist.json
# only admin should be able to run this
# param: ctx - The context of which the command is entered
# param: food - The food item/restaurant you want to add to the list
@ client.command(aliases=['af'])
@ commands.has_permissions(administrator=True)
# command can only be sent 1 time, every 3 seconds, per user.
@ commands.cooldown(1, 3, commands.BucketType.user)
async def addfood(ctx, *args):
    # check if the food is already in the list
    food = ' '.join(args)
    if food.lower() in foodlist:
        await ctx.send("```{} is already in the list!```".format(food))
    else:
        foodlist.append(food.lower())
        # add it to the list
        with open("./FoodBot/foodlist.json", "r+") as f:
            data = json.load(f)
            data["FOOD"] = foodlist
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()  # resizes file

        await ctx.send("```{} added to the food list```".format(food))


# add a food item to the foodlist.json
# only admin should be able to run this
# param: ctx - The context of which the command is entered
# param: food - The food item you want to remove from the list
@ client.command(aliases=['rf'])
@ commands.has_permissions(administrator=True)
# food can only be sent 1 time, every 3 seconds, per user.
@ commands.cooldown(1, 3, commands.BucketType.user)
async def remfood(ctx, *args):
    food = ' '.join(args)
    print(type(food))
    if food.lower() in foodlist:
        foodlist.remove(food.lower())
        with open("./FoodBot/foodlist.json", "r+") as f:
            data = json.load(f)
            data["FOOD"] = foodlist
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()

        await ctx.send("```{} removed from the food list```".format(food))

    # if the word isn't in the list
    else:
        await ctx.send("```{} is not in the list```".format(food))


def googlefoods(keyword):

    searchurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    # searchradius = "&radius=" + radius
    # searchfields = "&fields=formatted_address%2Cname%2Crating%2Cbusiness_status%2Copening_hours%2Cgeometry%2Cphotos"

    # by default google will use current IP to find a result
    url = searchurl + keyword + "&key=" + googlekey
    print(url)
    data = requests.get(url).json()
    print(data)

    with open(os.getcwd() + "/FoodBot/google_results.json", "w+") as f:
        json.dump(data, f)


def googlefoodphoto(photo_reference_id):
    photo_height = 400
    photo_width = 400
    raw_image_data = gmaps.places_photo(
        photo_reference=photo_reference_id, max_height=photo_height, max_width=photo_width)

    print("PHOTO DATA FOUND")
    # open or create new file photo.jpg
    # w: Open a file for writing. Creates a new file if it does not exist or truncates the file if it exists.
    # b: Open in binary mode.
    f = open('FoodBot/photo.jpg', 'wb')
    print("PHOTO FILE CREATED")
    for chunk in raw_image_data:
        if chunk:
            f.write(chunk)
        else:
            print("ALL CHUNKS LOADED")


client.run(TOKEN)
