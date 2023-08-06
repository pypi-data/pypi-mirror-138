import json
import requests
import pandas as pd
from datetime import datetime


class Substrate(object):
    def __init__(self, fundtype, ticker, normalize):
        super().__init__()

        self.key = 'd94168c2880f1fca96af660fa7561a25'
        self.fund_type = fundtype
        self.ticker = ticker,
        self.title = ['Wallet', 'Hash', 'Ticker', 'Amount', 'Type', 'Time', 'Block Explorer']
        self.block_explorer = f"https://{self.fund_type}.subscan.io"
        self.url = f'https://{self.fund_type}.api.subscan.io/api/scan/transfers'
        self.headers = {'Content-Type': 'application/json', 'X-API-Key': self.key}
        self.row = 100
        self.page = 0
        self.normalize = pow(10, normalize)


    def write_tx(wallet, hash, ticker, amount, type, time, block_explorer):
        line = [wallet, hash, ticker, amount, type, time, block_explorer]
        return line

    def _get_transactions_for_wallet(self, wallet):
            data_raw = {'row' : self.row, 'page' : self.page, 'address' : wallet}
            transfers = json.loads(requests.post(url=self.url, headers=self.headers, json=data_raw).text)
            count = transfers['data']['count']
            transactions = transfers['data']['transfers']
            while count > 100:
                count = count - 100
                page = page + 1
                data_raw['page'] = page
                temp = json.loads(requests.post(url=self.url, headers=self.headers, json = data_raw).text)
                for t in temp['data']['transfers']:
                    transactions.append(t)
                
            self._parse_transactions(wallet, transactions)
        

    def get_transactions(self, address_list):
        for wallet in address_list:
            transactions = self._get_transactions_for_wallet(wallet)
        return pd.DataFrame(transactions, columns=self.title)#.to_csv(r'C:\Users\jsilverman\Moonriver.csv', index=False)

    def _parse_transactions(self, wallet, transactions):
        data = []
        for tx in transactions:
            if tx['to'] == wallet:
                type = "Deposit"
            elif tx['from'] == wallet:
                type = "Withdrawal"
            else:
                type = "Other"

            hash = tx['hash']
            amount = float(tx['amount'])
            #if tx['block_num'] < 1248328 and self.ticker == 'DOT' :
            #   amount = amount * 100
            time =  datetime.utcfromtimestamp(tx['block_timestamp'])#.strftime('%Y-%m-%d %H:%M:%S')
            line = self.write_tx(wallet, hash, self.ticker, amount, type, time, self.block_explorer)
            data.append(line)

