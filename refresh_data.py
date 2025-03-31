import fetch_google_sheets
import fetch_shopify_data
import merge_data
import schedule
import time

def refresh_data():
    print("🔄 Fetching latest call data...")
    fetch_google_sheets.fetch_google_sheets_data()
    
    print("🔄 Fetching latest Shopify orders...")
    fetch_shopify_data.fetch_shopify_orders()
    
    print("🔄 Merging data...")
    merge_data.merge_data()

    print("✅ Data updated successfully!")

def schedule_daily_refresh():
    # Schedule the refresh_data function to run every day at a specific time (e.g., 00:00)
    schedule.every().day.at("00:00").do(refresh_data)
    print("⏰ Daily data refresh scheduled at 00:00.")

    # Run the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait for 1 minute before checking again

if __name__ == "__main__":
    schedule_daily_refresh()
