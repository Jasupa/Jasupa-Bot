import discord #Importeer alle code van Discord
from discord.ext import commands #Importeer alle command-commands van Discord

client = commands.Bot(command_prefix = 'ß') #Client variabel maken en prefix zetten

#Wat gebeurt er als de bot klaar is met opstarten?
@client.event
async def on_ready():
    print("De bot is klaar met opstarten!")

#Maak verbinding met Discord en start de bot
client.run(process.env.token)
