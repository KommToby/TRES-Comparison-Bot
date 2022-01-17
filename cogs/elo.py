import discord
from discord.ext import commands
from bot import DATABASE, AUTH
import asyncio

class Elo(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def elo(self, ctx, *args):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            user_discord_id = str(ctx.message.author.id)
            if not(await self.database.get_user(user_discord_id)):
                await ctx.send(f'You need to link your osu id first! use `-link`')
            else:
                if not args:
                    await ctx.send(f'Please provide a target star rating! e.g. `-elo 5.5`')
                else:
                    try:
                        sr = float(args[0])
                        if sr > 0.00:
                            if sr > 20.00:
                                await ctx.send(f'wtf')
                                await asyncio.sleep(3)
                                await ctx.send(f'can u put a normal sr number in please')
                            else:
                                await self.database.update_SR(user_discord_id, args[0])
                                await ctx.send(f'your elo/sr target is updated! Try doing `-start` to start map comparisons!')
                        else:
                            await ctx.send(f'Please enter a positive SR value -.-')
                    except ValueError:
                        await ctx.send(f'Please enter a valid Elo! (must be a decimal star rating, like 3.25)')


def setup(client):
    client.add_cog(Elo(client))