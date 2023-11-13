import requests
import pandas as pd
from io import StringIO


def get_form_responses():
    # Google Sheets URL
    sheet_url = 'sheetsurl.com'

    # Send a GET request to retrieve the CSV content of the Google Sheet
    response = requests.get(sheet_url)

    if response.status_code == 200:
        # Convert the CSV content to a DataFrame
        df = pd.read_csv(StringIO(response.text))

        # Get the last row as values
        last_row = df.iloc[-1]

        # Initialize the form_responses_json as a list
        form_responses_json = []

        current_dict = {}
        is_additional_pdu = False

        for column_name, value in last_row.items():
            if not pd.isna(value):
                if "Is there an additional PDU" in column_name:
                    is_additional_pdu = (value == "Yes")
                    if is_additional_pdu:
                        form_responses_json.append(current_dict)
                        current_dict = {"Is there an additional PDU?": value}
                else:
                    current_dict[column_name] = value

        # Append the last response
        form_responses_json.append(current_dict)

        # Remove any empty dictionaries from the list
        form_responses_json = [d for d in form_responses_json if d]

        updated_list = []
        for item in form_responses_json:
            new_item = {}
            for key, value in item.items():
                # Remove ".x" from the keys if it's present
                new_key = key.split('.')[0]
                new_item[new_key] = value
            updated_list.append(new_item)
    return updated_list
    
