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

@bot.command(pass_context=True, aliases=['j', 'joi'])
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


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")
client.run(TOKEN)
