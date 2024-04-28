import os
import time
import discord 
from discord.ext import commands, tasks
from data_collector import Nolus
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.all()
intents.typing = True
intents.presences = True
intents.message_content = True  
bot = commands.Bot(command_prefix="/", intents=intents)

nolus = Nolus()

@bot.event
async def on_ready():
    print(f'You have logged in as {bot.user}')
    await update.start()

@bot.command(name="stats")
async def send_stats(ctx): 
    print (f"Stats command by ~{ctx.author.name}")
    await ctx.send(nolus.message)

@bot.command(name='price')
async def price(ctx): 
    print (f"Stats command by ~{ctx.author.name}")
    await ctx.send(f"``Price of $NLS: {round(nolus.price,3)} $``")

@bot.command(name='deposits')
async def deposits(ctx): 
    print (f"Stats command by ~{ctx.author.name}")
    await ctx.send(f"``Deposits for axl.USDC (Osmosis): {nolus.deposit_check_osmo}``")
    await ctx.send(f"``Deposits for axl.USDC (Neutron): {nolus.deposit_check_ntrn}``")

@bot.command(name='apr')
async def apr(ctx): 
    print (f"Stats command by ~{ctx.author.name}")
    await ctx.send(f"``Yield for axl.USDC (Osmosis): {nolus.apr_osmo}``")
    await ctx.send(f"``Yield for axl.USDC (Neutron): {nolus.apr_ntrn}``")
    await ctx.send(f"``Yield for $NLS staking: {nolus.inflation}``")


@tasks.loop(minutes=2)
async def update():
        print ("Updating...")
        start = time.time()
        await nolus.update_values()
        print("Stats updated in %s seconds" % int(time.time() - start))
        print ("Message Updated at " + (nolus.time_updated))
         
BOT_TOKEN = os.environ.get("DISCORD_KEY")
bot.run(BOT_TOKEN)