import requests
import json
import os
import datetime
from pathlib import Path
import subprocess
import traceback

### CONFIGURABLE LOCATION SETTINGS ###
STATE = "oregon"  # Change to "california", "washington", etc.
COUNTY = "lane_county"  # Use lowercase with underscores (e.g., "multnomah_county")
CITY = None  # Set to a city name if applicable, otherwise None

# Base API URL (Default: Oregon)
BASE_URLS = {
    "oregon": "https://api.oregonlegislature.gov/odata/odataservice.svc/",
    # Future states can be added here (e.g., California, Washington, etc.)
}
BASE_URL = BASE_URLS.get(STATE, None)

if not BASE_URL:
    raise ValueError(f"State '{STATE}' is not yet supported.")

# Define data storage directory based on location
DATA_DIR = Path(f"legislative_data/{STATE}/{COUNTY}/{CITY if CITY else 'no_city'}")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Timestamp format for file naming
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
json_filename = DATA_DIR / f"legislation_{timestamp}.json"
changes_filename = DATA_DIR / f"changes_{timestamp}.json"

# List of API endpoints to fetch
ENDPOINTS = [
    "LegislativeSessions",
    "Measures",
    "Committees",
    "CommitteeMeetings",
    "CommitteeAgendaItems",
    "CommitteeStaffMembers",
    "CommitteeMeetingDocuments",
    "ConveneTimes",
    "FloorSessionAgendaItems",
    "Legislators",
    "MeasureAnalysisDocuments",
    "MeasureDocuments",
    "MeasureHistoryActions",
    "MeasureSponsors",
    "CommitteeProposedAmendments",
    "FloorLetters",
    "CommitteeVotes",
    "MeasureVotes",
    "CommitteeMembers"
]

def fetch_data(endpoint):
    """Fetch data from a specific API endpoint."""
    url = f"{BASE_URL}{endpoint}?$format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {traceback.format_exc()}")
        return None

def save_json(data, filename):
    """Save JSON data to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_latest_json():
    """Find the most recent JSON file in the directory to compare against."""
    json_files = sorted(DATA_DIR.glob("legislation_*.json"), reverse=True)
    return json_files[1] if len(json_files) > 1 else None  # Get second most recent file

def compare_json(old_file, new_file):
    """Compare two JSON files using git diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "--no-index", old_file, new_file],
            capture_output=True, text=True
        )
        return result.stdout.strip() if result.stdout else None
    except Exception as e:
        print(f"Error running git diff: {traceback.format_exc()}")
        return None

def main():
    print(f"Running legislative tracker for {STATE.title()}, {COUNTY.replace('_', ' ').title()}, {CITY if CITY else 'Unincorporated Area'} at {timestamp}")

    # Fetch data for all endpoints
    all_data = {endpoint: fetch_data(endpoint) for endpoint in ENDPOINTS}

    # Save raw API data as JSON
    save_json(all_data, json_filename)

    # Check if there's a previous file to compare against
    previous_json = get_latest_json()
    if previous_json:
        print(f"Comparing {previous_json} with {json_filename}")
        diff_output = compare_json(str(previous_json), str(json_filename))

        if diff_output:
            print("Changes detected, saving to changes file.")
            with open(changes_filename, "w", encoding="utf-8") as f:
                f.write(diff_output)
        else:
            print("No changes detected.")
    else:
        print("No previous JSON file found, skipping comparison.")

if __name__ == "__main__":
    main()
