# TODO

import json
import os
import random
import discord

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
    print("Connected")
    await client.change_presence(activity=discord.Game(name="trying my best <3"))
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")


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
    local_user_data = await DATABASE.get_user(user_discord_id)
    all_beatmaps = await DATABASE.get_all_beatmaps()
    comparison_check = False
    comparison_counter = 0
    while comparison_check == False and comparison_counter < 50:
        random_beatmap = random.randint(0, (len(all_beatmaps)-1))
        random_beatmap_2 = random_beatmap
        while random_beatmap_2 == random_beatmap:
            random_beatmap_2 = random.randint(0, (len(all_beatmaps)-1))
        beatmap_1_id = all_beatmaps[random_beatmap][0]
        beatmap_2_id = all_beatmaps[random_beatmap_2][0]
        if not(await DATABASE.get_user_comparison(local_user_data[1], beatmap_1_id, beatmap_2_id)):
            comparison_check = True
        else:
            comparison_counter = comparison_counter + 1
            comparison_check = False
    if comparison_counter >= 50:
        await ctx.send(f'Could not get a comparison for you at this time. Apparantly all of the possible comparisons you can do have been exhausted! Please contact an admin to confirm this')
    else:
        beatmap_1_data = await AUTH.get_beatmap(beatmap_1_id)
        beatmap_2_data = await AUTH.get_beatmap(beatmap_2_id)
        embed = await EMBED.create_comparison_embed(beatmap_1_data, beatmap_2_data)
        comparison = await ctx.send(embed=embed)
        await DATABASE.update_cache(user_discord_id, comparison.id, beatmap_1_id, beatmap_2_id)

    # await ctx.send(f'\n**__DEBUG DATA__** \nyour osu ign is {local_user_data[2]} - rank {local_user_data[3]} - average SR {local_user_data[4]} - total comparisons {local_user_data[6]} \nbeatmap_1_index: {random_beatmap}, id: {beatmap_1_id}\nbeatmap_2_index: {random_beatmap_2}, id: {beatmap_2_id}')


#  must be final line
if __name__ == '__main__':
    client.run(TOKEN)
