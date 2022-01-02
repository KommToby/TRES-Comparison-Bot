import discord
from discord.ext import commands
from bot import DATABASE, AUTH

class Start(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def start(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            user_discord_id = str(ctx.message.author.id)
            if not(await self.database.get_user((user_discord_id,))):
                await ctx.send(f'You need to link your osu id first! use `-link`')




def setup(client):
    client.add_cog(Start(client))