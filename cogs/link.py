import discord
from discord.ext import commands


class Link(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def link(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(Link(client))