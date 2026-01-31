from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Load credentials from environment variable or JSON file
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)

# Your spreadsheet ID (from the URL)
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"

def append_row(values):
    """Append a row of values to the first sheet in the spreadsheet"""
    sheet = service.spreadsheets()
    body = {"values": [values]}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1",  # Replace Sheet1 with your tab name
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    print(f"{result.get('updates').get('updatedCells')} cells appended.")