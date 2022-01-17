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
from elosports.elo import Elo

with open("config.json") as f:
    DISCORD_CONFIG_DATA = json.load(f)["discord"]
    TOKEN = DISCORD_CONFIG_DATA["token"]

GUILD = None
client = commands.Bot(command_prefix="-", case_insensitive=True, help_command=Help())
DATABASE = database.Database()
AUTH = osu_auth.OsuAuth()
EMBED = embed.Embed()
ELO = Elo(k=40, homefield=0) # Change this to 1/5 of the value when beta ends

# called when bot is online
@client.event
async def on_ready():
    i = 0
    print("Connected.")
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
            await client.change_presence(activity=discord.Game(name=f"{80-int(num/45)} user comparisons to go!"))
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
    
    comp = await DATABASE.get_all_comparisons()
    beatmaps = await DATABASE.get_all_beatmaps()
    if beatmaps:
        for b in beatmaps:
            ELO.addPlayer(name=b[0], rating=500)
    if comp:
        for c in comp:
            if c[3] == '1':
                ELO.gameOver(winner=c[1], loser=c[2], winnerHome=False)

    suggested_beatmaps = []
    beatmaps_data = []
    all_beatmaps = await DATABASE.get_all_beatmaps()
    elo_beatmaps = []
    # Elo application
    for i, beatmap in enumerate(all_beatmaps):
        new = (beatmap[0], str(round(float(ELO.ratingDict[beatmap[0]])/100, 2)), beatmap[2], beatmap[3], beatmap[4], beatmap[5], beatmap[6], beatmap[7], beatmap[8], beatmap[9])
        elo_beatmaps.append(new)

    elo = await DATABASE.get_elo(user_discord_id)
    elo = float(elo[0])
    if elo < 1.5:
        elo = 1.5
    elo_upper = elo + 1.5
    elo_lower = elo - 1.5

    target_beatmaps = []
    Count = 0
    while Count < 8:
        for i, beatmap in enumerate(elo_beatmaps):
            if float(beatmap[1]) > elo_upper or float(beatmap[1]) < elo_lower:
                pass
            else:
                target_beatmaps.append(beatmap)
                elo_beatmaps.remove(beatmap)
        Count = len(target_beatmaps)
        if Count < 8:
            elo_upper = elo_upper + 0.1
            if elo_lower < 0.1:
                elo_lower = 0
            else:
                elo_lower = elo_lower - 0.1

    # Maps in target range - compared less
    for i in range(0, 8):
        random_beatmap = random.randint(0, (len(target_beatmaps)-1))
        random_beatmap_data = target_beatmaps[random_beatmap]
        beatmaps_sorted = sorted(target_beatmaps, key=lambda x: x[2], reverse=True)
        suggested_beatmaps.append(random_beatmap_data)
        target_beatmaps.remove(target_beatmaps[random_beatmap])
        data = await AUTH.get_beatmap(random_beatmap_data[0])
        beatmaps_data.append(data)

    # random maps that have been compared less
    for i in range(0, 2):
        beatmaps_not_added = []
        for beatmap in all_beatmaps:
            if beatmap not in suggested_beatmaps:
                beatmaps_not_added.append(beatmap)

        beatmaps_sorted = sorted(beatmaps_not_added, key=lambda x: x[2], reverse=False)
        for i, j in enumerate(beatmaps_sorted):
            if i < 5:
                suggested_beatmaps.append(j)
                data = await AUTH.get_beatmap(j[0])
                beatmaps_data.append(data)

    if len(beatmaps_data) < 10:
        await ctx.send(f'An error occured when collecting beatmaps. Please try again')
    else:
        embed = await EMBED.create_comparison_embed(beatmaps_data)
        comparison = await ctx.send(embed=embed)
        await DATABASE.update_cache(user_discord_id, comparison.id, suggested_beatmaps)


#  must be final line
if __name__ == '__main__':
    client.run(TOKEN)
