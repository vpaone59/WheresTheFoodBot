# Vincent Paone
# Project began 6/30/2022 --
# WTFBot - Where's The Food Discord Bot  - main file
#

import os
import asyncio
from tokenize import String
from discord.ext import commands
from discord.utils import get
import random
import googlemaps
import requests
import discord
from dotenv import load_dotenv

load_dotenv() # loads the .env file

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
googlekey = os.getenv("GOOGLE_KEY")
print(googlekey)
# gmaps = googlemaps.Client(key=googlekey)

async def main():
    """
    main function that starts the Bot
    """
    global food_list # storing user input in this list
    food_list = []

    async with bot:
        await bot.start('OTk2NTE4NDkyODEzNjc2NTk1.GyQeMg.dg7SKP10-2Iaimvf5vUcj39OefoO-FbD6PAH_A')
        # on_ready will run next

@bot.event
async def on_ready():
    """
    runs once the bot establishes a connection with Discord
    """
    print(f'Logged in as {bot.user}')
    try:
        print("Bot ready")
    except Exception as e:
        print(f'Bot not ready {e}')


# every time there is a message in any channel in any guild, this runs
# param: message - The message content that was last sent
@bot.event
async def on_message(message):
    """
    every time there is a message in any channel in any guild, this runs
    param message - The message that was last sent to the channel
    """
    # ignore messages sent from the bot itself and other bots
    # prevents infinite replying
    if message.author == bot.user or message.author.bot:
        return
    
    await bot.process_commands(message)


@bot.command(aliases=['additem'])
async def add_food(ctx, add_on):
    """
    Add a food item to the food list. Takes one String parameter
    """
    if not add_on:
        await ctx.send("Can't add blank or none item")
    elif add_on in food_list:
        await ctx.send("Item already in the list")
    else:
        food_list.append(add_on)
        print(food_list)

@bot.command(aliases=['getlist'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def get_food_list(ctx):
    """
    Display the food list if there is at least one item
    """
    if len(food_list) == 0:
        await ctx.send("No items in the list")
    else:
        x = ''
        for f in food_list:
            f_but_string = str(f)
            x += f_but_string + '\n'
        await ctx.send(f"```{x}```")

@bot.command(aliases=['editlist'])
async def edit_food_list(ctx):
    """
    A function built with button views to allow the user to easily edit the food list using buttons, inputs, etc
    """
    await ctx.send('Choose an option:', view=Edit_Food_List())

class Edit_Food_List(discord.ui.View):
    """
    View that shows the buttons for the edit food list command
    """
    def __init__(self, *, timeout=120):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Add Item", style=discord.ButtonStyle.blurple)
    async def add_item_button(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.send_message("Add item")

    @discord.ui.button(label="Remove Item", style=discord.ButtonStyle.red)
    async def remove_item_button(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.send_message("Remove item")

asyncio.run(main())





# # params: ctx, the context in which the command is used
# @bot.command()
# # command can only be sent 1 time, every 3 seconds, per user.
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def foodsearch(ctx, *keywords):
#     kw = ' '.join(keywords)
#     googlefoods(kw)

#     with open("./google_search/google_results.json", "r+") as f:
#         data = json.load(f)

#     name = data["results"][0]["name"]
#     address = data["results"][0]["formatted_address"]
#     status = data["results"][0]["business_status"]
#     open_now = data["results"][0]["opening_hours"]
#     photo_ref_id = data["results"][0]["photos"][0]["photo_reference"]
#     average_rating = data["results"][0]["rating"]
#     total_ratings = data["results"][0]["user_ratings_total"]

#     if open_now["open_now"] == True:
#         open_status = "open"
#     else:
#         open_status = "closed"
#     await ctx.send(f"```We found a result near you for {name}. It's located at {address} and is currently {open_status} and {status.lower()}.```")

#     await ctx.send(f"```This particular location of {name} has an Average Rating (out of 5⭐️) of {average_rating}⭐️, with {total_ratings} total customer ratings.```")

#     googlefoodphoto(photo_ref_id)

#     await ctx.send(file=discord.File(current_directory + "/google_search/photo.jpg"))




        
# # add a food item to the foodlist.json
# # only admin should be able to run this
# # param: ctx - The context of which the command is entered
# # param: food - The food item/restaurant you want to add to the list
# @client.command(aliases=['af'])
# @commands.has_permissions(administrator=True)
# # command can only be sent 1 time, every 3 seconds, per user.
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def addfood(ctx, *args):
#     # check if the food is already in the list
#     food = ' '.join(args)
#     if food.lower() in foodlist:
#         await ctx.send("```{} is already in the list!```".format(food))
#     else:
#         foodlist.append(food.lower())
#         # add it to the list
#         with open("./foodlist.json", "r+") as f:
#             data = json.load(f)
#             data["FOOD"] = foodlist
#             f.seek(0)
#             f.write(json.dumps(data))
#             f.truncate()  # resizes file

#         await ctx.send("```{} added to the food list```".format(food))


# # add a food item to the foodlist.json
# # only admin should be able to run this
# # param: ctx - The context of which the command is entered
# # param: food - The food item you want to remove from the list
# @client.command(aliases=['rf'])
# @commands.has_permissions(administrator=True)
# # food can only be sent 1 time, every 3 seconds, per user.
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def remfood(ctx, *args):
#     food = ' '.join(args)
#     print(type(food))
#     if food.lower() in foodlist:
#         foodlist.remove(food.lower())
#         with open("./foodlist.json", "r+") as f:
#             data = json.load(f)
#             data["FOOD"] = foodlist
#             f.seek(0)
#             f.write(json.dumps(data))
#             f.truncate()

#         await ctx.send("```{} removed from the food list```".format(food))

#     # if the word isn't in the list
#     else:
#         await ctx.send("```{} is not in the list```".format(food))


# # a version of foodsearch that grabs more details from the location using a 2nd API call
# # !!!!!! this command utilizes the googlefoods() function AND WILL OVERWRITE any data in the google_results.json file
# # params: ctx - The context in which the command is used
# # params: *keywords - Multiple String objects that are combined into a single keyword query
# # params: ctx, the context in which the command is used
# @client.command()
# # command can only be sent 1 time, every 3 seconds, per user.
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def detailedfood(ctx, *keywords):
#     # combine the Strings entered in *keywords
#     kw = ' '.join(keywords)
#     googlefoods(kw)

#     # open the details.json created in googlefoods()
#     with open("./google_search/google_results.json", "r+") as f:
#         data = json.load(f)

#     # before assigned any variables, we make sure the API call did not fail
#     if data["status"] == "REQUEST_DENIED":
#         await ctx.send("REQUEST DENIED")
#         print(data["error_message"])
#     elif data["status"] != "OK":
#         await ctx.send("ERROR IN REQUEST")
#         print(data["error_message"])

#     name = data["results"][0]["name"]
#     address = data["results"][0]["formatted_address"]
#     status = data["results"][0]["business_status"]
#     open_now = data["results"][0]["opening_hours"]
#     photo_ref_id = data["results"][0]["photos"][0]["photo_reference"]
#     average_rating = data["results"][0]["rating"]
#     total_ratings = data["results"][0]["user_ratings_total"]
#     # new variable place_id
#     place_id = data["results"][0]["place_id"]

#     # use the unqiue place_id to do another API call for more details on the location
#     moredetails(place_id)

#     # use the phote ref id to get the photo
#     googlefoodphoto(photo_ref_id)

#     with open("./place_details/details.json", "r+") as f:
#         details = json.load(f)

#     reviews = details["result"]["reviews"]

#     # loop to get the reviews and add to a variable for sending later
#     x = 0
#     print_reviews = ""
#     for r in reviews:

#         r = reviews[x]

#         nam = r["author_name"]
#         ratin = r["rating"]
#         tim = r["relative_time_description"]
#         revie = r["text"]

#         print_reviews = print_reviews + \
#             "\nAuthor Name: " + nam + "\nRating: " + \
#             str(ratin) + "\nPosted: " + tim + "\nReview: " + revie + "\n"
#         x += 1

#     # set the "open" status of the location returned
#     if open_now["open_now"] == True:
#         open_status = "open"
#     else:
#         open_status = "closed"

#     # print location name, address, status, average rating and total rating
#     await ctx.send(f"```We found a result near you for {name}. It's located at {address} and is currently {open_status} and {status.lower()}.```")
#     await ctx.send(f"```This particular location of {name} has an Average Rating (out of 5⭐️) of {average_rating}⭐️, with {total_ratings} total customer ratings.```")

#     # print the photo for the location
#     await ctx.send(file=discord.File(current_directory + "/google_search/photo.jpg"))

#     # print some reviews (top 5) for the location
#     await ctx.send(f"```Here are some reviews:\n{print_reviews}```")


# # create a Google Maps API request url using user provided keywords
# # fills json google_results.json with the data returned
# # this specific function searches for locations with type=restaurant
# # params: keyword - The query to search for when making the API call
# def googlefoods(keyword):

#     searchurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="

#     # by default google will use current IP to find a result
#     url = searchurl + keyword + "&type=restaurant&key=" + googlekey
#     print(url)
#     data = requests.get(url).json()

#     if os.path.exists(current_directory + "/google_search/google_results.json"):
#         print("GOOGLE_RESULTS.JSON PATH EXISTS")
#         with open(current_directory + "/google_search/google_results.json", "w+") as f:
#             json.dump(data, f)

#     else:
#         print("GOOGLE_RESULTS.JSON PATH DOES NOT EXIST")
#         with open(current_directory + "/google_search/google_results.json", "w+") as f:
#             print("CREATED GOOGLE_RESULTS.JSON")
#             json.dump(data, f)
#             # dump the configTemplate to the new config.json


# # creates the photo file for the location returned in foodsearch
# # params: photo_reference_id - The reference id to the photo created when googlefoods() is called
# def googlefoodphoto(photo_reference_id):
#     photo_height = 400
#     photo_width = 400
#     raw_image_data = gmaps.places_photo(
#         photo_reference=photo_reference_id, max_height=photo_height, max_width=photo_width)

#     print("PHOTO DATA FOUND")
#     # open or create new file photo.jpg
#     # w: Open a file for writing. Creates a new file if it does not exist or truncates the file if it exists.
#     # b: Open in binary mode.
#     f = open('./google_search/photo.jpg', 'wb+')
#     print("PHOTO FILE CREATED")
#     for chunk in raw_image_data:
#         if chunk:
#             f.write(chunk)
#         else:
#             print("ALL CHUNKS LOADED")


# # using the place_id generated from googlefoods() we can make another API call to get information that textsearch can't get
# # params: placeid - The place_id generated from googlefoods()
# def moredetails(placeid):

#     searchurl = "https://maps.googleapis.com/maps/api/place/details/json?place_id="
#     # searchradius = "&radius=" + radius
#     # searchfields = "&fields=formatted_address%2Cname%2Crating%2Cbusiness_status%2Copening_hours%2Cgeometry%2Cphotos"

#     # by default google will use current IP for location when finding a result
#     # create the url request
#     url = searchurl + placeid + "&key=" + googlekey
#     print(url)
#     data = requests.get(url).json()

#     if os.path.exists(current_directory + "/place_details/details.json"):
#         print("details.json PATH EXISTS")
#         with open(current_directory + "/place_details/details.json", "w+") as f:
#             json.dump(data, f)

#     else:
#         print("GOOGLE_RESULTS.JSON PATH DOES NOT EXIST")
#         with open(current_directory + "/google_search/google_results.json", "w+") as f:
#             print("CREATED details.JSON")
#             json.dump(data, f)
#             # dump the configTemplate to the new config.json



