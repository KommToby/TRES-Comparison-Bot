import discord
from discord.ext import commands

from bot import DATABASE, AUTH

class Collect(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def collect(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if str(ctx.message.author.id) == "150313781673721856": # My discord id
                await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(Collect(client))