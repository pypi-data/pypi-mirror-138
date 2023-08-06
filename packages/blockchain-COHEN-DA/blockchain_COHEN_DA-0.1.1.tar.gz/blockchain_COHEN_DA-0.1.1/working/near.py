import os
import json
import requests
import pandas as pd
import csv
from datetime import datetime

mainnet = 'https://archival-rpc.mainnet.near.org'
cols = ['Wallet', 'Tx Hash', 'Lockup Account', 'Lockup Account Hash']
keys = ['wallet', 'hash', 'lockup', 'lockup_hash']
file = r'C:\Users\jsilverman\NEAR_transactions.csv'

data = pd.read_csv(file, skiprows=1)[cols].dropna()
result = []
tx = []
method_type = []

for line in data.values:
    row = dict(zip(keys,line))
    result.append(row)

for r in result:
    params = [r['hash'], r['lockup']]
    data = {'jsonrpc' : '2.0', 'id' : 'tx', 'method' : 'tx', 'params' : params}
    tx.append(json.loads(requests.post(mainnet, json=data).text))

# NEAR deposits to wallet from contract
# output for transfer testing
# Should be xlsx and not csv but good enough for now
    for t in tx:
        if t['result']['transaction']['signer_id'] == 'near':
            with open('C:\\Users\\jsilverman\\near.csv', 'w', newline='') as csvfile: 
                d = csv.writer(csvfile, delimiter=",")
                wallet = t['result']['transaction']['receiver_id']
                ticker = 'NEAR'
                hash = t['result']['transaction']['hash']
                if 'deposit' in t['result']['transaction']['actions'][0]['Transfer']:
                    amount = t['result']['transaction']['actions'][0]['Transfer']['deposit']
                    type = 'Deposit'
                else:
                    amount = ''
                    type = 'Withdrawal'
                params = {'block_id' : t['result']['transaction_outcome']['block_hash']}
                data = {'jsonrpc' : '2.0', 'id' : 'block', 'method' : 'block', 'params' : params}
                b = json.loads(requests.post(mainnet, json=data).text)
                time = int(int(b['result']['header']['timestamp'])/1e9)
                time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
                explorer = mainnet
                d.writerow([wallet, ticker, hash, amount, type, time, explorer])
        
        # Create log files for staking and other events
        else:
            method= t['result']['transaction']['actions'][0]['FunctionCall']['method_name']
            with open('C:\\Users\\jsilverman\\near_logs.txt', 'w') as f:
                wallet = t['result']['transaction']['signer_id']
                f.write(wallet)
                f.write('\n')
                f.write(method)
                f.write('\n')
                for r in t['result']['receipts_outcome']:
                    params = {'block_id' : r['block_hash']}
                    data = {'jsonrpc' : '2.0', 'id' : 'block', 'method' : 'block', 'params' : params}
                    b = json.loads(requests.post(mainnet, json=data).text)
                    time = int(int(b['result']['header']['timestamp'])/1e9)
                    time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
                    if len(r['outcome']['logs']) != 0 :
                       f.write(time)
                       f.write('\n')
                       for l in r['outcome']['logs']:
                            f.write(l)
                            f.write('\n')
                f.write('\n')






