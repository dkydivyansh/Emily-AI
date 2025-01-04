import os
import requests
import sys
def fetch_update_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to download update Data. Status code: {response.status_code}")
def download_file(url, destination):
    try:
        print("Downloading files...")
        destination_dir = os.path.dirname(destination)
        if destination_dir:
            os.makedirs(destination_dir, exist_ok=True)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded file: {destination}")
    except Exception as e:
        print(f"Error while downloading file: {e}")
def update_updater():
    update_url = 'updater-url'
    try:
        data = fetch_update_json(update_url)
        updater_url = data['updater_link']
        updater_path = 'updater.exe'
        download_file(updater_url, updater_path)
        print(f"successfully updated")
    except Exception as e:
        print(f"Error during update: {e}")          
        sys.exit(1)