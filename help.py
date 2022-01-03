import discord
from discord.ext import commands

class Help(commands.HelpCommand): # must have commands.cog or this wont work

    # def __init__(self):
    #     self.__init__()

    async def send_bot_help(self, ctx):
        channel = self.get_destination()
        if isinstance(channel, discord.channel.DMChannel):
            embed = discord.Embed(
                title="Taiko Rework ELO System Comparison Bot",
                color=discord.Colour.red()
            )
            embed.add_field(name="Commands",
                            value="`-link`: Links your discord account to your osu! account \n`-start`: Starts or continues (if you want to skip) taiko map comparison \n`-playstyle`: Adds your playstyle to the database (optional)",
                            inline = False)
            await channel.send(embed=embed)
        else:
            await channel.send(f'Please use commands in DMs with me to prevent spam!')


def setup(client):
    client.add_cog(Help(client))