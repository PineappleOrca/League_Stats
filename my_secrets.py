import os
from dotenv import load_dotenv

def get_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("RIOT_API_KEY")
    return api_key

def get_account_name():
    print("Currently Not a supported/Active function, since 2023 hasnt been updated!")
    account_list = ['my_account_name']
    return account_list

def get_my_accounts():
    account_list = [os.getenv("MAIN_ACC"), os.getenv("SMURF_1"), os.getenv("SMURF_2")]
    return account_list 

def get_other_account():
    print("Currently Not a supported/Active function, since 2023 hasnt been updated!")
    account_list = ['']
    return account_list 

def get_korea_accounts():
    print("Currently Not a supported/Active function, since 2023 hasnt been updated!")
    account_list = ['']
    return account_list 
