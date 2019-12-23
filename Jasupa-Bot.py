import discord #Importeer alle code van Discord
import os
import wavelink
from os import system

if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus.so')

from discord.utils import get

from discord.ext import commands #Importeer alle command-commands van Discord

bot = commands.Bot(command_prefix = 'ß') #Client variabel maken en prefix zetten

class Bot(commands.Bot):

    def __init__(self):
        super(Bot, self).__init__(command_prefix=['audio ', 'wave ','aw '])

        self.add_cog(Music(self))

    async def on_ready(self):
        print(f'Logged in as {self.user.name} | {self.user.id}')


class Music:

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='0.0.0.0',
                                              port=80,
                                              rest_uri='http://0.0.0.0:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='us_central')

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f'Added {str(tracks[0])} to the queue.')
        await player.play(tracks[0])
        
    @commands.command(name='repeat')
    async def repeat_(self, ctx):
        """Repeat the currently playing song.
        Examples
        ----------
        <prefix>repeat
            {ctx.prefix}repeat
        """
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=Player)

        if not player.is_connected:
            return

        if await self.has_perms(ctx, manage_guild=True):
            await ctx.send(f'I am now repeating the song. Requested by {ctx.author.mention}', delete_after=25)
            return await self.do_repeat(ctx)

        await self.do_vote(ctx, player, 'repeat')

    async def do_repeat(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=Player)

        if not player.entries:
            await player.queue.put(player.current)
        else:
            player.queue._queue.appendleft(player.current)

        player.update = True    


#Maak verbinding met Discord en start de bot
bot.run(os.environ['token'])
