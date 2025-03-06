# KleptoWatch

KleptoWatch is a legislative tracking system designed to monitor and report changes in government legislation, focusing on corporate influence, wealth-driven policy changes, and sneaky amendments. It tracks bills across states, counties, and cities, detecting modifications over time and alerting users to significant changes.

## 📌 Features

- Real-time tracking of legislative data from official government APIs
- Automated monitoring with timestamped JSON snapshots
- Git-based diff detection to track changes in bills, amendments, and votes
- Supports state, county, and city-level filtering (default: Oregon, Lane County, No City)
- Expandable to other states & locations
- Future integration: Bluesky alerts, AI-driven bill analysis

## 🏗️ Project Structure

```
KleptoWatch/  
├── legislative_data/          # Root data directory  
│   ├── oregon/               # State-level tracking  
│   │   ├── lane_county/      # County-level tracking  
│   │   │   ├── no_city/      # City-level tracking (default: unincorporated areas)  
│   │   │   │   ├── legislation_YYYY-MM-DD_HH-MM-SS.json  # Raw legislative data  
│   │   │   │   ├── changes_YYYY-MM-DD_HH-MM-SS.json      # Git-diff detected changes  
│   │   ├── multnomah_county/ # Another county example  
│   │   │   ├── portland/     # City-level tracking  
│   │   │   │   ├── legislation_YYYY-MM-DD_HH-MM-SS.json  
│   │   │   │   ├── changes_YYYY-MM-DD_HH-MM-SS.json  
├── scripts/                  # Python tracking scripts  
├── README.md                 # Documentation  
```
## 🚀 Getting Started

1️⃣ Clone the Repository  
`git clone git@github.com:nekorbin/KleptoWatch.git`
`cd KleptoWatch`

2️⃣ Setup venv and Install Dependencies
These steps only tested so far with Git-Bash on a Mac. 
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

3️⃣ Run the Tracker  
By default, this will fetch legislative data for Oregon, Lane County (Unincorporated areas).  
`python scripts/track_legislation.py`  
To track a specific city or county, modify the STATE, COUNTY, and CITY settings inside track_legislation.py.  

## Automate Daily Runs (Optional)
Use cron (Linux/macOS) or Task Scheduler (Windows) to run at 8 AM, Noon, and 6 PM:  
`0 8,12,18 * * * /usr/bin/python3 /path/to/KleptoWatch/scripts/track_legislation.py`

## 🔍 Example API Request
To manually test the Oregon Legislative API:  
`curl -X GET "https://api.oregonlegislature.gov/odata/odataservice.svc/Measures"`

## 🛠️ Contributing
Open an issue for bugs, suggestions, or feature requests
Submit PRs for new state integrations, city tracking, or AI-driven monitoring

## 🔥 Future Enhancements
✅ Bluesky Bot Alerts – Post major bill changes to social media  
✅ AI-Driven Bill Analysis – Detect sneaky amendments or harmful clauses  
✅ Database Integration – Store & analyze long-term legislative trends  

## ⚔️ Stick it to the man!
🛑 "Not Left, Not Right — Just Down vs Up."  
🛠️ Built by watchdogs, for the people.  
