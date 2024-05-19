# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
from dotenv import load_dotenv
import discord
import requests

from discord import Intents
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await tree.sync(guild=discord.Object(id = 1241468028378677308))
    print("Ready!")




# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=1241468028378677308)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
@tree.command(
    name="cheeseinput",
    description="My first application Command",
    guild=discord.Object(id=1241468028378677308)
)
async def not_first_command(interaction):
    await interaction.response.send_message("cheese!")
'''
@tree.command(
    name = "getSummoner"
    description="get summoner data"
    guild=discord.Object(id=1241468028378677308)
    )
async def summoner(ctx, *, summoner_name):
    data = get_summoner_data(summoner_name)
    if data:
        await ctx.send(f"Summoner Name: {data['name']}\nSummoner Level: {data['summonerLevel']}")
    else:
        await ctx.send("Summoner not found or API error.")

'''



@tree.command(
    name="input-userid-api-id",
    description="direct messages the user and grabs a valid input",
    guild=discord.Object(id=1241468028378677308)
)
async def on_message(interaction):
    user = await client.fetch_user(interaction.user.id)
    await user.send("Hello there!")
    await interaction.response.send_message("sent!")




@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == (prefix + 'changeprefix'):
        await message.channel.send('Okay! what would you like to change it to?')

    if message.content.startswith( prefix + 'hello'):
        await message.channel.send('Hello!')



try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("The Token doesn't exist")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
