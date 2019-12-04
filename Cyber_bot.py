import discord
from discord.ext import commands
import os

TOKEN = os.environ.get('BOT_TOKEN')
client = commands.Bot(command_prefix='$')

@client.event
async def on_connect():
    print(f'{client.user} в сети!')
    print('Bot работает.')
    
@client.event
async def on_member_join(member):
    id1 = int('634235156713963551')
    id2 = int('639461753041846316')
    if member.guild.id == id1:
        role = discord.utils.get(member.guild.roles, name='new role')
        await member.add_roles(role)
    elif member.guild.id == id2:
        role = discord.utils.get(member.guild.roles, name='гость')
        await member.add_roles(role)
    else:
        pass

@client.command(pass_context=True)
async def привет(ctx):
    await ctx.send('Привет {}'.format(ctx.message.author.mention))

@client.command(pass_context=True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    
@client.command(brief = 'Сделать звонок на сервере')
@commands.has_permissions(administrator = True)
async def call(ctx):
    Guild = ctx.message.guild.id
    channel = ctx.message.author.voice.channel.id
    embed = discord.Embed(colour = 0xff000, description = f'https://discordapp.com/channels/{Guild}/{channel}')
    await ctx.send(embed = embed)

client.run(TOKEN)
