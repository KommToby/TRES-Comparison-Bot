# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import discord
from discord.ext import commands
from bot import DATABASE, AUTH, ELO

class Export(commands.Cog): # must have commands.cog or this wont work

    def __init__(self, client):
        self.client = client
        self.database = DATABASE
        self.auth = AUTH
        self.elo = ELO

    @commands.Cog.listener() # event within the cog
    async def on_ready(self):
        print('Bot is online.')

    @commands.command() # command within the cog
    async def export(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if str(ctx.message.author.id) == "150313781673721856" or str(ctx.message.author.id) == "163125004995657728" or str(ctx.message.author.id) == "303333305946996905": # My discord id
                await self.start_export(ctx)
            else:
                await ctx.send(f'Only administrators can use this command.')

    async def start_export(self, ctx):
        with open("beatmap_ids.txt", "w") as f:
            with open("beatmap_elos_export.txt", "w") as g:
                comp = await self.database.get_all_comparisons()
                beatmaps = await self.database.get_all_beatmaps()
                # define the scope
                scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

                # add credentials to the account
                creds = ServiceAccountCredentials.from_json_keyfile_name('tres.json', scope)

                # authorize the clientsheet 
                client = gspread.authorize(creds)

                # get the instance of the Spreadsheet
                dt = datetime.now().strftime("%d/%m %H:%M:%S")
                dt = f"Dump {dt}"
                sheet = client.open('TRES')
                sheet.add_worksheet(title=f"{dt}", rows="1000", cols="100")
                workspace = client.open('TRES').worksheet(f"{dt}")
                # workspace.append_row([["a"], ["b"]])
                # row, column
                workspace.update_cell(1, 1, 'Beatmap')
                workspace.update_cell(1, 2, 'Name & Difficulty')
                workspace.update_cell(1, 3, 'Current SR')
                workspace.update_cell(1, 4, 'ELO')
                workspace.update_cell(1, 5, 'rELO')

                if beatmaps:
                    for i, b in enumerate(beatmaps):
                        nelo = open("elo.txt", "r")
                        for j, line2 in enumerate(nelo):
                            if j == i:
                                ELO.addPlayer(name=b[0], rating=float(line2[:-2]))
                if comp:
                    for c in comp:
                        if c[3] == '1':
                            self.elo.gameOver(winner=c[1], loser=c[2], winnerHome=False)
                epic_array = []
                for i, beatmap in enumerate(self.elo.ratingDict):
                    temp_array = []
                    temp_array.append(f"{beatmap}")
                    temp_array.append(f"{beatmaps[i][6]} - {beatmaps[i][7]} [{beatmaps[i][8]}]")
                    temp_array.append(f"{beatmaps[i][1]}")
                    temp_array.append(f"{str(round(float(self.elo.ratingDict[beatmap]), 1))}")
                    temp_array.append(f"{str(round(int(self.elo.ratingDict[beatmap])))}")
                    epic_array.append(temp_array)

                    # also write to file just to be safe
                    f.write(f"{beatmap}\n")
                    g.write(f"{str(self.elo.ratingDict[beatmap])}\n")

                # write all the data
                workspace.update(f"A2:E{i+2}", epic_array)


        await ctx.send(f'Elo values exported successfully')


def setup(client):
    client.add_cog(Export(client))