import os
from dotenv import load_dotenv

import requests
import time
import asyncio


import nextcord
from nextcord.ext import commands
import nextcord.ext
from nextcord import Intents
from nextcord import Client
from nextcord.ext import application_checks
import pickledb
from apiRiot import Player, in_same_game
import tracemalloc
db = pickledb.load('discord.db', True)
db.set("Player 1", "")
db.set("Player 2", "")
inprogress = 0
GUILD_ID = [1241468028378677308]

intents = Intents.default()
intents.message_content = True

bot = commands.Bot()
client = Client(intents=intents)
load_dotenv()
tracemalloc.start()
better_list = []
prefix = "!"

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print("Ready!")

@bot.slash_command(
    name = "addtodb",
    description = "Enter API Key, Game name, and Tagline (no hashtag)",
    guild_ids= GUILD_ID
)
async def addtodb(ctx: nextcord.Interaction, api: str, gamename: str, tagline: str) -> None:
    author = str(ctx.user)
    toPrint = ""
    if not db.exists(author+"apikey"):
        db.set(author + "apikey", api)
        toPrint +=(f'API key "{api}" associated with "{ctx.user}" is now registered\n') 
    else: 
        toPrint +=(f'"{api}" already registered with user "{ctx.user}"\n')


    if not db.exists(author+"gamename"):
        db.set(author + "gamename", gamename)
        toPrint +=(f'Game name "{gamename}" associated with "{ctx.user}" is now registered\n')
    else: 
        toPrint+=(f'"{gamename}" already registered with user "{ctx.user}"\n')
        
    if not db.exists(author+"tagline"): 
        db.set(author + "tagline", tagline)
        toPrint+=(f'Tagline "{tagline}" associated with "{ctx.user}" is now registered\n') 
    else: 
        toPrint+=(f'"{tagline}" already registered with user "{ctx.user}"\n')
    await ctx.response.send_message(f'{toPrint}', ephemeral = True)



@bot.slash_command(
    name = "dispcurrency",
    description = "Displays currency amount you have",
    guild_ids= GUILD_ID
)
async def dispcurrency(ctx: nextcord.Interaction) -> None:
    author = str(ctx.user)
    if not db.exists(author+"currency"): 
        await ctx.response.send_message(f'Unable to get currency associated with "{ctx.user}"', ephemeral = True) 
    else: 
        curr = db.get(author + "currency")
        await ctx.response.send_message(f'"{ctx.user}" has ${curr} in the bank', ephemeral = True)
    

@bot.slash_command(
    name = "cancel",
    description = "Cancels current match",
    guild_ids = GUILD_ID
)
async def cancel(ctx: nextcord.Interaction) -> None:
    global inprogress
    global better_list
    if inprogress == 0:
        await ctx.response.send_message('No match in progress', ephemeral = True) 
    else: 
        inprogress == 0
        better_list = []
        await ctx.response.send_message('Match in progress cancelled') 

@bot.slash_command(
        name = "claim",
        description = "Claim your daily betting allowance",
    guild_ids = GUILD_ID
)
async def test(ctx: nextcord.Interaction) -> None:
    author = str(ctx.user) # We get the username (RobertK#6151)
    if not db.exists(author+"currency"): # If username is not already in the database
        await ctx.response.send_message(f'Unable to get currency associated with "{ctx.user}"', ephemeral = True) # Make profile for username in database or it will error
    else:
        curr = db.get(author + "currency")
        curr+= 1000
        await ctx.response.send_message(f'"{ctx.user}" now has ${curr} in the bank', ephemeral = True)

@commands.cooldown(1, 300, commands.BucketType.user)      
async def my_command(ctx):
    await ctx.send("Claimed!")

# CD
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {int(error.retry_after)} seconds.")
    else:
        raise error

@bot.slash_command(
    name = "addcurrency",
    description = "Adds currency (admin only)",
    guild_ids= GUILD_ID
)
@application_checks.has_permissions(administrator=True)
async def addcurrency(ctx: nextcord.Interaction, usr: nextcord.User,add: int):
    author = str(usr) 
    if not db.exists(author+"currency"): 
        await ctx.response.send_message(f'No currency count associated "{usr}", adding an entry of ${add}', ephemeral = True) 
        db.set(author+"currency", add)
    else: 
        db.set(author+"currency", db.get(author+"currency")+add)
        curr = db.get(author + "currency")
        await ctx.response.send_message(f'"{usr}" now has ${curr} in the bank', ephemeral = True)


@bot.slash_command(
    name = "bet",
    description = "Double or nothing, bet-to-win is for singles mode only, useless otherwise",
    guild_ids= GUILD_ID
)
async def bet(ctx: nextcord.Interaction, usr: nextcord.User, amt: int, bet_to_win: bool):
    author = str(ctx.user) 
    global inprogress
    global better_list
   
    if ctx.user.id in better_list:
        await ctx.response.send_message(f'Invalid bet: You have already made a bet', ephemeral = True)
    else:
        better_list.append(ctx.user.id)
        if inprogress == 0:
            await ctx.response.send_message(f'Invalid bet: No match in progress', ephemeral = True)
        elif not db.exists(author+"currency"):
            await ctx.response.send_message(f'Invalid bet: You do not have any currency, please ask an admin to start', ephemeral = True)
        elif amt <= 0:
            await ctx.response.send_message(f'Invalid bet: Please enter a positive integer for your bet', ephemeral = True)
        elif int(db.get(author + "currency")) < amt:
            await ctx.response.send_message(f'Invalid bet: You are too poor bet this amount', ephemeral = True)
        elif db.get("Player 1") ==db.get("Player 2"):
            if bet_to_win == True:
                db.set(author+"betamt", amt)
                db.set(author+"betusr", "W"+str(usr))
                await ctx.response.send_message(f'"{ctx.user}" bets ${amt} on "{usr}" to win')
            else:
                db.set(author+"betamt", amt)
                db.set(author+"betusr", "L"+str(usr))
                await ctx.response.send_message(f'"{ctx.user}" bets ${amt} on "{usr}" to lose')
        elif db.get("Player 1") == str(usr) or db.get("Player 2") == str(usr):
            db.set(author+"betamt", amt)
            db.set(author+"betusr", str(usr))
            await ctx.response.send_message(f'"{ctx.user}" bets ${amt} on "{usr}"')
        else:
            await ctx.response.send_message(f'"{usr}" is not currently in a match', ephemeral = True) 

class buttonMenu(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label = 'Accept', style=nextcord.ButtonStyle.green)
    async def confirm(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        await interaction.response.send_message('You have pressed: Accept', ephemeral=False)
        self.value = True
        self.stop()

    @nextcord.ui.button(label = 'Decline', style=nextcord.ButtonStyle.red)
    async def deny(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        await interaction.response.send_message('You have pressed: Decline', ephemeral=False)
        self.value = True
        self.stop()
class singleButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label = 'Match Over', style=nextcord.ButtonStyle.blurple)
    async def matchover(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        await interaction.response.send_message('Match is now over: see updated embed for results', ephemeral=False)
        self.value = True
        self.stop()
    @nextcord.ui.button(label = 'Cancel', style=nextcord.ButtonStyle.red)
    async def cancel2(self, button:nextcord.ui.Button, ctx:nextcord.Interaction):
        global inprogress
        global better_list
        if inprogress == 0:
            await ctx.response.send_message('No match in progress', ephemeral = True) 
        else: 
            inprogress == 0
            better_list = []
            await ctx.response.send_message('Match in progress cancelled') 
        self.value = False
        self.stop()

class canButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label = 'Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button:nextcord.ui.Button, ctx:nextcord.Interaction):
        global inprogress
        global better_list
        if inprogress == 0:
            await ctx.response.send_message('No match in progress', ephemeral = True) 
        else: 
            inprogress == 0
            better_list = []
            await ctx.response.send_message('Match in progress cancelled') 
        self.value = True
        self.stop()


print("cheese!")



@bot.slash_command(
    name="choose-winner",
    description="Choose the winner of the ongoing duel",
)
async def chooseWinner(interaction: nextcord.Interaction, winner: nextcord.User) -> None:
    global better_list
    global inprogress
    if inprogress == 1:
        player1 = db.get("Player 1")
        player2 = db.get("Player 2")
        if str(winner) == player1 or str(winner) == player2:
            winbed = nextcord.Embed(color= 0x6DDE62, title='DUEL RESULTS: ' +str(player1)+' VS '+str(player2))
            winbed.add_field(name ="WINNER".center(50), value=f"CHAMPION: :sparkles: {winner} :sparkles:".center(50))
            await interaction.send(content=None,embed=winbed)
            for i in better_list:
                tempu = await bot.fetch_user(i)
                if db.get(str(tempu)+"betusr") == str(winner): 
                    db.set(str(tempu)+"currency",str(int(db.get(str(tempu)+"betamt")) + int(db.get(str(tempu)+"currency"))))
                    await tempu.send(f"Your bet of ${db.get(str(tempu)+'betamt')} has hit! Your balance is now ${db.get(str(tempu)+'currency')}")
                else:
                    db.set(str(tempu)+"currency",str(int(db.get(str(tempu)+"currency")) - int(db.get(str(tempu)+"betamt"))))
                    await tempu.send(f"Your bet of ${db.get(str(tempu)+'betamt')} did not hit! Your balance is now ${db.get(str(tempu)+'currency')}")
            better_list= []
            inprogress = 0
        else:
            await interaction.response.send_message("Inputted winner was not in the match")
    else: 
        await interaction.response.send_message("No match in progress/Match was cancelled")

@bot.slash_command(
    name="duel",
    description="Enter an opponent's discord username to send them a duel invitation",
    guild_ids = GUILD_ID
)
async def duel(interaction: nextcord.Interaction, opponent: nextcord.User) -> None:
    global inprogress
    global better_list
    if inprogress == 1:
        await interaction.response.send_message("Match already in progress. Please wait for it to end.")
    else:
        better_list = []
        await interaction.response.send_message("Awaiting Opponent Response")
        user = await bot.fetch_user(interaction.user.id)
        db.set("Player 1",str(user))
        user2 = await bot.fetch_user(opponent.id)
        db.set("Player 2", str(user2))
        
        view = buttonMenu()
        can = canButton()

        await user2.send("Please accept or deny", view=view)
        await view.wait()

        if view.value is None:
            return
        elif view.value:
            inprogress = 1
            embed = nextcord.Embed(color= 0xB9F5F1, title='DUEL: ' +user.name+' VS '+user2.name)
            
            await interaction.edit_original_message(content=None, embed=embed, view = can)
            await can.wait()
            if can.value == True:
                inprogress = 0
                better_list= []



@bot.slash_command(
    name="single",
    description="Enter your Discord username to start a match",
    guild_ids = GUILD_ID
)
async def singles(interaction: nextcord.Interaction) -> None:
    global inprogress
    global better_list
    if inprogress == 1:
        await interaction.response.send_message("Match already in progress. Please wait for it to end.")
    else:
        better_list = []
        await interaction.response.send_message("Singles betting started")
        user = await bot.fetch_user(interaction.user.id)
        db.set("Player 1",str(user))
        db.set("Player 2",str(user))
        
        inprogress = 1
        embed = nextcord.Embed(color= 0xB9F5F1, title='SINGLE: ' +user.name)
        P1 = Player(db.get(str(user) + "apikey").strip(),db.get(str(user)+"gamename").strip(), db.get(str(user)+"tagline").strip())
        


    # =================Isitha was involved here proceed with caution ================    
        P1 = Player(db.get(str(user) + "apikey") , db.get(str(user) + "gamename"), db.get(str(user) + "tagline"))
        veew = singleButton()
        await interaction.edit_original_message(content=None, embed=embed, view = veew)
        await veew.wait()

        if inprogress==0 or veew.value == False:
            interaction.edit_original_message(content="MATCH CANCELLED", embed=embed)
            inprogress = 0
            better_list= []
            return
        else:
            match = P1.get_most_recent_match()
                #add function for checking who won
            for i in better_list:
                tempu = await bot.fetch_user(i)
                if P1.won_game(match):
                    if db.get(str(tempu)+"betusr")[1] == "W":
                        db.set(str(tempu)+"currency",str(int(db.get(str(tempu)+'betamt')) + int(db.get(str(tempu)+'currency'))))
                        await tempu.send(f"Your bet of ${db.get(str(tempu)+'betamt')} has hit! Your balance is now ${db.get(str(tempu)+'currency')}")
                    else:
                        db.set(str(tempu)+"currency",str(int(db.get(str(tempu)+"currency")) - int(db.get(str(tempu)+"betamt"))))
                        await tempu.send(f"Your bet of ${db.get(str(tempu)+'betamt')} did not hit! Your balance is now ${db.get(str(tempu)+'currency')}")
                else:
                    if db.get(str(tempu)+"betusr")[1] == "L":
                        db.set(str(tempu)+"currency",str(int(db.get(str(tempu)+'betamt')) + int(db.get(str(tempu)+'currency'))))
                        await tempu.send(f"Your bet of ${db.get(str(tempu)+'betamt')} has hit! Your balance is now ${db.get(str(tempu)+'currency')}")
                    else:
                        db.set(str(tempu)+"currency",str(int(db.get(str(tempu)+"currency")) - int(db.get(str(tempu)+"betamt"))))
                        await tempu.send(f"Your bet of ${db.get(str(tempu)+'betamt')} did not hit! Your balance is now ${db.get(str(tempu)+'currency')}")
            better_list= []
            inprogress = 0
        
            winbed = nextcord.Embed(color= 0x6DDE62, title='SINGLE MATCH RESULTS: ' +str(user))
            if P1.won_game(match):
                winbed.add_field(name ="WIN".center(50), value=f"CHAMPION: :sparkles: {user} :sparkles:".center(50))
            else:
                winbed.add_field(name ="LOSE".center(50), value=f"FALIURE: :raincloud: {user} :raincloud:".center(50))
            await interaction.edit_original_message(content=None,embed=winbed)


    
@bot.slash_command(
    name = "echo",
    description = "asdw",
    guild_ids=GUILD_ID
    )
async def echo(interaction: nextcord.Interaction, message: str) -> None:
    await interaction.response.send_message(message)



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
tracemalloc.stop()