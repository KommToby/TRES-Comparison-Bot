# TODO

import json
import os
import random
import discord
import asyncio

from discord.ext import commands
import database
import osu_auth
import embed
from help import Help

with open("config.json") as f:
    DISCORD_CONFIG_DATA = json.load(f)["discord"]
    TOKEN = DISCORD_CONFIG_DATA["token"]

GUILD = None
client = commands.Bot(command_prefix="-", case_insensitive=True, help_command=Help())
DATABASE = database.Database()
AUTH = osu_auth.OsuAuth()
EMBED = embed.Embed()

# called when bot is online
@client.event
async def on_ready():
    i = 0
    print("Connected")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
    while True:
        if i != 0:
            await asyncio.sleep(60)
        else:
            i = 1
        comparisons = await DATABASE.get_all_comparisons()
        if comparisons:
            num = (len(comparisons)/2)
            await client.change_presence(activity=discord.Game(name=f"Now with {int(num)} comparisons!"))
        else:
            pass


@client.command(name="load")
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension}")


# Command unloader
@client.command(name="unload")
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Unloaded {extension}")

# "Main" program stored in bot start file
async def suggestion(ctx, user_discord_id):
    suggested_beatmaps = []
    beatmaps_data = []
    all_beatmaps = await DATABASE.get_all_beatmaps()
    for i in range(0, 10):
        random_beatmap = random.randint(0, (len(all_beatmaps)-1))
        random_beatmap_data = all_beatmaps[random_beatmap]
        suggested_beatmaps.append(random_beatmap_data)
        all_beatmaps.remove(all_beatmaps[random_beatmap])
        data = await AUTH.get_beatmap(random_beatmap_data[0])
        beatmaps_data.append(data)
    embed = await EMBED.create_comparison_embed(beatmaps_data)
    comparison = await ctx.send(embed=embed)
    await DATABASE.update_cache(user_discord_id, comparison.id, suggested_beatmaps)


#  must be final line
if __name__ == '__main__':
    client.run(TOKEN)
