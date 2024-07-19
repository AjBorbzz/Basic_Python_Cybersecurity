import os
import psutil
import subprocess
from datetime import datetime


"""
# Cybersecurity Forensics Script

This script performs basic forensic analysis on a system, including:
1. Listing running processes.
2. Listing active network connections.
3. Collecting file metadata from a specified directory.

## Requirements
- `psutil` library (install via `pip install psutil`).

## Usage
```bash
python forensics_script.py

Notes
Ensure you have the necessary permissions to access system information and files.
This is a basic implementation for educational purposes.
"""


def list_running_processes():
    print("Listing running processes:")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            process_info = proc.info
            print(f"PID: {process_info['pid']}, Name: {process_info['name']}, User: {process_info['username']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("\n")

def list_network_connections():
    print("Listing network connections:")
    for conn in psutil.net_connections():
        try:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            print(f"PID: {conn.pid}, Type: {conn.type}, Local Address: {laddr}, Remote Address: {raddr}, Status: {conn.status}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("\n")

def get_file_metadata(directory):
    print(f"Collecting file metadata in directory: {directory}")
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_stat = os.stat(filepath)
                creation_time = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                modification_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"File: {filepath}, Size: {file_stat.st_size} bytes, Created: {creation_time}, Modified: {modification_time}")
            except Exception as e:
                print(f"Could not access file {filepath}: {e}")
    print("\n")

def main():
    print("Starting cybersecurity forensics script...\n")
    
    list_running_processes()
    list_network_connections()
    
    directory = input("Enter the directory to collect file metadata (e.g., C:\\Users\\Username\\Documents): ")
    get_file_metadata(directory)
    
    print("Forensics analysis completed.")

if __name__ == "__main__":
    main()
