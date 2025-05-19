# Mood of the Queue

A simple, friendly tool to help your support team log and visualize the emotional “vibe” of incoming tickets—right in your browser.

---

## Why We Built This

Every support ticket carries a little bit of emotion—frustration when something breaks, joy when everything’s smooth, or confusion when details are missing. This app does exactly that: log a mood, add a quick note, and watch the bar chart update in near real time.

---

## Key Features

* **One-click Mood Logging**
  Choose from 😊, 😠, 😕 or 🎉 and drop in a short note if you like.
* **Auto-Refresh**
  Data and charts refresh automatically (you choose the interval).
* **Flexible Date Filtering**
  Pick any start/end date to review historical entries.
* **Group-by-Day Toggle**
  See daily totals or focus on today’s breakdown.
* **Interactive Plotly Charts**
  Color-coded bars make trends pop.
* **Raw Data Explorer**
  Expand a table view to scan every single record.

---

## How It Works

1. **Google Sheets as a Backend**
   A shared Sheet called `Mood-log` (with columns `timestamp | mood | note`) stores every entry.
   We talk to it via the `gspread` library, authenticating with a Service Account JSON key.
2. **Streamlit Front-End**

   * **Page Config & Auto-Refresh**
     We set up the page layout and use `streamlit_autorefresh` to reload data every N seconds.
   * **Sidebar Controls**
     Let you pick a date range, toggle “Group by day,” and adjust the refresh interval.
   * **Mood Form**
     A simple form on the left to submit a new mood + note; writes straight to Google Sheets.
   * **Visualization Panel**
     On the right, we filter and group the data based on your controls, then render a Plotly bar chart.
   * **Raw Data Expander**
     Dive into the full DataFrame right inside the app.

---

## Getting Started

### Prerequisites

* **Python 3.8+**
* A **Google Cloud Service Account** with Editor access to a Google Sheet
* A Google Sheet named `Mood-log` with headers:

  ```
  timestamp | mood | note
  ```
* The service-account JSON key file saved as `google_credentials.json` in your project root

### Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/mood-tracker-app.git
   cd mood-tracker-app
   ```
2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Share your sheet**
   Open `Mood-log` in Google Sheets → Share → add your service-account email as Editor.
5. **Hide secrets**
   Ensure `google_credentials.json` is in `.gitignore` before pushing to GitHub.

---

## Running the App

```bash
streamlit run app.py
```

* Your browser should open at [http://localhost:8501](http://localhost:8501).
* Use the **sidebar** to adjust date filters, toggle grouping, and set refresh interval.
* In the **Log a Mood** panel, pick an emoji, type an optional note, and click **Submit**.
* The **Trends** chart will update automatically—and you can expand the raw table below it to inspect every entry.

---

## Deployment 

* **Streamlit Community Cloud**
  Connect your GitHub repo for free, zero-config hosting.

---

## Customization Ideas

* Swap in custom emojis or add more mood categories.
* Add a “top notes” word-cloud panel to surface recurring issues.

---

## Acknowledgments

Built by **Dherya Agarwal**.

---

*Happy mood-tracking!*
