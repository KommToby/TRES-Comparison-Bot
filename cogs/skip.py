import discord
from discord.ext import commands
from bot import DATABASE, AUTH, suggestion
import asyncio

class Skip(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def skip(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            user_discord_id = str(ctx.message.author.id)
            user = await self.database.get_user(user_discord_id)
            if (await self.database.get_user(user_discord_id)):
                await self.database.update_cache(user_discord_id, "0", "")
                print(f"User {user[2]} skipped their comparison")
                await ctx.send(f"Comparison skipped. Starting a new comparison..")
                await asyncio.sleep(1)
                await suggestion(ctx, user_discord_id)
            else:
                await ctx.send(f"Please use `-link`! The bot has been reset and/or you havent signed up yet!")
                pass


def setup(client):
    client.add_cog(Skip(client))