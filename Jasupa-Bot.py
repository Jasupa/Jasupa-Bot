import discord #Importeer alle code van Discord
import os
import youtube_dl

from discord.ext import commands #Importeer alle command-commands van Discord

client = commands.Bot(command_prefix = 'ß') #Client variabel maken en prefix zetten

#Wat gebeurt er als de bot klaar is met opstarten?
@client.event
async def on_ready():
    print("De bot is klaar met opstarten!")

@bot.commands(pass_context=True, aliases=['j','joi'])
async def join(ctx):
    global voice
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
        voice = await channel.connect():
        print("De bot is verbonden met {channel}\n")
    
    await ctx.send("{channel} gejoined")



#Maak verbinding met Discord en start de bot
client.run(os.environ['token'])
