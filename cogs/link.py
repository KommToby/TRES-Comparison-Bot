import discord
from discord.ext import commands
from bot import DATABASE, AUTH

class Link(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def link(self, ctx, *args):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if not args:
                await ctx.send(f'Please provide an osu! id, eg: `-link 12345678`')
            else:
                if args[0].isnumeric():
                    user_data = await self.auth.get_user_data(str(args[0]))
                    if user_data:
                        best_plays = await self.auth.get_user_scores(str(args[0]))
                        average_sr = await self.average_sr_from_top(best_plays)
                        discord_id = str(ctx.message.author.id)
                        user_database = await self.database.get_user( str(discord_id) )
                        if not(user_database):
                            await self.database.add_user(discord_id, str(args[0]), user_data['username'], user_data['statistics']['global_rank'], average_sr, "", 0)
                            await ctx.send(f"user {user_data['username']} has successfully been linked to your discord account!")
                        else:
                            await self.database.update_user(discord_id, str(args[0]), user_data['username'], user_data['statistics']['global_rank'], average_sr, "")
                            await ctx.send(f"user {user_data['username']} is now the osu! account linked to your discord account")
                    else:
                        await ctx.send(f'Please enter a valid user id!')
                else:
                    await ctx.send(f'You need to provide your osu! id, not your osu! username. You can find your osu! id at the end of the url on your profile')

    async def average_sr_from_top(self, data):
        average_sr = 0.00
        for play in data:
            average_sr = average_sr + play['beatmap']['difficulty_rating']
        average_sr = average_sr / 5
        return average_sr

def setup(client):
    client.add_cog(Link(client))