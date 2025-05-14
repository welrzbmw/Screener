
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def export_to_google_sheet(df):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Warrior Screener Output").sheet1
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
