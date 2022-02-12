import discord
from discord.ext import commands

from bot import DATABASE, AUTH

class Users(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def users(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if str(ctx.message.author.id) == "150313781673721856" or str(ctx.message.author.id) == "163125004995657728" or str(ctx.message.author.id) == "303333305946996905": # My discord id
                message_string = await self.create_string()
                await ctx.send(message_string) 
            else:
                await ctx.send("You do not have permissions for this command")

        elif str(ctx.message.channel.id) == "898907991653376072":
            if str(ctx.message.author.id) == "150313781673721856" or str(ctx.message.author.id) == "163125004995657728" or str(ctx.message.author.id) == "303333305946996905": # My discord id
                message_string = await self.create_string()
                await ctx.send(message_string) 
            else:
                await ctx.send("You do not have permissions for this command")

    async def create_string(self):
        users = await DATABASE.get_all_users()
        message_string = "```css\n"
        max_name_length = 0
        most_comparisons = 0
        for user in users:
            if len(str(user[2])) > max_name_length:
                max_name_length = len(str(user[2]))
            if int(user[6]) > most_comparisons:
                most_comparisons = int(user[6])
        max_name_length = max_name_length+1
        total_comparisons = await DATABASE.get_all_comparisons()
        message_gap = " " * (max_name_length-len("Username"))
        message_string = message_string + f"[Username{message_gap} (Elo) | Streak | Comparisons] ({round(len(total_comparisons)/90)} total)\n"
        users = sorted(users, key=lambda x: x[4], reverse=False)
        for user in users:
            user_gap = " " * (max_name_length-len(user[2]))
            streak_gap = " " * (len("Streak ") - len("10"))
            message_string = message_string + f" {user[2]}{user_gap} ({round(float(user[4]), 1)}) | {user[11]}{streak_gap} | {user[6]} Cs"
            if int(user[6]) == most_comparisons:
                message_string = message_string + f" <- Most!\n"
            else:
                message_string = message_string + f"\n"
        message_string = message_string + "```"
        return message_string


def setup(client):
    client.add_cog(Users(client))