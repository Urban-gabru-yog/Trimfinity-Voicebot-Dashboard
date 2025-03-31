import streamlit as st
import pandas as pd
import plotly.express as px

# Load merged data
df = pd.read_csv("data/merged_data.csv")

# Convert StartTimestamp to datetime and extract date
df['StartTimestamp'] = pd.to_datetime(df['StartTimestamp'], errors='coerce')
df['call_date'] = df['StartTimestamp'].dt.date  # Extracts only YYYY-MM-DD

st.title("📊 Customer Call & Sales Dashboard")

# Date Range Filter
start_date = st.date_input("Start Date", df['call_date'].min())
end_date = st.date_input("End Date", df['call_date'].max())

# Filter data within selected date range
df_filtered = df[(df['call_date'] >= start_date) & (df['call_date'] <= end_date)]

# ---- Business Metrics ----
st.metric("Total Calls Made", len(df_filtered))

# Load call data
call_data = pd.read_csv("data/call_data.csv")

# Convert StartTimestamp to datetime and extract date for call_data
call_data['StartTimestamp'] = pd.to_datetime(call_data['StartTimestamp'], errors='coerce')
call_data['call_date'] = call_data['StartTimestamp'].dt.date  # Extracts only YYYY-MM-DD

# Convert TotalDuration to numeric, forcing errors to NaN, then fill with 0
call_data['TotalDuration (in sec)'] = pd.to_numeric(call_data['TotalDuration (in sec)'], errors='coerce').fillna(0)

# Filter picked-up calls within the selected date range where TotalDuration > 1
picked_up_calls = call_data[
    (call_data['call_date'] >= start_date) & 
    (call_data['call_date'] <= end_date) & 
    (call_data['TotalDuration (in sec)'] > 1)
]
st.metric("Total Picked Up Calls", len(picked_up_calls))

st.metric("Total Purchases After Calls", df_filtered['order_number'].count())

conversion_percentage = round(df_filtered['order_number'].count() / len(picked_up_calls) * 100, 2)
st.metric("Conversion Percentage", f"{conversion_percentage}%")

# Function to count total purchases after calls using email matching
def count_total_purchases_after_calls():
    # Load the data from CSV files
    df_calls = pd.read_csv("data/call_data.csv")
    df_orders = pd.read_csv("data/shopify_orders.csv")

    # Convert email columns to lowercase for consistent matching
    df_calls['Email'] = df_calls['Email'].str.lower()
    df_orders['contact_email'] = df_orders['contact_email'].str.lower()

    # Get the set of emails from call_data
    call_emails = set(df_calls['Email'].dropna())

    # Find matching emails in shopify_orders
    matched_emails = df_orders['contact_email'].isin(call_emails)

    # Count the total number of matching rows (purchases after calls)
    total_purchases = matched_emails.sum()

    return total_purchases


# ---- Calls vs Purchases (Interactive Bar Chart) ----
st.subheader("📞 Calls vs 🛒 Purchases")
df_grouped = df_filtered.groupby('call_date')['order_number'].count().reset_index()
fig = px.bar(df_grouped, x="call_date", y="order_number", 
             labels={"call_date": "Date", "order_number": "Purchases"},
             hover_data={"order_number": True}, 
             title="Daily Purchases After Calls")
st.plotly_chart(fig)

# ---- Call Duration Distribution (Interactive Histogram) ----
st.subheader("⏳ Call Duration Distribution")
fig = px.histogram(df_filtered, x="DurationSeconds", nbins=20, 
                   labels={"DurationSeconds": "Call Duration (Seconds)"},
                   title="Call Duration Distribution")
st.plotly_chart(fig)

# ---- Customer Sentiment Analysis (Interactive Pie Chart) ----
st.subheader("😊 Customer Sentiment Distribution")
sentiment_counts = df_filtered['UserSentiment'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'count']
fig = px.pie(sentiment_counts, names="Sentiment", values="count", 
             title="Customer Sentiment Analysis", hole=0.3)
st.plotly_chart(fig)

# ---- Disconnection Reasons Breakdown (Interactive Bar Chart) ----
st.subheader("📞 Disconnection Reasons")
fig = px.bar(df_filtered, x="DisconnectionReason", title="Disconnection Reasons Breakdown")
st.plotly_chart(fig)

# ---- Successful vs Failed Calls (Interactive Bar Chart) ----
st.subheader("✅ Successful vs ❌ Failed Calls")
call_outcomes = df_filtered['CallSuccessful'].value_counts().reset_index()
call_outcomes.columns = ['Status', 'Count']
fig = px.bar(call_outcomes, x="Status", y="Count",
             title="Call Outcome Breakdown",
             text="Count", color="Status",
             color_discrete_map={"0": "red", "1": "green"})
fig.update_traces(texttemplate='%{text}', textposition='outside')
st.plotly_chart(fig)



# ---- Download CSV ----
st.download_button(label="📥 Download Data", data=df_filtered.to_csv(index=False), file_name="filtered_data.csv", mime="text/csv")
