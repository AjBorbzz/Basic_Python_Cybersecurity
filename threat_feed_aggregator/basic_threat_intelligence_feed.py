import requests
import schedule
import time
from datetime import datetime

# Define threat intelligence feed sources
FEEDS = {
    'AlienVault OTX': 'https://otx.alienvault.com/api/v1/indicators/export',
    'VirusTotal': 'https://www.virustotal.com/vtapi/v2/url/report',
    # Add more feeds as needed
}

# Function to fetch data from a given URL
def fetch_feed(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Function to aggregate data from all sources
def aggregate_feeds():
    aggregated_data = []
    for name, url in FEEDS.items():
        data = fetch_feed(url)
        if data:
            aggregated_data.append({'source': name, 'data': data})
    return aggregated_data

# Function to display aggregated data
def display_aggregated_data(aggregated_data):
    print(f"Threat Intelligence Feed Aggregator - {datetime.now()}")
    for feed in aggregated_data:
        print(f"Source: {feed['source']}")
        print("Data:")
        print(feed['data'])
        print("-" * 40)

# Scheduled job to fetch and display data
def job():
    aggregated_data = aggregate_feeds()
    display_aggregated_data(aggregated_data)

# Schedule the job to run every hour
schedule.every().hour.do(job)

if __name__ == "__main__":
    print("Starting Threat Intelligence Feed Aggregator...")
    while True:
        schedule.run_pending()
        time.sleep(1)