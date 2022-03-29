# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import discord
from discord.ext import commands
from bot import DATABASE, AUTH, ELO

class Verify(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH
        self.elo = ELO

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def verify(self, ctx, *args):
        if str(ctx.message.author.id) == "150313781673721856" or str(ctx.message.author.id) == "163125004995657728" or str(ctx.message.author.id) == "303333305946996905": # My discord id
            if not args:
                await ctx.send(f'Please provide an osu! id')
            elif len(args) > 1:
                await ctx.send(f'Please only provide one osu id')
            else:
                try:
                    await self.database.verify_user(args[0])
                    user = await self.database.get_user_from_osu_id(args[0])
                    message = await ctx.send(f'User {user[2]} successfully verified')
                    await message.edit(content=f'User {user[2]} successfully verified (<@{user[0]}>)')
                    guild_s = self.client.get_guild(898883144726495314)
                    user_id_int = int(user[00])
                    member = guild_s.get_member(user_id_int)
                    channel = await member.create_dm()
                    await channel.send(f'You have been verified! you can now get started by using `-elo')
                except:
                    await ctx.send(f'Verification failed, Please check logs')
                    # if the above is sent, is the user in the discord?
        else:
            await ctx.send(f'Only administrators can use this command.')


def setup(client):
    client.add_cog(Verify(client))