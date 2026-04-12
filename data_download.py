# This is a script with the functions to download the data from the Riot API
from my_secrets import get_api_key, get_account_name
from riotwatcher import LolWatcher, ApiError
import pandas as pd
#from os import listdir
#from os.path import isfile, join
import os
import glob
import csv
import json
from dotenv import load_dot_env

def get_account_information(watcher, region, account_name):
    '''
    This Function takes in the watcher, region (string) and the account name (string singular)
    -> Outputs information on the account
    '''
    me = watcher.summoner.by_puuid(region, account_name)
    return me

def get_ranked_stats(watcher, region, data):
    '''
    This function takes in the watcher, region and the output from the get_account_information function and returns the ranked stats for that account
    '''
    ranked_stats = watcher.league.by_puuid(region, data['id'])
    return ranked_stats

def get_match_list(watcher, region, data):
    '''
    This function takes in the watcher, the region and the output from get_account_information and then 
    returns a list of 20 instances with match ids
    '''
    my_matches = watcher.match.matchlist_by_puuid(region, data['puuid'])
    return my_matches

def build_match_database(watcher, region, data):
    '''
    This Function takes in watcher, region and data from the get_account_information 
    AIM -> Build Global Database of matches with match ids since I can only request 20 instances at a time, I need to keep appending to the Global Database
    OUTPUT -> appends to the global database
    '''
    # Path to the Database
    path_to_match_database = '/Users/kevin/Documents/Kevin/Projects/my_league_stats/Data/match_database/match_database.csv'
    match_list = get_match_list_from_database(path_to_match_database)
    latest_match_list = get_match_list(watcher, region, data)
    # Appending the global match list on the database to the latest 20 games pulled from the API
    match_list = match_list + latest_match_list
    # Converting the list to a set so that only the unique values are stored
    match_set = set(match_list)
    match_list = list(match_set)
    # Converting 
    pd_match_list = pd.DataFrame(list(match_set))
    pd_match_list.to_csv(path_to_match_database)
    return match_list

def get_match_list_from_database(path):
    match_list = []
    df = pd.read_csv(path)
    match_list = df['0'].tolist()
    return match_list

def get_match_data(watcher, region):
    '''
    This Function takes in the list of matches and appends the information to a JSON file with all the match data
    -> TO DO
    -> This function should read all the files in the folder nammed 'match_data' and then see which game ids need to be processed
    -> create a list where you have the set of game ids for which JSON files do not exist
    -> then iterate through the list and generate JSON files with the information on each game from the match 'info' bit
    ->
    '''
    # Source File paths on local computer
    match_list_src = os.getenv("MATCH_LIST_SRC")
    match_data_src = os.getenv("MATCH_DATA_SRC")
    #match_list_src = '/Users/kevin/Documents/Kevin/Projects/my_league_stats/Data/match_database/match_database.csv'
    #match_data_src = '/Users/kevin/Documents/Kevin/Projects/my_league_stats/Data/match_data/'

    # getting total match list from database, and list of matches already stored 
    match_list = get_match_list_from_database(match_list_src)
    list_of_files = get_list_of_files(match_data_src)
    new_match_list = [x for x in match_list if x not in list_of_files] 
    print(f"{len(new_match_list)} new games detected!")
    for match in new_match_list:
        write_match_data(watcher, match, region)
        print(f"Data for Match: {match} has been written!")

def write_match_data(watcher, match_id, region):
    file_path = os.getenv("MATCH_DATA_SRC")
    #file_path = '/Users/kevin/Documents/Kevin/Projects/my_league_stats/Data/match_data/'
    file_name = file_path + match_id + '.json'
    match_detail = watcher.match.by_id(region, match_id)
    match_info = match_detail['info']
    json_object = json.dumps(match_info)
    with open(file_name, 'w') as f:
        f.write(json_object)

def get_list_of_files(path):
    '''
    This is a function which will get the list of files for the games which are already processed
    INPUT -> takes in a PATH as a STRING 
    OUTPUT -> returns a list of files in the PATH and subtracts the file ending '.json' from it
    '''
    file_ending = '.json'
    list_of_files = [f.replace(file_ending,'') for f in os.listdir(path) if os.isfile(os.join(path,f))]
    return list_of_files


