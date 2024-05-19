# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
from dotenv import load_dotenv

import requests

import nextcord
from nextcord.ext import commands
import nextcord.ext
from nextcord import Intents
from nextcord import Client
from nextcord.ext import application_checks
import pickledb
from req import Player

db = pickledb.load('discord.db', True)

GUILD_ID = [1241468028378677308]

intents = Intents.default()
intents.message_content = True

bot = commands.Bot()
client = Client(intents=intents)
#tree = application_command.CommandTree(client)
#client.tree = tree
load_dotenv()

prefix = "!"
'''def get_summoner_data(summoner_name):
    url = RIOT_API_URL.replace('REGION', 'YOUR_REGION') + summoner_name
    headers = {
        'X-Riot-Token': RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
'''

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print("Ready!")

@bot.slash_command(
    name = "addtodb",
    description = "Enter API Key, Game name, and Tagline (no hashtag)",
    guild_ids= GUILD_ID
)
async def addtodb(ctx: nextcord.Interaction, api: str, gamename: str, tagline: str) -> None:
    author = str(ctx.user) # We get the username (RobertK#6151)
    toPrint = ""
    if not db.exists(author+"apikey"): # If username is not already in the database
        db.set(author + "apikey", api)
        toPrint +=(f'API key "{api}" associated with "{ctx.user}" is now registered\n') # Make profile for username in database or it will error
    else: 
        toPrint +=(f'"{api}" already registered with user "{ctx.user}"\n')


    if not db.exists(author+"gamename"): # If username is not already in the database
        db.set(author + "gamename", gamename)
        toPrint +=(f'Game name "{gamename}" associated with "{ctx.user}" is now registered\n') # Make profile for username in database or it will error
    else: 
        toPrint+=(f'"{gamename}" already registered with user "{ctx.user}"\n')
        
    if not db.exists(author+"tagline"): # If username is not already in the database
        db.set(author + "tagline", tagline)
        toPrint+=(f'Tagline "{tagline}" associated with "{ctx.user}" is now registered\n') # Make profile for username in database or it will error
    else: 
        toPrint+=(f'"{tagline}" already registered with user "{ctx.user}"\n')
    await ctx.response.send_message(f'{toPrint}', ephemeral = True)

# ==============Isithas shit code begins

@bot.slash_command(
    name = "dispcurrency",
    description = "Display Currency",
    guild_ids= GUILD_ID
)
async def dispcurrency(ctx: nextcord.Interaction) -> None:
    author = str(ctx.user) # We get the username (RobertK#6151)
    if not db.exists(author+"currency"): # If username is not already in the database
        await ctx.response.send_message(f'Unable to get currency associated with "{ctx.user}"', ephemeral = True) # Make profile for username in database or it will error
    else: 
        curr = db.get(author + "currency")
        await ctx.response.send_message(f'"{ctx.user}" has ${curr} in the bank', ephemeral = True)
    

@bot.slash_command(
    name = "addcurrency",
    description = "Adds Currency if admin",
    guild_ids= GUILD_ID
)
@application_checks.has_permissions(manage_messages=True)
async def addcurrency(ctx: nextcord.Interaction, usr: nextcord.User,add: int):
    author = str(usr) # We get the username (RobertK#6151)
    if not db.exists(author+"currency"): # If username is not already in the database
        db.set(author+"currency", add)
        await ctx.response.send_message(f'No currency count associated "{usr}", adding an entry of ${add}', ephemeral = True) # Make profile for username in database or it will error
    else: 
        db.set(author+"currency", db.get(author+"currency")+add)
        curr = db.get(author + "currency")
        await ctx.response.send_message(f'"{usr}" now has ${curr} in the bank', ephemeral = True)
# ==============Isitha's shit code ends    

class buttonMenu(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label = 'Accept', style=nextcord.ButtonStyle.green)
    async def confirm(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        #this happens when it is pressed 
        await interaction.response.send_message('yes is press', ephemeral=False)
        self.value = True
        self.stop()

    @nextcord.ui.button(label = 'Decline', style=nextcord.ButtonStyle.red)
    async def deny(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        #this happens when it is pressed 
        await interaction.response.send_message('no is press', ephemeral=False)
        self.value = True
        self.stop()

print("cheese!")
# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@bot.slash_command(
    name="duel",
    description="Enter an opponent's discord username to send them a duel invitation",
)
async def duel(interaction: nextcord.Interaction, opponent: nextcord.User) -> None:
    await interaction.response.send_message("Awaiting Opponent Response")
    #gets player 1
    user = await bot.fetch_user(interaction.user.id)
    #gets player 2
    print(user)
    user2 = await bot.fetch_user(opponent.id)
    print(user2)
    
    view = buttonMenu()

    await user2.send("accept or deny the duel lol", view=view)
    await view.wait()

    if view.value is None:
        return
    elif view.value:
        #do this
        print('YAH')
        embed = nextcord.Embed(color= 0xB9F5F1, title='DUEL: ' +user.name+' VS '+user2.name)
        embed.add_field(name=(f"{user.name}\'s KDA").ljust(50),value= (f"{user.name}\'s kda data here").ljust(50), inline=True)
        embed.add_field(name=(f"{user2.name}\'s KDA").rjust(50),value= (f"{user2.name}\'s kda data here").rjust(50),inline=True)

        print(str(user))
        P1 = Player(db.get(str(user) + "apikey"),db.get(str(user)+"gamename"), db.get(str(user)+"tagline"))
        
        await interaction.edit_original_message(content=None, embed=embed)
    #i changed a comment


    else:
        #do that
        print('NOH')
        
    



@bot.slash_command(
    name="cheeseinput",
    description="My first application Command",
    guild_ids = GUILD_ID
)
async def not_first_command(interaction):
    await interaction.response.send_message("cheese!")
    
@bot.slash_command(
    name = "echo",
    description = "asdw",
    guild_ids=GUILD_ID
    )
async def echo(interaction: nextcord.Interaction, message: str) -> None:
    await interaction.response.send_message(message)





@bot.slash_command(
    name="input-userid-api-id",
    description="direct messages the user and grabs a valid input",
    guild_ids=GUILD_ID
)
async def on_message(interaction):
    user = await bot.fetch_user(interaction.user.id)
    await user.send("Hello there!")
    await interaction.response.send_message("sent!")




@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == (prefix + 'changeprefix'):
        await message.channel.send('Okay! what would you like to change it to?')

    if message.content.startswith( prefix + 'hello'):
        await message.channel.send('Hello!')



try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("The Token doesn't exist")
    bot.run(token)
except nextcord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
