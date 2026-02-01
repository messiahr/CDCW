from googleapiclient.discovery import build
from google.oauth2 import service_account
import random
import string

# Load credentials from environment variable or JSON file
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)

# Your spreadsheet ID (from the URL)
SPREADSHEET_ID = "1VYT1sS49L1WXsbX8XX3UKdB7aVkjqJRVP8IC5rE4PH4"

# A dictionary that will hold unique IDs mapped to their corresponding rows
id_to_row_map = {}


def generate_unique_id(form_data):
    """Generate a 4-character alphanumeric ID based on the form data."""
    # Concatenate all non-None values string representation
    hash_input = "".join(str(item) for item in form_data if item is not None)
    hash_value = sum(ord(c) for c in hash_input)  # Simple sum of character ordinals
    random.seed(hash_value)
    return "".join(random.choices(string.ascii_letters + string.digits, k=4))


def append_row(values):
    """Append a row of values to the first sheet in the spreadsheet with ID in the leftmost column."""
    generated_id = values[0]  # Assuming the unique ID is the first element in the row

    # Values structure:
    # 0: ID, 1: Name, 2: Age, 3: Gender, 4: Height, 5: Hair Color, 6: Hair Length,
    # 7: Mobility, 8: Features, 9: Additional Info

    distinguishing_features = (
        values[8] if len(values) > 8 else ""
    )  # Features are in column I (index 8)

    # Check if the ID already exists in the hash table
    if generated_id in id_to_row_map:
        # If the ID already exists, retrieve the corresponding row number
        row_number = id_to_row_map[generated_id]
        print(f"ID {generated_id} already exists in row {row_number}.")

        # Fetch the existing row data from the sheet
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                spreadsheetId=SPREADSHEET_ID,
                range=f"IDs!A{row_number}:J{row_number}",  # Fetch columns A to J
            )
            .execute()
        )

        values_in_row = result.get("values", [])

        if values_in_row:
            current_row = values_in_row[0]
            # Ensure the row has enough columns padded
            while len(current_row) < 10:
                current_row.append("")

            # Get existing distinguishing features from column I (index 8)
            existing_features = current_row[8]

            # Combine existing and new distinguishing features, ensuring they are separated by "; "
            if existing_features and distinguishing_features:
                distinguishing_features = (
                    f"{existing_features}; {distinguishing_features}"
                )

            # Prepare updated row
            # We are overwriting other details with the latest submission, but appending features
            updated_row = [
                values[0],  # ID
                values[1],  # Name
                values[2],  # Age
                values[3],  # Gender
                values[4],  # Height
                values[5],  # Hair Color
                values[6],  # Hair Length
                values[7],  # Mobility
                distinguishing_features,  # Merged features
                values[9] if len(values) > 9 else "",  # Additional Info (overwrite)
            ]

            # Update the row
            update_body = {"values": [updated_row]}

            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"IDs!A{row_number}:J{row_number}",
                valueInputOption="USER_ENTERED",
                body=update_body,
            ).execute()
            print(f"Row {row_number} updated.")
    else:
        # If the ID doesn't exist, append a new row to the sheet
        sheet = service.spreadsheets()
        body = {"values": [values]}
        result = (
            sheet.values()
            .append(
                spreadsheetId=SPREADSHEET_ID,
                range="IDs",  # Replace with your actual tab name
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        # Get the new row number from the result (after appending)
        row_number = result["updates"]["updatedRange"].split("!")[1].split(":")[0][1:]
        print(f"Row {row_number} appended.")

        # Update the hash table with the new ID and its corresponding row number
        id_to_row_map[generated_id] = row_number


def get_services():
    """Fetch values from the range G1:Z1 in the 'IDs' sheet"""
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range="Record!B1:Z1",  # Specify the sheet and the range
        )
        .execute()
    )

    values = result.get("values", [])
    if not values:
        print("No data found.")
        return []
    else:
        # Return the list of IDs from the first row
        return values[0]  # Since it's a single row, we get the first list of values


def get_all_records():
    """Fetch all records from columns A to J in the 'IDs' sheet"""
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range="IDs!A2:J",  # Fetch from column A (ID) to J (Additional Information)
        )
        .execute()
    )

    values = result.get("values", [])
    return values
