import discord
from discord.ext import commands
from bot import DATABASE, AUTH, ELO

class Export(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH
        self.elo = ELO

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def export(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if str(ctx.message.author.id) == "150313781673721856": # My discord id
                await self.start_export(ctx)
            else:
                await ctx.send(f'Only administrators can use this command.')

    async def start_export(self, ctx):
        with open("beatmap_ids.txt", "w") as f:
            with open("beatmap_elos_export.txt", "w") as g:
                comp = await self.database.get_all_comparisons()
                beatmaps = await self.database.get_all_beatmaps()
                if beatmaps:
                    for b in beatmaps:
                        self.elo.addPlayer(name=b[0], rating=500)
                if comp:
                    for c in comp:
                        if c[3] == '1':
                            self.elo.gameOver(winner=c[1], loser=c[2], winnerHome=False)
                for beatmap in self.elo.ratingDict:
                    f.write(f"{beatmap}\n")
                    g.write(f"{str(self.elo.ratingDict[beatmap])}\n")

        await ctx.send(f'Elo values exported successfully')

def setup(client):
    client.add_cog(Export(client))