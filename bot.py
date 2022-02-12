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
            # await client.change_presence(activity=discord.Game(name=f"{100-int(num/45)} user comparisons to go!"))
            await client.change_presence(activity=discord.Game(name=f"{100-int(num/45)} user comparisons to go!"))
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

    l = 0 # THIS IS WHAT IS USED TO DETERMINE HOW MANY RANDOM MAPS THERE ARE!! AT PHASE 2 PLEASE TURN THIS TO 8

    target_beatmaps = []
    Count = 0

    # Determining the set of beatmaps that fit in the elo range
    while Count < l:
        for i, beatmap in enumerate(elo_beatmaps):
            if float(beatmap[1]) > elo_upper or float(beatmap[1]) < elo_lower:
                pass
            else:
                target_beatmaps.append(beatmap)
                elo_beatmaps.remove(beatmap)
        Count = len(target_beatmaps)
        if Count < l:
            elo_upper = elo_upper + 0.1
            if elo_lower < 0.1:
                elo_lower = 0
            else:
                elo_lower = elo_lower - 0.1

    # Maps in target range - compared less
    for i in range(0, l):
        random_beatmap = random.randint(0, (len(target_beatmaps)-1))
        random_beatmap_data = target_beatmaps[random_beatmap]
        beatmaps_sorted = sorted(target_beatmaps, key=lambda x: x[2], reverse=True)
        suggested_beatmaps.append(random_beatmap_data)
        target_beatmaps.remove(target_beatmaps[random_beatmap])
        data = await AUTH.get_beatmap(random_beatmap_data[0])
        beatmaps_data.append(data)

    # for a fix
    beatmap_ids = []
    for b in suggested_beatmaps:
        beatmap_ids.append(b[0])

    # random maps that have been compared less
    beatmaps_not_added = []
    for beatmap in all_beatmaps:
        if beatmap[0] not in beatmap_ids and beatmap[0] not in beatmaps_not_added:
            beatmaps_not_added.append(beatmap)

    beatmaps_sorted = sorted(beatmaps_not_added, key=lambda x: x[2], reverse=False)
    dupe_maps = [] # maps that have the same number of comparisons
    dupe = [] # the number of times the map with the least comparisons has been compared will be stored in here
    while len(dupe_maps) <= 10-l: # while they arent the needed number of less-compared maps in the array
        dupe.append(beatmaps_sorted[0][2])
        for i, j in enumerate(beatmaps_sorted):
            if j[2] in dupe and j not in dupe_maps:
                dupe_maps.append(j)
                beatmaps_sorted.remove(j)

    if len(dupe_maps)>=(10-l): ## if there more or equal needed duplicate maps
        while len(beatmaps_data) < 10: # make sure we're not giving the bot too many maps to compare

            ## This is so we 'shuffle' maps with the same number of comparisons, to ensure that the least compares map are still guaranteed
            used_set = []
            value = -1
            for q, w in enumerate(dupe_maps):
                if q == 0:
                    value = w[2]
                if w[2] == value:
                    used_set.append(w)
                    dupe_maps.remove(w)

            ## Shuffling the used set as found above, and then applying it to the list of maps the bot uses
            random.shuffle(used_set)
            for k, o, in enumerate(used_set):
                if len(beatmaps_data) < 10:
                    suggested_beatmaps.append(o)
                    data = await AUTH.get_beatmap(o[0])
                    beatmaps_data.append(data)

    else:
        for i, j in enumerate(beatmaps_sorted):
            if i < 10-l:
                suggested_beatmaps.append(j)
                data = await AUTH.get_beatmap(j[0])
                beatmaps_data.append(data)

    if len(beatmaps_data) < 10:
        await ctx.send(f'An error occured when collecting beatmaps. Please try again')
    else:
        user_data = await DATABASE.get_user(user_discord_id)
        embed = await EMBED.create_comparison_embed(beatmaps_data, user_data)
        comparison = await ctx.send(embed=embed)
        await DATABASE.update_cache(user_discord_id, comparison.id, suggested_beatmaps)


#  must be final line
if __name__ == '__main__':
    client.run(TOKEN)
