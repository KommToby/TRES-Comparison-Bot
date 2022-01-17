import discord
from discord.ext import commands
from bot import DATABASE, AUTH, ELO

class Import(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH
        self.elo = ELO

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def importb(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if str(ctx.message.author.id) == "150313781673721856": # My discord id
                await self.start_import(ctx)
            else:
                await ctx.send(f'Only administrators can use this command.')

    async def start_import(self, ctx):
        with open("beatmaps.txt", "r") as f:
            for line in f:
                beatmap_id = line.strip()
                beatmap_data = await self.auth.get_beatmap(str(beatmap_id))
                if not(await self.database.get_beatmap((str(beatmap_id)))):
                    await self.database.add_beatmap(str(beatmap_id), beatmap_data['difficulty_rating'], beatmap_data['bpm'], beatmap_data['total_length'], beatmap_data['beatmapset']['artist'], beatmap_data['beatmapset']['title'], beatmap_data['version'], beatmap_data['url'])
                    self.elo.addPlayer(beatmap_id, rating=500)
                else:
                    await ctx.send(f'Error 0x01')
        await ctx.send(f'Beatmaps successfully imported!')

def setup(client):
    client.add_cog(Import(client))