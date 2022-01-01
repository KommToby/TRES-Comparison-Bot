# TODO

import json
import os

from discord.ext import commands
import database
import osu_auth

with open("config.json") as f:
    DISCORD_CONFIG_DATA = json.load(f)["discord"]
    TOKEN = DISCORD_CONFIG_DATA["token"]

GUILD = None
client = commands.Bot(command_prefix="-")
DATABASE = database.Database()
AUTH = osu_auth.OsuAuth()

# called when bot is online
@client.event
async def on_ready():
    print("Connected")
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


#  must be final line
if __name__ == '__main__':
    client.run(TOKEN)
