import discord
from discord.ext import commands
from bot import DATABASE, AUTH, suggestion
import asyncio

class Harder(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def harder(self, ctx, *args):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            user_discord_id = str(ctx.message.author.id)
            cache = await self.database.get_cache(user_discord_id)
            if cache[1] != '0':
                if not args:
                    await ctx.send(f'Please provide which map you believe is harder!')
                else:
                    if len(args) > 1:
                        await ctx.send(f"Please only provide one value for which beatmap is harder. `-harder 1` if the first map is harder, or `-harder 2` if the second map is.")
                    else:
                        if args[0] != "1" and args[0] != "2" and args[0] != "0":
                            await ctx.send(f"Please use correct values! only `1`, `2`, or `0` are acceptable values. Please read the embed to make sure youre choosing the right map!")
                        else:
                            osu_id = await self.database.get_user_osu_id(user_discord_id)
                            osu_id = osu_id[0]
                            if args[0] == "1": # beatmap 1 is harder
                                await self.database.add_comparison(osu_id, cache[2], cache[3], "1")
                                await self.database.add_comparison(osu_id, cache[3], cache[2], "2")
                            elif args[0] == "2": # beatmap 2 is harder
                                await self.database.add_comparison(osu_id, cache[2], cache[3], "2")
                                await self.database.add_comparison(osu_id, cache[3], cache[2], "1")
                            elif args[0] == "0": # beatmaps are basically the same
                                await self.database.add_comparison(osu_id, cache[2], cache[3], "0")
                                await self.database.add_comparison(osu_id, cache[3], cache[2], "0")
                            await self.database.update_cache(user_discord_id, "0", "0", "0")
                            comparisons_1 = await self.database.get_beatmap_comparisons(cache[2])
                            comparisons_2 = await self.database.get_beatmap_comparisons(cache[3])
                            comparisons_1 = int(comparisons_1[0]) + 1
                            comparisons_2 = int(comparisons_2[0]) + 1
                            await self.database.update_comparisons(cache[2], str(comparisons_1))
                            await self.database.update_comparisons(cache[3], str(comparisons_2))
                            user_comparisons = await self.database.get_user_comparisons(user_discord_id)
                            user_comparisons = int(user_comparisons[0]) + 1
                            await self.database.update_user_comparisons(user_discord_id, user_comparisons)
                            await ctx.send(f"Comparison Successful. starting a new comparison..")
                            await asyncio.sleep(1)
                            await suggestion(ctx, user_discord_id)
            else:
                await ctx.send(f"You have not got a comparison to make! try doing `-start`")


def setup(client):
    client.add_cog(Harder(client))