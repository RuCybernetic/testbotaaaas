import discord
from discord.ext import commands
import os

TOKEN = os.environ.get('BOT_TOKEN')
client = commands.Bot(command_prefix='!')

@client.event
async def on_connect():
    print(f'{client.user} в сети!')
    print('Bot работает.')

@client.command(pass_context=True)
async def привет(ctx):
    await ctx.send('Привет {}'.format(ctx.message.author.mention))

client.run(TOKEN)
