import json
import requests
import pandas as pd
import datetime


class DOT:
    def get_transactions(addr):

        api_key = 'd94168c2880f1fca96af660fa7561a25'
        headers = {'Content-Type' : 'application/json', 'X-API-Key' : api_key}

        row = 100
        page = 0

        data = []
        normalize = 1e10

        title = ['Wallet, Ticker, Hash, Amount, Type, Time, Block Explorer']
        for r in addr :
            data_raw = {'row' : row, 'page' : page, 'address' : r['address']}
           

            url_prefix = "https://polkadot.api.subscan.io/api/scan/"
            transfer_url = url_prefix + "transfers"

            transfers = json.loads(requests.post\
                (url = transfer_url, headers = headers, json = data_raw).text)


            count = transfers['data']['count']
            tx_list = transfers['data']['transfers']
        
            while count > 100:
                count = count - 100
                page = page + 1
                data_raw['page'] = page
                temp = json.loads(requests.post(url=transfer_url, headers=headers, json = data_raw).text)
                for t in temp['data']['transfers']:
                    tx_list.append(t)
            

            for t in tx_list:
                if t['to'] == r['address'] :
                    transaction_type = "Deposit"
                elif t['from'] == r['address'] :
                    transaction_type = "Withdrawal"
                else:
                    transaction_type = "Other"
                wallet = r['address']
                ticker = 'DOT'
                hash = t['hash']
                amount = int(t['amount']) / normalize
                if t['block_num'] < 1248328:
                    amount = amount * 100
                time =  datetime.datetime.utcfromtimestamp(t['block_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                block_explorer = "https://polkadot.subscan.io"
                line = [wallet, hash, ticker, amount, transaction_type, time, block_explorer]
                data.append(line)
        df = pd.DataFrame(data, columns=title)
        return(df)