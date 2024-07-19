import requests
import pandas as pd
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
aggregated_data = pd.DataFrame()

def fetch_virustotal():
    url = "https://www.virustotal.com/api/v3/intelligence/hunting_notifications"
    headers = {"x-apikey": "YOUR_VIRUSTOTAL_API_KEY"}
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_alienvault():
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": "YOUR_ALIENVAULT_API_KEY"}
    response = requests.get(url, headers=headers)
    return response.json()

def normalize_data(data, source):
    normalized = []
    for item in data:
        normalized.append({
            "source": source,
            "threat": item.get("name", ""),
            "description": item.get("description", ""),
            "timestamp": item.get("created", "")
        })
    return pd.DataFrame(normalized)

def aggregate_data():
    global aggregated_data
    vt_data = fetch_virustotal()
    av_data = fetch_alienvault()
    
    vt_df = normalize_data(vt_data, "VirusTotal")
    av_df = normalize_data(av_data, "AlienVault")
    
    aggregated_data = pd.concat([vt_df, av_df], ignore_index=True)

scheduler = BackgroundScheduler()
scheduler.add_job(func=aggregate_data, trigger="interval", seconds=3600)
scheduler.start()

@app.route('/threats', methods=['GET'])
def get_threats():
    global aggregated_data
    return jsonify(aggregated_data.to_dict(orient='records'))

if __name__ == '__main__':
    aggregate_data()
    app.run(debug=True, port=5000)