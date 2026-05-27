import os
from dotenv import load_dotenv
from enum import Enum

def get_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("RIOT_API_KEY")
    return api_key

def get_account_name():
    print("Currently Not a supported/Active function, since 2023 hasnt been updated!")
    account_list = ['my_account_name']
    return account_list

def get_my_accounts():
    account_list = [os.getenv("SMURF_1"), os.getenv("MAIN_ACC"), os.getenv("SMURF_2")]
    return account_list 

def get_other_accounts():
    account_list = [os.getenv("BROVY_PUUID"), os.getenv("TWP_1_PUUID"), os.getenv("TWP_2_PUUID")]
    return account_list 

def get_korea_accounts():
    account_list = [os.getenv("PZZANG_1_PUUID"), os.getenv("PZZANG_2_PUUID"), os.getenv("PZZANG_3_PUUID")]
    return account_list

def get_account_map() -> dict:
    return {
        os.getenv("MAIN_ACC"): os.getenv("MAIN_NAME"),
        os.getenv("SMURF_1"): os.getenv("SMURF_1_NAME"),
        os.getenv("SMURF_2"): os.getenv("SMURF_2_NAME"),
        os.getenv("BROVY_PUUID"): os.getenv("BROVY_IGN"),
        os.getenv("TWP_1_PUUID"): os.getenv("TWP_1_IGN"),
        os.getenv("TWP_2_PUUID"): os.getenv("TWP_2_IGN")
    }

def get_ign(account_id: str) -> str:
    accounts = get_account_map()
    return accounts.get(account_id, "Unknown Player")


