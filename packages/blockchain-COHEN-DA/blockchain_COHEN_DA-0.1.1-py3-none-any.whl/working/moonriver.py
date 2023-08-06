import requests
import json
import csv
import pandas as pd
import datetime

class Moonriver():
    
    

    def write_tx(wallet, hash, ticker, amount, type, time, block_explorer):
        tx = [wallet, hash, ticker, amount, type, time, block_explorer]
        return tx

    def get_transactions(addr) :
        data = []
        header = ['Wallet', 'Hash', 'Ticker', 'Amount', 'Type', 'Time', 'Block Explorer']
        ckey = 'ckey_d5a5850f10a046d9b28e72408df'

        addr = [
            '0x2800b279e11e268d9d74af01c551a9c52eab1be3'
        ]
        #data.append(header)
        for a in addr:
            url = 'https://api.covalenthq.com/v1/1285/address/'+a+'/transactions_v2/?page-size=10000&key='+ckey
            tx = json.loads(requests.get(url).text)['data']['items']
            for t in tx:
                wallet = a
                ticker = 'MORV'
                hash = t['tx_hash']
                amount = (t['gas_spent'] * t['gas_price']) / 1e18
                type = 'Withdrawal'
                time = t['block_signed_at']
                block_explorer = 'https://blockscout.moonriver.moonbeam.network'
                line = Moonriver.write_tx(wallet, hash, ticker, amount, type, time, block_explorer)
                data.append(line)
                if t['to_address'] == a.lower():
                    type = 'Deposit'
                elif t['from_address'] == a.lower():
                    type = 'Withdrawal'
                else:
                    type = 'Other'
                amount = int(t['value'])/1e18
                line = Moonriver.write_tx(wallet, hash, ticker, amount, type, time, block_explorer)
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
                                        if p['value']:
                                            amount = int(p['value']) / pow(10, exp)
                                        else:
                                            amount = 0
                                if add == 1:
                                    line = Moonriver.write_tx(wallet, hash, ticker, amount, type, time, block_explorer)
                                    data.append(line)
            

        df = pd.DataFrame(data, columns=header).to_csv(r'C:\Users\jsilverman\Moonriver.csv', index=False)

    # with open('C:\\Users\\jsilverman\\Polygon.csv', 'w', newline='') as csvfile:
    #     out = csv.writer(csvfile, delimiter=",")
    #     for d in data:
    #         out.writerow(d)