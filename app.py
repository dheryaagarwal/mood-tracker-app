import streamlit as st
import pandas as pd
import plotly.express as px
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Mood of the Queue", layout="wide")

st_autorefresh(interval=60_000, key="auto_refresh")

st.sidebar.title("Options")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Mood-log").sheet1

records = sheet.get_all_records()
data = pd.DataFrame(records)
if not data.empty:
    data["timestamp"] = pd.to_datetime(data["timestamp"])

min_date = data["timestamp"].dt.date.min() if not data.empty else date.today()
default_range = [min_date, date.today()]
date_range = st.sidebar.date_input("Select date range", default_range)
group_by_day = st.sidebar.checkbox("Group by day", value=False)
st.sidebar.markdown("---")
refresh_interval = st.sidebar.slider("Refresh interval (sec)", 10, 300, 60)
st.sidebar.info(f"Auto-refresh every {refresh_interval}s")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Log a Mood")
    with st.form("mood_form"):
        mood = st.selectbox("Select mood", ["😊", "😠", "😕", "🎉"])
        note = st.text_area("Add a short note (optional)")
        submitted = st.form_submit_button("Submit Mood")
        if submitted:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([timestamp, mood, note])
            st.success("Mood logged successfully!")

filtered = data[
    (data["timestamp"].dt.date >= date_range[0]) &
    (data["timestamp"].dt.date <= date_range[1])
]

with col2:
    if not filtered.empty:
        if group_by_day:
            grouped = (
                filtered
                .groupby([filtered["timestamp"].dt.date, "mood"]) 
                .size()
                .reset_index(name="Count")
            )
            grouped.columns = ["Date", "Mood", "Count"]
            fig = px.bar(
                grouped,
                x="Date",
                y="Count",
                color="Mood",
                barmode="group",
                title="Mood Counts by Day"
            )
        else:
            today = date.today()
            today_data = filtered[filtered["timestamp"].dt.date == today]
            counts = today_data["mood"].value_counts().reset_index()
            counts.columns = ["Mood", "Count"]
            fig = px.bar(
                counts,
                x="Mood",
                y="Count",
                title=f"Mood Counts for {today.isoformat()}",
                color="Mood"
            )
        st.header("Trends")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Show raw data"):
            st.dataframe(filtered)
    else:
        st.info("No data in the selected range.")

st.markdown("---")
st.caption("Built by Dherya Agarwal — Keep track of everyone's mood!")
