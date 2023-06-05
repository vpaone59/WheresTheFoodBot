# Vincent Paone
# Project began 6/30/2022 --
# WTFBot - Where's The Food Discord Bot  - main file
#

import os
import asyncio
from tokenize import String
from discord.ext import commands
from discord.utils import get
import googlemaps
import requests
import discord
from dotenv import load_dotenv

# loads the .env file and assign environment variables
load_dotenv() 
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_KEY = os.getenv("GOOGLE_KEY")
google_client = googlemaps.Client(key=GOOGLE_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

async def main():
    """
    main function that starts the Bot
    """
    # storing user input in this list
    

    async with bot:
        await load_all()
        await bot.start(TOKEN)
        # on_ready will run next

@bot.event
async def on_ready():
    """
    runs once the bot establishes a connection with Discord
    """
    try:
        print(f'Logged in as {bot.user}')
        print("Bot ready")
    except Exception as e:
        print(f'Bot not ready {e}')

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


class Questionnaire(discord.ui.Modal, title='Questionnaire Response'):
    name = discord.ui.TextInput(label='Name')
    answer = discord.ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


@bot.command(aliases=['search'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def food_search(ctx, *keywords):

    kw = ' '.join(keywords)
    data = google_foods(kw)

    status = data["status"]
    # if the request is denied we just exit the method and send an error message
    if status ==  'REQUEST_DENIED':
        await ctx.send(f"ERROR\n{data}")
        return

    name = data["results"][0]["name"]
    address = data["results"][0]["formatted_address"]
    status = data["results"][0]["business_status"]
    open_now = data["results"][0]["opening_hours"]
    photo_ref_id = data["results"][0]["photos"][0]["photo_reference"]
    average_rating = data["results"][0]["rating"]
    total_ratings = data["results"][0]["user_ratings_total"]

    google_food_photo(photo_ref_id)
    # adjust the open status of the restaurant
    if open_now["open_now"] == True:
        open_status = "open"
    else:
        open_status = "closed"

    print(name, address, status, open_now, photo_ref_id, average_rating, total_ratings)
    await ctx.send(f"We found you a result for {name}. It's located at {address} and is currently {open_status} and {status.lower()}.\nThis location of {name} has an Average Rating of {average_rating}⭐️/5⭐️, with {total_ratings} total customer ratings!", file=discord.File("./google_search/photo.jpg"))


def google_foods(keyword):
    """
    Use the Google Places API key to search for a restaurant and/or location keyword
    By default google will use current IP location to find a result, unless a location is specified with the keyword
    For example "mcdonalds 90210"
    """
    searchurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" 
    url = searchurl + keyword + "&type=restaurant&key=" + GOOGLE_KEY
    return requests.get(url).json()    
    

def google_food_photo(photo_reference_id):
    """
    Use a provided photo reference id to search for and construct the photo in the google_search directory
    """
    photo_height = 400
    photo_width = 400
    raw_image_data = google_client.places_photo(
        photo_reference=photo_reference_id, max_height=photo_height, max_width=photo_width)
    
    f = open('./google_search/photo.jpg', 'wb+')
    for chunk in raw_image_data:
        if chunk:
            f.write(chunk)
        else:
            print("ALL CHUNKS LOADED")


# @bot.command()
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def detailedfood(ctx, *keywords):
#     # combine the Strings entered in *keywords
#     kw = ' '.join(keywords)
#     google_foods(kw)

#     # open the details.json created in google_foods()
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
#     google_food_photo(photo_ref_id)

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

# # using the place_id generated from google_foods() we can make another API call to get information that textsearch can't get
# # params: placeid - The place_id generated from google_foods()
# def moredetails(placeid):

#     searchurl = "https://maps.googleapis.com/maps/api/place/details/json?place_id="
#     # searchradius = "&radius=" + radius
#     # searchfields = "&fields=formatted_address%2Cname%2Crating%2Cbusiness_status%2Copening_hours%2Cgeometry%2Cphotos"

#     # by default google will use current IP for location when finding a result
#     # create the url request
#     url = searchurl + placeid + "&key=" + GOOGLE_KEY
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

async def load_Cogs():
    """
    Function to load all Cogs that live in the cogs folder
    Ran on Bot startup
    """
    for filename in os.listdir(os.getcwd() + '/cogs'):
        if filename.endswith('.py'):
            try:
                # -3 cuts the .py extension from filename
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Cog {filename} loaded')
            except commands.ExtensionAlreadyLoaded:
                print(f'Cog {filename} aleady loaded')
            except Exception as e:
                print(f'Cog {filename} NOT loaded\n{e}')


async def unload_Cogs():
    """
    Function to unload all Cogs in the cogs folder
    Runs on -rl all
    """
    for filename in os.listdir(os.getcwd() + '/cogs'):
        if filename.endswith('.py'):
            try:
                await bot.unload_extension(f'cogs.{filename[:-3]}')
                print(f'Cog {filename} unloaded successfully')
            except commands.ExtensionNotLoaded:
                print(f'Cog {filename} is not loaded')


async def load_all():
    """
    goes through the /cogs dir and tries to load \
    every file with .py extension
    """
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'{filename} loaded')
            except Exception as e:
                print(f'Could not load {filename}\n{e}')


@bot.command(aliases=['rf', 'rl'], description='Reloads all Cog files')
@commands.has_permissions(administrator=True)
async def refresh(ctx, extension):
    """
    reload cog file, same as doing unload then load, do -refresh "name of cog file" or -rf all
    only admin should be able to run this
    param: ctx - The context in which the command has been executed
    param: extension - The name of the Cog file to reload
    """
    if extension == 'all':
        # unload, then load
        await unload_Cogs()
        await load_Cogs()
        await ctx.send('```Success reloading all cogs```')
    else:
        try:
            print(f'> Reloading {extension}.py --')
            await bot.reload_extension(f'cogs.{extension}')
            print(f'> -- {extension}.py reloaded.')
            await ctx.send(f'```Cog {extension}.py reloaded```')

        except commands.ExtensionNotFound:
            await ctx.send(f'```Cog {extension}.py not in directory```')

        except Exception as e:
            print(f'> -- {extension}.py could not be reloaded \n{e}')
            await ctx.send(f'```Cog {extension}.py could not be reloaded \n{e}```')

asyncio.run(main())








