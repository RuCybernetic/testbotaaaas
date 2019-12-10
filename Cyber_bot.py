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
client = commands.Bot(command_prefix='$')

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

@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")

client.run(TOKEN)
