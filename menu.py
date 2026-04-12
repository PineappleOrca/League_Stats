from my_secrets import get_my_accounts, get_other_accounts, get_korea_accounts

def get_user_input():
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('Please Select an Option to Download')
    print('(1) Download My Account Data')
    print('(2) Download Other EUW Account Data')
    print('(3) Download Korea Account Data')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    user_input = int(input('Please Enter Your Choice as an integer: '))
    server_string = get_server(user_input)
    account_list = get_accounts(user_input)
    data_dict = {}
    data_dict[server_string] = account_list 
    return data_dict

def get_server(region_num):
    region_mapping = {
        1: 'europe',
        2: 'euw1',
        3: 'kr'
    }
    return region_mapping.get(region_num, 'Invalid')

def get_accounts(user_input):
    account_mapping = {
        1: get_my_accounts(),
        2: get_other_accounts(),
        3: get_korea_accounts()
    }
    return account_mapping.get(user_input, 'Invalid')

