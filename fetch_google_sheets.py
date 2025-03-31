import pandas as pd

# Replace with your actual Google Sheet ID
SHEET_ID = "1bq41LpVUed9JT3d3OSgB57WyqoSNocq5Kp8uLVzBdKc"

def fetch_google_sheets_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)
    return df

if __name__ == "__main__":
    df_calls = fetch_google_sheets_data()
    print(df_calls.head())  # Preview data
    df_calls.to_csv("data/call_data.csv", index=False)
