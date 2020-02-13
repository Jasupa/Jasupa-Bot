import discord #Importeer alle code van Discord
import os
import youtube_dl
import spotdl
import sys
import datetime
import random
import colorsys
import ctypes
import ctypes.util

from os import system

from discord.utils import get

from discord.ext import commands #Importeer alle command-commands van Discord

bot = commands.Bot(command_prefix = 'ß') #Client variabel maken en prefix zetten


#Wat gebeurt er als de bot klaar is met opstarten?
@bot.event
async def on_ready():
    print("De bot is klaar met opstarten!")


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice is not None:
        return await voice.move_to(channel)

    await channel.connect()

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
async def play(ctx, *url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'outtmpl': "./song.mp3",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    song_search = " ".join(url)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([f"ytsearch1:{song_search}"])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -ff song -f " + '"' + c_path + '"' + " -s " + song_search)

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07


@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")

queues = {}

@bot.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, *url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    song_search = " ".join(url)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([f"ytsearch1:{song_search}"])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + song_search)


    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")

@bot.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        await ctx.send("Next Song")
    else:
        print("No music playing")
        await ctx.send("No music playing failed")

@bot.command(pass_context=True, aliases=['v', 'vol'])
async def volume(ctx, volume: int):

    if ctx.voice_client is None:
        return await ctx.send("Not connected to voice channel")

    print(volume/100)

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")

@bot.command(pass_context=True, aliases=['wa','wai'])
async def waifu(ctx):

    embed = discord.Embed(color=0xf2fa07)
    embed.set_image(url = random.choice(['https://remilia.cirno.pw/image/36828/7c424239-8414-4234-9c63-a122c57fd3f1.jpg',
    'https://remilia.cirno.pw/image/36828/691b4216-d95b-4068-a9f4-c32edc7bb72c.jpg',
    'https://f0.pngfuel.com/png/906/702/pink-haired-female-character-in-red-top-and-black-pants-outfit-illustration-anime-board-waifu-anime-png-clip-art.png',
    'https://i.pinimg.com/736x/e5/88/20/e5882022981ba6268c3f7cdeac07d971.jpg',
    'https://lh3.googleusercontent.com/dMggJXNJjA3TtcCkbZ7B6ozqqaFqwnBhR942vDmQlu27Npeh1827E89xKraId1b-rA',
    'https://images-na.ssl-images-amazon.com/images/I/51pYggo33jL.jpg',
    'https://i.pinimg.com/originals/da/b2/d4/dab2d405730473923d33a32e814950cd.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTunqBOtJywMoDdBrMGY_st7jhXN9ujq5g6KE7vlwNWb393nTfV',
    'https://i.pinimg.com/originals/40/4f/42/404f42d916449d5d57383ad3df15e6ad.jpg',
    'https://ih0.redbubble.net/image.582060261.0350/flat,800x800,075,f.u1.jpg',
    'https://cache.desktopnexus.com/thumbseg/1903/1903382-bigthumbnail.jpg'
    ]))
    embed.set_footer(text=f"Requested by: {ctx.author.name}")

    await ctx.send(embed=embed)
@bot.command(pass_context=True, aliases=['jas','jasu'])
async def Jasupa(ctx):

    embed = discord.Embed(color=0xf2fa07)
    embed.set_image(url = random.choice([
    'https://i.pinimg.com/originals/0e/8e/7e/0e8e7e3bc609f0a31e308d2fca075d78.png',
    'https://a-static.besthdwallpaper.com/len-kagamine-behang-25446_L.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQ_RrHU90-xSPuZcffKc2GF97FsmmsAhUR05FhxoszuiAUZrpjT',
    'https://www.wallpaperup.com/uploads/wallpapers/2013/10/20/163545/5b70a058875bc581462087daf00ccad4-700.jpg',
    'https://www.itl.cat/pngfile/big/141-1419644_len-rin-kagamine-len-and-rin-kagamine.jpg',
    'https://www.itl.cat/pngfile/big/141-1419713_anime-kosuzume-vocaloid-kagamine-len-kagamine-rin-kagamine.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQOaNoWinIZH_BNOgfbzUZUsZPeeKPVj60y2hoIXVux6WwJ6DaY',
    'https://static.zerochan.net/Kagamine.Len.full.238285.jpg',
    'https://lh3.googleusercontent.com/proxy/ogy4VEEf2V0GH31ODq-LbfZO1SMVjgl2eg8lFC6maTEuE39NkeC---5WjX7OdVRBj5SyZrvR6qCxpk51-kMYx08Vk6P4V6IwYtlwoM0YgGnQdeAzz2MHs_doVBjdQ7a9um4sxJpjIFYzWnW1fA'
    ]))
    embed.set_footer(text=f"Requested by: {ctx.author.name}")

    await ctx.send(embed=embed)


#Maak verbinding met Discord en start de bot
bot.run(os.environ['token'])
