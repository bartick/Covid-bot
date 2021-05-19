import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time

load_dotenv()

def get_prefix(bot, message):
    if message.content.split()[0][1:] == 'state':
        return '?'
    else:
        return ['B.','b.']

bot = commands.Bot(command_prefix=get_prefix, help_command=None, activity=discord.Game(name='For covid data \n?state [state code]'))

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

@bot.command(
    name='ping',description='Shows you bots current latency'
    )
async def ping(ctx):
    before = time.monotonic()
    before_ws = int(round(bot.latency * 1000, 1))
    message = await ctx.send("🏓 Pong")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}')

if __name__=='__main__':
    bot.run(os.getenv('TOKEN'))