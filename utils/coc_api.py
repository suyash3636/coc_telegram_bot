import requests
from config import COC_API_KEY, CLAN_TAG

def get_clan_info():
    encoded_tag = CLAN_TAG.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}"
    headers = {"Authorization": f"Bearer {COC_API_KEY}", "Accept": "application/json"}

    response = requests.get(url, headers=headers, timeout=10)
    return response.json() if response.status_code == 200 else None

def get_war_details():
    encoded_tag = CLAN_TAG.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}/currentwar"
    headers = {"Authorization": f"Bearer {COC_API_KEY}", "Accept": "application/json"}

    response = requests.get(url, headers=headers, timeout=10)
    return response.json() if response.status_code == 200 else None
