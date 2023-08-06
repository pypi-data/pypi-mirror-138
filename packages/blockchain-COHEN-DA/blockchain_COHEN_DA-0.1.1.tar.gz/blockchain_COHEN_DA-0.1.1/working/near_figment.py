import json
import pandas as pd
import requests
from datetime import datetime

start_time_string = '2021-01-01 7:59:59'
start_time = datetime.strptime(start_time_string, '%Y-%m-%d %H:%M:%S').timestamp()

end_time_string = '2022-01-01 7:59:59'
end_time = datetime.strptime(end_time_string, '%Y-%m-%d %H:%M:%S').timestamp()

near_addr =  [
    '5b4378098c67c414022d65d1d0feb1943e76017acee696a511b5aa960d64e35a', 
    '86c505939b5314583a7f95ba38b688517ca876f53a266da3b0a88ad339c6519b', 
    'dafund.near'
    ]

title = ['Wallet', 'Hash', 'Ticker', 'Amount', 'Type', 'Time', 'Block Explorer']

data = []

for addr in near_addr:
    url = 'https://near--indexer.datahub.figment.io/apikey/\
        fde1f393d03bab612d3eb16dec33d3b4/transactions?account='\
        + addr
    near_tx = json.loads(requests.get(url).text)['records']

    for tx in near_tx:
        if tx['success'] == True:
            time = datetime.strptime(tx['time'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
            if time >= start_time and time <= end_time :
                time = datetime.strptime(tx['time'], '%Y-%m-%dT%H:%M:%S.%fZ')\
                    .strftime('%Y-%m-%d %H:%M:%S')
                hash = tx['hash']
                if tx['sender'] == addr :
                    type = 'Withdrawal'
                    amount = int(tx['fee'])/1e24
                    line = [addr, hash, 'NEAR', amount, type, time, 'explorer.near.org']
                    data.append(line)
                elif tx['receiver'] == addr:
                    type = 'Deposit'
                if 'deposit' in tx['actions'][0]['data']:
                    amount = int(tx['actions'][0]['data']['deposit'])/1e24
                    line = [addr, hash, 'NEAR', amount, type, time, 'explorer.near.org']
                    data.append(line)

pd.DataFrame(data, columns=title).to_csv(r'C:\Users\jsilverman\Pantera DAF, LP Near Transactions.csv', index=False)