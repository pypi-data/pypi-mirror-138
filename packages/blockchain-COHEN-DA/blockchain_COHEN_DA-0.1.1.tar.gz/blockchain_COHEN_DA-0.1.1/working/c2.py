import json
import requests
from datetime import datetime
import pandas as pd


def _get_transactions_for_wallet(wallet):
    url = f'https://api.covalenthq.com/v1/{self.chain_id}/address/{wallet}/transactions_v2/?page-size=10000&key={self.ckey}'
    transactions = json.loads(requests.get(url).text)['data']['items']

    self._parse_transactions(wallet.lower(), transactions)

def _parse_transactions(wallet, transactions):
    data = []    
    
    for tx in transactions:
        ticker = self.ticker
        hash = tx['tx_hash']

        # Fee processing
        fee = (tx['gas_spent'] * tx['gas_price']) / 1e18
        amount = fee
        type = 'Withdrawal' 
        time = datetime.strptime(tx['block_signed_at'], '%Y-%m-%dT%H:%M:%SZ') #.strftime('%Y-%m-%d %H:%M:%S')
        
        line = self.write_tx(wallet, hash, ticker, amount, type, time, self.block_explorer)
        data.append(line)

        # Main transaction
        if tx['to_address'] == wallet:
            type = 'Deposit'
        elif tx['from_address'] == wallet:
            type = 'Withdrawal'
        else:
            type = None

        
        if type:
            amount = int(tx['value'])/1e18

            line = self.write_tx(wallet, hash, ticker, amount, type, time, self.block_explorer)
            data.append(line)


        for e in tx['log_events'] :
            ticker = e['sender_contract_ticker_symbol']
            if not ticker:
                continue

            exp = e['sender_contract_decimals']

            if e['decoded'] and e['decoded']['params']:
                params = e['decoded']['params']

                deposit = [p for p in params if p['name'] == 'to' and p['value'] == wallet]
                if deposit:
                    deposit = deposit[0]
                    type = 'Deposit'
                    
                withdrawal = [p for p in params if p['name'] == 'from' and p['value'] == wallet]
                if withdrawal:
                    withdrawal = withdrawal[0]
                    type = 'Withdrawal'

                value = [p for p in params if p['name'] == 'value']
                if value:
                    amount = int(value[0]) / pow(10,exp)
                
                if deposit or withdrawal:
                    line = self.write_tx(wallet, hash, ticker, amount, type, time, self.block_explorer)
                    data.append(line)

def get_transactions(self, addr) :

        

    df = pd.DataFrame(data, columns=self.header)
    return(df)