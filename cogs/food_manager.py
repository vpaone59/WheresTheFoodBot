import discord
from discord.ext import commands

class Food_Manager(commands.Cog):
    """
    """

    def __init__(self, bot):
        self.bot = bot

        global food_list
        food_list = []


    @commands.Cog.listener()
    async def on_ready(self):
        """
        runs when Cog is loaded and ready to use
        """
        print(f'{self} ready')

   
    @commands.command(aliases=['add_item', 'add'])
    async def add_food(self, ctx, add_on):
        """
        Add a food item to the food list. Takes one String parameter
        """
        if not add_on:
            await ctx.send("Can't add blank or none item")
        elif add_on in food_list:
            await ctx.send("Item already in the list")
        else:
            food_list.append(str(add_on))
            print(food_list)
        food = gather_food_list()
        print(food)
        await ctx.send(food)


    @commands.command(aliases=['list'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def show_food_list(self, ctx):
        """
        Display the food list if there is at least one item
        """
        if len(food_list) == 0:
            await ctx.send("No items in the list")
        else:
            my_list = gather_food_list()
            await ctx.send(my_list)


    @commands.command(aliases=['edit_list', 'edit'])
    async def edit_food_list(self, ctx):
        """
        A function built with button views to allow the user to easily edit the food list using buttons, inputs, etc
        """
        await ctx.send('Choose an option:', view=Edit_Food_List())


class Edit_Food_List(discord.ui.View):
        """
        View that shows the buttons for the edit food list command
        """
        global food_list

        def __init__(self, *, timeout=None):
            super().__init__(timeout=timeout)

        @discord.ui.button(label="Show List", style=discord.ButtonStyle.blurple)
        async def show_items_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            food = gather_food_list()
            await interaction.response.send_message(food)

        @discord.ui.button(label="Add Item", style=discord.ButtonStyle.blurple)
        async def add_item_button(self, interaction: discord.Interaction, button: discord.ui.Button,):
            await interaction.response.send_message("Add item")

        @discord.ui.button(label="Remove Item", style=discord.ButtonStyle.red)
        async def remove_item_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Remove item")

        # @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
        # async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        #     await interaction.message.delete()


async def gather_food_list():
    """
    """
    if len(food_list) == 0:
        list_of_food = "No items in the list"
    else:
        list_of_food = ''
        for f in food_list:
            list_of_food += f + '\n'

    return list_of_food


async def setup(bot):
    await bot.add_cog(Food_Manager(bot))