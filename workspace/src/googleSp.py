import gspread
import settings
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

json = settings.KEY_JSON
SPREADSHEET_KEY = settings.SPREADSHEET_KEY
credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
gc = gspread.authorize(credentials)


def getAISettings():
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    return worksheet.acell('B3').value
