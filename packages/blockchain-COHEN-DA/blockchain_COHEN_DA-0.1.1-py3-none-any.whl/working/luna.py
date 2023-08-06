import re
import json
import requests
import pandas as pd
from datetime import datetime

from .chain_interface import ChainInterface

class Terra(ChainInterface):
    def __init__(self, block_explorer, ticker):
        self.block_explorer = block_explorer
        self.ticker = ticker

    def get_ticker(self, value):
        return  re.findall('[a-z]+', value)[0].upper()

    def get_amount(self, value):
        return float(re.findall('\d*\.?\d+', value)[0])


    def comment_functions():    
        # def get_contract_symbol(address):
        #     url = f'https://fcd.terra.dev/v1/wasm/contract/{address}'
        #     tmp = json.loads(requests.get(url).text)['init_msg']
        #     if 'symbol' in tmp:
        #         ticker = tmp['symbol']
        #         exp = tmp['decimal']
        #     else:
        #         for k,v in tmp.items():
        #             if k.endswith('_token'):
        #                 contract_address = v 
        #                 url = f'https://fcd.terra.dev/v1/wasm/contract/{contract_address}'
        #                 ticker = json.loads(requests.get(url).text)['init_msg']['symbol']
        #                 exp = json.loads(requests.get(url).text)['init_msg']['decimals']
        #     contract_data = {'ticker' : ticker, 'exp' : exp}
        #     return contract_data

        # def transfer_from_contract(event, x, addr, time, hash, data, exp, ticker) :
        #     sender = event['attributes'][x+1]['value']
        #     receiver = event['attributes'][x+2]['value']
        #     amount = float(event['attributes'][x+3]['value']) / exp
        #     if sender == addr:
        #         type = 'Deposit'
        #     if receiver == addr:
        #         type = 'Withdrawal'
        #     line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #     data.append(line)

        # def swap_from_contract(event, x, addr, time, hash, data) :
        #     type = 'Withdrawal'
        #     ticker = event['attributes'][x+1]['value'].upper()
        #     amount = float(event['attributes'][x+3]['value'])
        #     line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #     data.append(line)
        #     type = 'Deposit'
        #     ticker = event['attributes'][x+2]['value'].upper()
        #     amount = float(event['attributes'][x+4]['value'])
        #     line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #     data.append(line)

        # def claim_from_contract(event, x, addr, time, hash, data, ticker) :
        #     type = 'Deposit'
        #     amount = float(event['attributes'][x+3])
        #     line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #     data.append(line)

        # def process_from_contract(raw_event, addr, time, hash, data):
        #     for event in raw_event:
        #         for x in range(1, len(event['attributes'])):
        #             if event['attributes'][x]['key'] == 'action':
        #                 contract_address = event['attributes'][x-1]['value']
        #                 contract_data = get_contract_symbol(contract_address)
        #                 ticker = contract_data['ticker']
        #                 exp = contract_data['exp']

        #                 if event['attributes'][x]['value'] == 'transfer':
        #                     transfer_from_contract(event, x, addr, time, hash, data, exp, ticker)
                        
        #                 # What fees do we account for ?
        #                 if event['attributes'][x]['value'] == 'swap':
        #                     swap_from_contract(event, x, addr, time, hash, data)
                        
        #                 if event['attributes'][x]['value'] == 'claim' :
        #                     if event['attributes'][x+2]['value'] == addr:
        #                         claim_from_contract(event, x, addr, time, hash, data, ticker)

        # def process_coin_received(raw_event, addr, time, hash, data):
        #     coin = []
        #     type = 'Deposit'
        #     for x in range(0, len(raw_event['attributes']), 2) :
        #         coin.append([raw_event['attributes'][x]['value'], raw_event['attributes'][x+1]['value']])
        #     for c in coin:
        #         if c[0] == addr:
        #             amount = get_amount(c[1])
        #             ticker = get_ticker(c[1])
        #             line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #             data.append(line)
        #     return data

        # def process_coin_spent(raw_event, addr, time, hash, data):
        #     coin = []
        #     type = 'Withdrawal'
        #     for x in range(0, len(raw_event['attributes']), 2) :
        #         coin.append([raw_event['attributes'][x]['value'], raw_event['attributes'][x+1]['value']])
        #     for c in coin:
        #         if c[0] == addr:
        #             amount = get_amount(c[1])
        #             ticker = get_ticker(c[1])
        #             line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #             data.append(line)
        #     return data
        return

    def process_transfer(self, raw_event, addr, time, hash, data):
        transfers = []
        type = ''
        for x in range(0, len(raw_event['attributes']), 3):
            transfers.append(
                [
                raw_event['attributes'][x]['value'],
                raw_event['attributes'][x+1]['value'],
                raw_event['attributes'][x+2]['value']
                ])
        for transfer in transfers:
            if transfer[0] == addr:
                type= 'Deposit'
            elif transfer[1] == addr:
                type = 'Withdrawal'
            if type:
                for a in transfer[2].split(',') :
                    ticker = self.get_ticker(a)
                    amount =  self.get_amount(a) / 1e6
                    line = [addr, hash, ticker, amount, type, time, self.block_explorer]
                    data.append(line)
        return data

    def comment2():
        # def process_swap(raw_event, addr, time, hash, data ):
        #     for a in raw_event['attributes']:
        #         if a['key'] == 'offer' or a['key'] == 'swap_fee':
        #             type = 'Withdrawal'
        #         if a['key'] == 'swap_coin':
        #             type = 'Deposit'
        #         amount = get_amount(a['value'])
        #         ticker = get_ticker(a['value'])
        #         line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #         data.append(line)
        #     return data

        # def process_withdraw_rewards(raw_event, addr, time, hash, data):
        #     type = 'Deposit'
        #     for x in raw_event['attributes']:
        #         if x['key'] == 'amount':
        #             for a in x['value'].split(',') :
        #                 amount = get_amount(a)
        #                 ticker = get_ticker(a)
        #                 line = [addr, hash, ticker, amount, type, time, 'finder.terra.money']
        #                 data.append(line)
        #     return data

        # def process_unbond(raw_event, addr, time, hash, staking_data):
        #     type = 'Unbond'
        #     for a in raw_event['attributes']:
        #         if a['key'] == 'amount':
        #             amount = float(a['value'])
        #         if a['key'] == 'completion_time' :
        #             completion_time = datetime.strptime(a['value'], '%Y-%m-%dT%H:%M:%SZ') #.strftime('%Y-%m-%d %H:%M:%S')
        return

    def process_transaction_fee(self, transaction, addr, time, hash, data):
        value = transaction['tx']['value']
        if 'sender' in value['msg'][0]['value'] and value['msg'][0]['value']['sender'] == addr:
            for a in value['fee']['amount'] :
                amount = int(a['amount']) #/ 1e6
                ticker = a['denom'].upper()
                line = [addr, hash, ticker, amount, 'Withdrawal', time, self.block_explorer]
                data.append(line)
        return data

    def process_transactions(self, txs, addr):
        data = []
        #header = ['Wallet', 'Hash', 'Ticker', 'Amount', 'Type', 'Time', 'Block Explorer']

        for t in txs:
                time = datetime.strptime(t['timestamp'], '%Y-%m-%dT%H:%M:%SZ') #.strftime('%Y-%m-%d %H:%M:%S')
                hash = t['txhash']
                #ticker = 'LUNA'
                self.process_transaction_fee(t, addr, time, hash, data)
                try:
                    raw_log = json.loads(t['raw_log'])
                    for r in raw_log:
                        for raw_event in r['events'] :
                            if raw_event['type'] == 'transfer' :  
                                self.process_transfer(raw_event, addr, time, hash, data)
                            # elif raw_event['type'] == 'swap' :
                            #     process_swap(raw_event, addr, time, hash, data)
                            # elif raw_event['type'] == 'withdraw_rewards':
                            #     process_withdraw_rewards(raw_event, addr, time, hash, data)
                #             elif raw_event['type'] == 'coin_spent':
                #                 process_coin_spent(raw_event, addr, time, hash, data)
                #             elif raw_event['type'] == 'coin_received' :
                #                 process_coin_received(raw_event, addr, time, hash, data)
                            # elif raw_event['type'] == 'from_contract' :
                            #     process_from_contract(raw_event, addr, time, hash, data, ticker)
                except:
                    pass

        return pd.DataFrame(data)

    def get_transactions(self, addr):
    
        if not addr.startswith('terravaloper') :
            url = f'https://fcd.terra.dev/v1/txs?account={addr}&limit=100'
            tmp = json.loads(requests.get(url).text)
            txs = [t for t in tmp['txs']]
            while 'next' in tmp:
                offset = tmp['next']
                url = f'https://fcd.terra.dev/v1/txs?account={addr}&limit=100&offset={offset}'
                tmp = json.loads(requests.get(url).text)
                txs.extend([t for t in tmp['txs']])
        
            return self.process_transactions(txs, addr)
            
chain_configurations = [
    ('Terra', 'finder.terra.money', 'LUNA')
]

# Build a dictionary of Covalenth API class instances 
# for parsing for each chain config
interfaces = {c[0]: Terra(*(c[1:])) 
                for c in chain_configurations}
             