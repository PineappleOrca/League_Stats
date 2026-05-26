from riotwatcher import LolWatcher, ApiError
from my_secrets import get_api_key, get_my_accounts
import requests
import json


def get_mastery_points(api_key: str, region: str, summoner_name: str, champion_id: int) -> int:
    # Initialize the LolWatcher with your API key
    watcher = LolWatcher(api_key)
    try:
        # Get summoner information
        summoner = watcher.summoner.by_puuid(region, summoner_name)
        # Get mastery information for the given champion
        champion_mastery = watcher.champion_mastery.by_puuid(region, summoner["puuid"])
        for mastery in champion_mastery:
            if mastery["championId"] == champion_id:
                return mastery["championPoints"]
        return 0  # If no mastery found for the champion
    except ApiError as e:
        print(f"Error: {e.response.status_code} - {e.response.text}")
        return None
    
def test_get_mastery_points(api_key: str, region: str, summoner_name: str) -> int:
    # Initialize the LolWatcher with your API key
    watcher = LolWatcher(api_key)
    try:
        # Get summoner information
        summoner = watcher.summoner.by_puuid(region, summoner_name)
        # Get mastery information for the given champion
        champion_mastery = watcher.champion_mastery.by_puuid(region, summoner["puuid"])
        return champion_mastery
    except ApiError as e:
        print(f"Error: {e.response.status_code} - {e.response.text}")
        return None

def estimate_games_played(master_points, win_rate):
    return master_points/(900.0*win_rate + 100.0)

def get_champion_id_map() -> dict:
    # 1. Get the latest game patch version from Riot's version endpoint
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    latest_version = requests.get(version_url).json()[0]
    
    # 2. Fetch the master champion JSON file for that specific version
    data_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
    response = requests.get(data_url).json()
    champion_data = response["data"]
    
    # 3. Riot maps things by name key (e.g., {"Aatrox": {"key": "266", ...}})
    # We invert it so we can easily look it up by ID number instead
    champion_map = {}
    for champ_name, details in champion_data.items():
        champ_id = int(details["key"]) # Riot stores IDs as strings, cast to int
        champion_map[champ_id] = details["name"]
    return champion_map

def get_total_mastery(api_key: str, region: str, summoner_names: list, champion_id: int, champion_name: str) -> None:
    # This is the champion ID for Yasuo
    #champion_id = 157
    total = 0
    for summoner in summoner_name:
        mastery_points = get_mastery_points(riot_api_key, region, summoner, champion_id)
        if mastery_points is not None:
            total += mastery_points 
    print(f"{champion_name}: {total}")

if __name__ == '__main__':
    # Replace with your Riot API key
    riot_api_key = get_api_key()
    region = "euw1"
    summoner_name = get_my_accounts()
    champ_dict = get_champion_id_map()
    master_dict = {}
    master_dict['total'] = {}
    for summoner in summoner_name:
        master_dict[summoner] = test_get_mastery_points(riot_api_key, region, summoner_name)
    for summoner in summoner_name:
        for champ in champ_dict:
            champion_name = champ_dict[champ]
            master_dict['total'][champion_name] += master_dict[summoner][champ]['championPoints']
    print(master_dict['total'])
    #for champ in champ_dict:
    #    get_total_mastery(riot_api_key, region, summoner_name, champ, champ_dict[champ])
    