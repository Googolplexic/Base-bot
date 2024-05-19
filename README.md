# Python Discord Bot
By:
William Chen https://github.com/Willywum
Isitha Tennakoon https://github.com/IsithaT
Coleman Lai https://github.com/Googolplexic
Howard Jin https://github.com/Wurrd

All SFU CS first years

Python Discord bot using nextcord.
built on a discord starter from 
https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
and manipulated to work with nextcord for the Stormhacks 2024 hackathon

first time doing a hackathon for all of us but it was fun

the bot lets you duel your friends in league of legends as well as other games
your other friends can bet fake internet points on who might win

reads the league API to get last game data for singles mode

the choose-winner slash command was implemented after we realized
that we had to apply to a product forum on the riot developer website
to get private match data, as it is considered private

so we had to compromise and make this slash command.
if we had the time, the path we would take is to get the oauth
from riot to be able to access private matches and we would be able to 
use the riot api to verify and complete matches

i dont know what else you need to know, so go have fun
wait no
you need to change the GUILD_ID to match the id of the server the bot is invited to
and you need to make a .env file to store the TOKEN for the bot.



