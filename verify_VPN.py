import requests

def check_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    print(f"🌍 Your current IP: {response.json()['ip']}")

check_ip()
