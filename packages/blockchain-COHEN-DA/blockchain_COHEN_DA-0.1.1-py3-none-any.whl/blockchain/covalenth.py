"""Returns transactions for all chains served by Covalenth API"""
import json
from datetime import datetime
import requests
import pandas as pd

from .chain_interface import ChainInterface

class CovalenthAPIClient(ChainInterface):
    """Defines CovalenthClass()"""
    def __init__(self, chain_id, block_explorer, ticker):
        super().__init__()
        self.ckey = 'ckey_d5a5850f10a046d9b28e72408df'
        self.chain_id = chain_id
        self.block_explorer = block_explorer
        self.ticker = ticker
        

    def write_tx(self, wallet, txhash, ticker, amount,
        transaction_type, time, block_explorer, event_type):
        """Writes out one transaction in order"""
        row = [wallet, txhash, ticker, amount, transaction_type, time, block_explorer, event_type]
        return row

    def _parse_transaction(self, wallet, transaction, data):
    
        ticker = self.ticker
        txhash = transaction['tx_hash']

        time = datetime.strptime(transaction['block_signed_at'], '%Y-%m-%dT%H:%M:%SZ')

        # Fee processing
        if transaction['from_address'] == wallet:
            fee = (transaction['gas_spent'] * transaction['gas_price']) / 1e18
            amount = fee
            transaction_type = 'Withdrawal'
            line = self.write_tx(wallet, txhash, ticker, amount,
                transaction_type, time, self.block_explorer, '')
            data.append(line)

        # Main transaction
        if transaction['to_address'] == wallet:
            transaction_type = 'Deposit'

        elif transaction['from_address'] == wallet:
            transaction_type = 'Withdrawal'

        else:
            transaction_type = None


        if transaction_type:
            amount = int(transaction['value'])/1e18


            line = self.write_tx(wallet, txhash, ticker, amount,
                    transaction_type, time, self.block_explorer, '')
            data.append(line)


        for event in transaction['log_events'] :
            ticker = event['sender_contract_ticker_symbol']
            if not ticker:
                continue

            exp = event['sender_contract_decimals']
            if not exp:
                exp = 18

            if event['decoded'] and event['decoded']['params']:
                if event['decoded']['name'] == 'Swap':
                    continue

                params = event['decoded']['params']

                deposit = [p for p in params if p['name'] == 'to' and p['value'] == wallet]
                if deposit:
                    transaction_type = 'Deposit'

                withdrawal = [p for p in params if p['name'] == 'from' and p['value'] == wallet]
                if withdrawal:
                    transaction_type = 'Withdrawal'

                value = [p['value'] for p in params if p['name'] == 'value']
                if value:
                    if value[0] :
                        amount = int(value[0]) / pow(10,exp)

                if deposit or withdrawal:
                    line = self.write_tx(wallet, txhash, ticker, amount,
                            transaction_type, time, self.block_explorer, '')
                    data.append(line)


        return data

    def _get_transactions_for_wallet(self, wallet, data):
        #data = []
        url = f'https://api.covalenthq.com/v1/{self.chain_id}/address/{wallet}/transactions_v2/?page-size=10000&key={self.ckey}'
        transactions = json.loads(requests.get(url).text)['data']['items']
        for transaction in transactions:
            if transaction['successful']:
                self._parse_transaction(wallet.lower(), transaction, data)
        #self._parse_transactions(wallet.lower(), transactions, data )
        return data

    def get_transactions(self, wallet):
        """get_transactions(), called by main()"""
        #transactions = []
        transactions = []
        self._get_transactions_for_wallet(wallet.lower(), transactions)
        wallet_transactions = pd.concat([pd.DataFrame(transactions)], ignore_index=True)
        return wallet_transactions

chain_configurations = [
    ('Ronin', 2020, 'explorer.roninchain.com', 'RONIN'),
    ('Polygon', 137, 'polygonscan.com', 'MATIC'),
    ('Binance Smart Chain', 56, 'bscscan.com', 'BNB'),
    ('Fantom', 250, 'ftmscan.com', 'FTM'),
    ('MoonBeam', 1284, 'blockscout.moonbeam.network', 'GLMR'),
    ('MoonRiver', 1285, 'blockscout.moonriver.moonbeam.network', 'MOVR'),
    ('RSK', 30, 'explorer.rsk.co', 'RSK'),
    ('Arbitrum', 42161, 'explorer.offchainlabs.com', 'ARB'),
    ('Palm', 11297108109, 'explorer.palm.io', 'Palm'),
    ('Klayton', 8217, 'scope.klaytn.com', 'KLAY'),
    ('HECO', 128, 'hecoinfo.com', 'HECO'),
    ('iotex', 4689, 'iotexscan.io', 'IOTX'),
    ('EvMos', 900, 'explorer.evmos.org', 'PHOTON')
]

# Build a dictionary of Covalenth API class instances
# for parsing for each chain config
interfaces = {c[0]: CovalenthAPIClient(*(c[1:]))
                for c in chain_configurations}
