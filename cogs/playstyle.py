import discord
from discord.ext import commands
from bot import DATABASE, AUTH

class Playstyle(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def playstyle(self, ctx, *args):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            user_discord_id = str(ctx.message.author.id)
            if not(await self.database.get_user(user_discord_id)):
                await ctx.send(f'You need to link your osu id first! use `-link`')
            else:
                if not args:
                    await ctx.send(f'Please provide a playstyle! e.g. `-playstyle KDDK`')
                else:
                    if not(args[0].isnumeric()) and len(args[0]) == 4:
                        letters = True
                        kcount = 0
                        dcount = 0
                        for letter in args[0]:
                            if letter.upper() == "K":
                                kcount = kcount+1
                            elif letter.upper() == "D":
                                dcount = dcount+1
                            else:
                                letters = False
                        if kcount != 2 or dcount != 2:
                            letters = False
                        if letters is True:
                            await self.database.update_playstyle(user_discord_id, args[0])
                            await ctx.send(f'Playstyle updated! Try doing `-start` to start map comparisons!')
                        else:
                            await ctx.send(f'Please enter a valid playstyle (only two of each Ks and Ds, no spaces)!')
                    else:
                        await ctx.send(f'Please enter a valid playstyle (four characters of Ks and Ds, no spaces)')

def setup(client):
    client.add_cog(Playstyle(client))