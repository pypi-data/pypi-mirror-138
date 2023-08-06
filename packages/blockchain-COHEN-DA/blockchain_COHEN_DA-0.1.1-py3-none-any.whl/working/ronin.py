import requests
import json
import csv
import pandas as pd
import datetime

class Ronin():
     

    def write_tx(wallet, hash, ticker, amount, type, time, block_explorer):
        tx = [wallet, hash, ticker, amount, type, time, block_explorer]
        return tx

    def get_transactions(addr) :
        data = []
        header = ['Wallet', 'Hash', 'Ticker', 'Amount', 'Type', 'Time', 'Block Explorer']
        ckey = 'ckey_d5a5850f10a046d9b28e72408df'

        addr = [
            '0x5b796afc457875fbce45c9dea5b10e8ec3a1525e'
        ]
        #data.append(header)
        for a in addr:
            url = 'https://api.covalenthq.com/v1/2020/address/'+a+'/transactions_v2/?page-size=10000&key='+ckey
            tx = json.loads(requests.get(url).text)['data']['items']
            for t in tx:
                wallet = a
                ticker = 'RONIN'
                hash = t['tx_hash']
                amount = (t['gas_spent'] * t['gas_price']) / 1e18
                type = 'Withdrawal'
                time = t['block_signed_at']
                block_explorer = 'explorer.ronin.com'
                line = Ronin.write_tx(wallet, hash, ticker, amount, type, time, block_explorer)
                data.append(line)
                if t['to_address'] == a.lower():
                    type = 'Deposit'
                elif t['from_address'] == a.lower():
                    type = 'Withdrawal'
                else:
                    type = None
                amount = int(t['value'])/1e18
                if type:
                    line = Ronin.write_tx(wallet, hash, ticker, amount, type, time, block_explorer)
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
                                    line = Ronin.write_tx(wallet, hash, ticker, amount, type, time, block_explorer)
                                    data.append(line)
            

        df = pd.DataFrame(data, columns=header).to_csv(r'C:\Users\jsilverman\Ronin.csv', index=False)

    # with open('C:\\Users\\jsilverman\\Polygon.csv', 'w', newline='') as csvfile:
    #     out = csv.writer(csvfile, delimiter=",")
    #     for d in data:
    #         out.writerow(d)