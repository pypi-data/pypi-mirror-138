import requests
import json
import csv
import datetime

ckey = 'ckey_d5a5850f10a046d9b28e72408df'

addr = [
    '0x1E9D9468DCa9491C7e6aE46079eB39d18f341A9f',
    '0x5e7b5b815DA7a903855CF96687899Af3f0DDF449',
    '0x3a68Bb6F1679b01144f03BfaC531760cd45BE170'
    ]

data = []
header = ['Wallet', 'Ticker', 'Hash', 'Amount', 'Type', 'Time', 'Block Explorer']
data.append(header)
for a in addr:
    url = 'https://api.covalenthq.com/v1/250/address/'+a+'/transactions_v2/?page-size=10000&key='+ckey
    tx = json.loads(requests.get(url).text)['data']['items']
    for t in tx:
        wallet = a
        ticker = 'FTM'
        hash = t['tx_hash']
        amount = (t['gas_spent'] * t['gas_price']) / 1e18
        type = 'Transaction Fee'
        time = t['block_signed_at']
        block_explorer = 'ftmscan.com'
        line = [wallet, ticker, hash, amount, type, time, block_explorer]
        data.append(line)
        if t['to_address'] == a.lower():
            type = 'Deposit'
        elif t['from_address'] == a.lower():
            type = 'Withdrawal'
        else:
            type = 'Other'
        amount = int(t['value'])/1e18
        line = [wallet, ticker, hash, amount, type, time, block_explorer]
        data.append(line)

        for e in t['log_events'] :
            ticker = e['sender_contract_ticker_symbol']
            exp = e['sender_contract_decimals']
            if e['decoded']:
                if 'params' in e['decoded']:
                    if e['decoded']['params'] :
                        add = 0
                        for p in e['decoded']['params'] :
                            if p['name'] == 'to' and p['value'] == a.lower():
                                type = 'Deposit'
                                add = 1
                            if p['name'] == 'from' and p['value'] ==  a.lower():
                                type = 'Withdrawal'
                                add = 1
                            if p['name'] == 'value' :
                                amount = int(p['value']) / pow(10, exp)
                        if ticker == '':
                            add = 0
                        if add == 1:
                            line = [wallet, ticker, hash, amount, type, time, block_explorer]
                            data.append(line)
    data.append([])


with open('C:\\Users\\jsilverman\\Fantom.csv', 'w', newline='') as csvfile:
    out = csv.writer(csvfile, delimiter=",")
    for d in data:
        out.writerow(d)