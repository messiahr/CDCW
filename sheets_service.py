from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load credentials from environment variable or JSON file
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)

# Your spreadsheet ID (from the URL)
SPREADSHEET_ID = "1VYT1sS49L1WXsbX8XX3UKdB7aVkjqJRVP8IC5rE4PH4"

def append_row(values):
    """Append a row of values to the first sheet in the spreadsheet"""
    sheet = service.spreadsheets()
    body = {"values": [values]}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="IDs",  # Replace Sheet1 with your tab name
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    print(f"{result.get('updates').get('updatedCells')} cells appended.")
    
def get_ids():
    """Fetch values from the range G1:Z1 in the 'IDs' sheet"""
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="IDs!G1:Z1"  # Specify the sheet and the range
    ).execute()
    
    values = result.get('values', [])
    
    if not values:
        print("No data found.")
        return []
    else:
        # Return the list of IDs from the first row
        return values[0]  # Since it's a single row, we get the first list of values
