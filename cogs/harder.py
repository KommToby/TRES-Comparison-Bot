import discord
from discord.ext import commands
from bot import DATABASE, AUTH, EMBED, suggestion
import asyncio
import random

class Harder(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH
        self.embed = EMBED

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def harder(self, ctx, *args):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            user_discord_id = str(ctx.message.author.id)
            cache = await self.database.get_cache(user_discord_id)
            if cache:
                if cache[1] != '0':
                    if not args:
                        await ctx.send(f'Please provide which map you believe is harder!')
                    else:
                        if len(args) != 10:
                            await ctx.send(f"You havent provided enough arguments, you should have all numbers 0-9 in the order of hardest to easiest")
                        else:
                            arg_array = []
                            cont = True
                            reason = ""
                            dupenum = ""
                            for arg in args:
                                if len(arg) > 1 or not(arg.isnumeric()):
                                    cont = False
                                    reason = "num"
                                if arg not in arg_array:
                                    arg_array.append(arg)
                                else:
                                    cont = False
                                    reason = "dupe"
                                    dupenum = arg
                            if cont == False:
                                if reason == "num":
                                    await ctx.send(f"Please only provide numbers 0-9 in the order of hardest to easiest, no numbers above 9 should be used, and no letters should be used")
                                elif reason == "dupe":
                                    await ctx.send(f"You provided the value {dupenum} more than once. Please try again, providing numbers 0-9 in the order of hardest to easiest, no numbers above 9 should be used, and no letters should be used")
                            else:
                                if args[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                    await ctx.send(f"Please use correct values! only values 1-9 are acceptable values. Please read the embed to make sure youre choosing the right maps!")
                                else:
                                    await self.database.start_confirmation(user_discord_id)
                                    beatmaps = []
                                    cache = await self.database.get_cache(user_discord_id)
                                    for i, arg in enumerate(arg_array):
                                        pos = int(arg)+2
                                        beatmap_data = await self.auth.get_beatmap(cache[pos])
                                        beatmaps.append(beatmap_data)
                                    
                                    password = random.randint(100, 1000)
                                    password = str(password)
                                    await self.database.update_password(user_discord_id, password)
                                    embed = await self.embed.create_confirmation_embed(beatmaps, user_discord_id, password)
                                    await ctx.send(embed=embed)
                                    order = ""
                                    for arg in arg_array:
                                        order = order + str(arg)
                                    await self.database.update_order(user_discord_id, order)   
                else:
                    await ctx.send(f"You have not got a comparison to make! try doing `-start`")
            else:
                await ctx.send(f"Something went wrong. have you done `-start` or `-link` yet?")


def setup(client):
    client.add_cog(Harder(client))