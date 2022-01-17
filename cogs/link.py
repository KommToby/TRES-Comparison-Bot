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
                        if best_plays:
                            average_sr = await self.average_sr_from_top(best_plays)
                            discord_id = str(ctx.message.author.id)
                            user_database = await self.database.get_user( str(discord_id) )
                            if not(user_database): # If the user has not linked before, add a new user to the database AND add a cache
                                await self.database.add_user(discord_id, str(args[0]), user_data['username'], user_data['statistics']['global_rank'], average_sr, "", 0)
                                await self.database.add_cache(discord_id)
                                await ctx.send(f"user {user_data['username']} has successfully been linked to your discord account! Try doing `-elo` before starting your comparisons!")
                                print(f"Added {user_data['username']} as a user")
                            else: # Otherwise, update the users data in the database to the new osu account
                                await self.database.update_user(discord_id, str(args[0]), user_data['username'], user_data['statistics']['global_rank'], average_sr, "")
                                await ctx.send(f"user {user_data['username']} is now the osu! account linked to your discord account! Try doing `-elo` before starting your comparisons!")
                                print(f"Updated {user_data['username']}'s data")
                        else:
                            await ctx.send(f'An error occured. This user has either not played taiko! enough, or there was an api issue. Please try again')
                    else:
                        await ctx.send(f'Please enter a valid user id!')
                else:
                    await ctx.send(f'You need to provide your osu! id, not a username, or url. You can find your id at the end of your profile url!')

    async def average_sr_from_top(self, data):
        average_sr = 0.00
        for play in data:
            average_sr = average_sr + play['beatmap']['difficulty_rating']
        average_sr = average_sr / 5
        return average_sr

def setup(client):
    client.add_cog(Link(client))