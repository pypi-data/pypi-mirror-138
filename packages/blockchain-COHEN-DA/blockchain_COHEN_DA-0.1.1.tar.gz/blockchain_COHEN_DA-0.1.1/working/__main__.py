'''This app grabs blockchain transactions and balances
for list of addresses provided as input

Supported chains:
-   'Ronin'
-   'Polygon',
-   'Binance Smart Chain',
-   'Fantom',
-   'MoonBeam',
-   'MoonRiver',
-   'RSK',
-   'Arbitrum',
-   'Palm',
-   'Klayton',
-   'HECO',
-   'IoTex',
-   'EvMos'
'''


import json
import sys
from os import listdir
from os.path import splitext

from pprint import pprint
import datetime
from numpy import promote_types
import pandas as pd
from PyInquirer import prompt


from blockchain import interfaces


def prompt_questions(choices):
    answers = prompt([
    {
        "type": "list",
        "name": "file",
        "message": "Choose the file that has the wallet addresses:",
        "choices": choices
    },

    {
        "type" : "input",
        "name" : "start_time",
        "message" : "Start time for transactions (UTC): ",
        "default" : "2021-01-01 00:00:00"
    },

    {
        "type" : "input",
        "name" : "end_time",
        "message" : "End time for transactions (UTC): ",
        "default" : "2021-12-31 23:59:59"
    },

    {
        "type" : "input",
        "name" : "output_file",
        "message" : "Name of output file",
        "default" : "transactions.csv"
    }
    ])
    return answers

def unsupported_user_check(message):
    """ Corrects user input error and prompts to continue or exit with message"""
    check = prompt(
            {
                'type': 'confirm',
                'message': 'Do you want to continue?',
                'name': 'continue',
                'default': True
            }
    )

    if not check['continue']:
        sys.exit(message)


def _process_time(time_string, direction):
    try:
        parsed_time = datetime.datetime.strptime(
            time_string, '%Y-%m-%d %H:%M:%S')
        processed_time = datetime.datetime(
            parsed_time.year, parsed_time.month,
            parsed_time.day, parsed_time.hour,
            parsed_time.minute, parsed_time.second,
            tzinfo=datetime.timezone.utc)
    except ValueError:
        if direction == 1:
            print('Invalid start time entered using 2021-01-01 00:00:00 UTC as start time')
            unsupported_user_check('Not Valid Start time')
            processed_time = _process_time('2021-01-01 00:00:00', 1)
        else:
            print('Invalid end time entered using 2021-01-01 00:00:00 UTC as start time')
            unsupported_user_check('Not valid End time')
            processed_time = _process_time('2021-12-31 00:00:00', 0)
    return processed_time


# main app
if __name__ == '__main__':
    df = pd.DataFrame()
    header = ['Wallet', 'Hash', 'Ticker', 'Amount', 'Type', 'Time', 'Block Explorer', 'Event Type']
   
    # get list of xlsx files in current directory and put into prompt questions
    FOLDER = 'C:\\Users\\jsilverman\\TT'
    choices = [f for f in listdir(FOLDER) if splitext(f)[1] == '.xlsx']
   
    # get user selection
    answers = prompt_questions(choices)

    pprint(answers)

    outfile = answers['output_file']
    # import wallets from excel
    try:
        wallets = pd.read_excel(FOLDER + '\\' + answers['file']).\
            query('Custody_Provider_Type == "Self"')
    except NameError:
        unsupported_user_check('Input file needs to be .xlsx')

    #print(wallets)
    start_time = _process_time('2021-01-01 00:00:00', 1)
    end_time = _process_time('2021-12-31 23:59:59', 0)

    if answers['start_time']:
        start_time = _process_time(answers['start_time'], 1)


    if answers['end_time'] :
        end_time = _process_time(answers['end_time'], 0)

    while end_time < start_time :
        print("End time must be after start time")
        
        date_questions = [
        {
            "type" : "input",
            "name" : "start_time",
            "message" : "Start time for transactions",
            "default" : "2021-01-01 00:00:00"
        },

        {
            "type" : "input",
            "name" : "end_time",
            "message" : "End time for transactions",
            "default" : "2021-12-31 00:00:00"
        
        }
    ]
        answers = prompt(date_questions)
        if answers['start_time']:
            start_time = _process_time(answers['start_time'], 1)
        else:
            start_time = _process_time('2021-01-01 00:00:00', 1)

        if answers['end_time'] :
            end_time = _process_time(answers['end_time'], 0)
        else:
            end_time = _process_time('2021-12-31 23:59:59', 0)


    # get supported chains from package list
    supported_chains = set(interfaces.keys())
    print(f'Supported chains: {supported_chains}')

    # check for unsupported chains
    chains = list(wallets['Custody_Provider'].unique())
    unsupported_chains = [c for c in chains if c not in supported_chains]


    # get decision to continue if unsupported chains found
    if len(unsupported_chains) > 0:
        print('\nThese chains are not supported')
        print(unsupported_chains)
        unsupported_user_check('Too many unsupported chains')

    # loop through records to get transactions
    for wallet in wallets[wallets['Custody_Provider'].isin(\
        supported_chains)][['Custody_Provider','API_Key_Or_Wallet']].itertuples():
        print(wallet.Custody_Provider + ': ' + wallet.API_Key_Or_Wallet)
        df = pd.concat([interfaces[wallet.Custody_Provider]\
            .get_transactions(wallet.API_Key_Or_Wallet), df])
    # export to csv/excel
    df.columns=header
    begin = df['Time'] > start_time
    end = df['Time'] < end_time
    filtered_df = df[begin]
    filtered_df = df[end]
    filtered_df.to_csv(FOLDER+'\\'+ outfile, index=False)
