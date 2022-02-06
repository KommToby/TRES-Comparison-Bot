# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('tres.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
sheet = client.open('TRES')
sheet.add_worksheet(title=f"{dt}", rows="1000", cols="100")
workspace = client.open('TRES').worksheet(f"{dt}")
workspace.append_row(["hello"])
# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)