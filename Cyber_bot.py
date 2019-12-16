import discord
from discord.ext import commands
from discord.utils import get
import os
import sys
import nacl.utils
import ffmpeg
from sys import path
from discord import opus

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

    raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))

TOKEN = os.environ.get('BOT_TOKEN')
client = commands.Bot(command_prefix='!')
client.load_extension("jishaku")

@client.event
async def on_connect():
    print(f'{client.user} в сети!')
    print('Bot работает.')
    
@client.event
async def on_member_join(member):
    id = 647290681320013825
    if member.guild.id == id:
        role = discord.utils.get(member.guild.roles, name='Гость')
        await member.add_roles(role)
    else:
        pass
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id != 654933197586694156:
        return
    if str(payload.emoji) == "<:LoL:654146562468872214>":
        role = client.get_guild(payload.guild_id).get_role(653834600602402827)
        member = client.get_guild(payload.guild_id).get_member(payload.user_id)
        await member.add_roles(role)
    elif str(payload.emoji) == "<:Hots:654150946456338463>":
        role = client.get_guild(payload.guild_id).get_role(653835527497449472)
        member = client.get_guild(payload.guild_id).get_member(payload.user_id)
        await member.add_roles(role)
    elif str(payload.emoji) == "<:diablo3_2:654159805694476298>":
        role = client.get_guild(payload.guild_id).get_role(653835076853039104)
        member = client.get_guild(payload.guild_id).get_member(payload.user_id)
        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != 654933197586694156:
        return
    if str(payload.emoji) == "<:LoL:654146562468872214>":
        role = client.get_guild(payload.guild_id).get_role(653834600602402827)
        member = client.get_guild(payload.guild_id).get_member(payload.user_id)
        await member.remove_roles(role)
    elif str(payload.emoji) == "<:Hots:654150946456338463>":
        role = client.get_guild(payload.guild_id).get_role(653835527497449472)
        member = client.get_guild(payload.guild_id).get_member(payload.user_id)
        await member.remove_roles(role)
    elif str(payload.emoji) == "<:diablo3_2:654159805694476298>":
        role = client.get_guild(payload.guild_id).get_role(653835076853039104)
        member = client.get_guild(payload.guild_id).get_member(payload.user_id)
        await member.remove_roles(role)

@client.command(aliases=['привет'])
async def hello(ctx):
    await ctx.send('Привет {}'.format(ctx.message.author.mention))

@client.command()
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

@client.command()
async def join(ctx):
	channel = ctx.author.voice.channel.id
	await client.get_channel(int(channel)).connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

client.run(TOKEN)
