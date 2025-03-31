import requests
import pandas as pd

SHOPIFY_STORE = "b77a66-2a.myshopify.com"
SHOPIFY_ACCESS_TOKEN = "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"

def fetch_shopify_orders():
    try:
        # Define API Endpoint
        url = f"https://{SHOPIFY_STORE}/admin/api/2023-01/orders.json?status=created&limit=250"

        # Use X-Shopify-Access-Token for Authentication
        headers = {
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
        }

        response = requests.get(url, headers=headers)

        # Check if request was successful
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return pd.DataFrame()

        # Parse JSON Response
        orders = response.json().get("orders", [])

        # Convert to DataFrame
        if not orders:
            print("⚠️ No orders found in Shopify.")
            return pd.DataFrame()

        df_orders = pd.json_normalize(orders)  # Flatten JSON

        return df_orders

    except Exception as e:
        print(f"❌ Error fetching Shopify orders: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df_orders = fetch_shopify_orders()

    if not df_orders.empty:
        df_orders.to_csv("data/shopify_orders.csv", index=False)
        print("✅ Shopify orders data saved successfully: data/shopify_orders.csv")
    else:
        print("⚠️ No data saved due to errors or empty response.")
