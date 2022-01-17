import discord
from discord.ext import commands
from bot import DATABASE, AUTH, suggestion, ELO
import asyncio

class Confirm(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH
        self.elo = ELO

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def confirm(self, ctx, *args):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if not args:
                await ctx.send(f"Usage: `-confirm 'password'`")
            elif len(args)>1:
                await ctx.send(f"Usage: `-confirm 'password'` (No spaces in the password)")
            elif (len(args[0])<3) or (len(args[0])>4) or not(args[0].isnumeric()):
                await ctx.send(f"Please use a valid password!")
            else:
                user_discord_id = str(ctx.message.author.id)
                user_data = await self.database.get_user(user_discord_id)
                if str(args[0]) != str(user_data[8]):
                    await ctx.send(f"Incorrect password. Please try again")
                else:
                    osu_id = await self.database.get_user_osu_id(user_discord_id)
                    osu_id = osu_id[0]
                    parse_args = []
                    cache = await self.database.get_cache(user_discord_id)
                    order = user_data[9]
                    if order != "":
                        arg_array = []
                        for i in order:
                            arg_array.append(i)
                        for arg in arg_array:
                            parse_args.append(arg)
                        for i, arg in enumerate(arg_array):
                            position = int(arg)+2
                            for k, p in enumerate(parse_args):
                                if arg != p:
                                    second_position = int(p)+2
                                    await self.database.add_comparison(osu_id, cache[position], cache[second_position], "1")
                                    await self.database.add_comparison(osu_id, cache[second_position], cache[position], "2")
                                    ELO.gameOver(winner=cache[position], loser=cache[second_position], winnerHome=False)
                            parse_args.remove(arg)

                        for i, arg in enumerate(arg_array):
                            position = int(arg)+2
                            comparison = await self.database.get_beatmap_comparisons(cache[position])
                            comparison = int(comparison[0]) + 1
                            await self.database.update_comparisons(cache[position], str(comparison))
                        user_comparisons = await self.database.get_user_comparisons(user_discord_id)
                        user_comparisons = int(user_comparisons[0]) + 1
                        await self.database.update_user_comparisons(user_discord_id, user_comparisons)
                        await self.database.update_cache(user_discord_id, "0", [["0"],["0"],["0"],["0"],["0"],["0"],["0"],["0"],["0"],["0"]])
                        await ctx.send(f"Comparison Successful. starting a new comparison..")
                        print(f"Comparison Completed By {user_data[2]}")
                        await self.database.update_order(user_discord_id, "")
                        await asyncio.sleep(1)
                        await suggestion(ctx, user_discord_id)
                    else:
                        await ctx.send(f"You dont have anything to confirm! Try doing `-start` or `-skip`")


def setup(client):
    client.add_cog(Confirm(client))