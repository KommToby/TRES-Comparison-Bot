import discord
from discord.ext import commands
from bot import DATABASE, AUTH, suggestion

class Start(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH
        self.suggestion = suggestion

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def start(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            user_discord_id = str(ctx.message.author.id)
            if not(await self.database.get_user(user_discord_id)):
                await ctx.send(f'You need to link your osu id first! use `-link`')
            else:
                cache = await self.database.get_cache(user_discord_id)
                if cache:
                    if cache[1] != "0":
                        await ctx.send(f"you already have a comparison! if you want to skip it, use `-skip`")
                    else:
                        await self.suggestion(ctx, user_discord_id)
                else:
                    await self.suggestion(ctx, user_discord_id)
        else:
            await ctx.send(f'<@{ctx.message.author.id}> Please use commands in DMs with me to prevent spam!')



def setup(client):
    client.add_cog(Start(client))