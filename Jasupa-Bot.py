import discord #Importeer alle code van Discord
import os
import youtube_dl

from discord.ext import commands #Importeer alle command-commands van Discord

client = commands.Bot(command_prefix = 'ß') #Client variabel maken en prefix zetten

players = {}

#Wat gebeurt er als de bot klaar is met opstarten?
@client.event
async def on_ready():
    print("De bot is klaar met opstarten!")

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play (ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()






#Maak verbinding met Discord en start de bot
client.run(os.environ['token'])
