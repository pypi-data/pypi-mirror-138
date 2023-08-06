import requests
import json
import csv
import datetime

url_prefix = 'https://node.deso.org/api/v1'

addrs = [
    'BC1YLgSCCq3b6mCmdiviV6nwW2PmnqvoebmAggcKqr5dEDDbzLyVrxs',
    'BC1YLgSBWbN3PxHrDTRvjMtYdA1mTEXZ8x35fZozWaVo8yBEipFm8WJ',
    'BC1YLheYMsM27NFDakSFc93SWcWfJww5quuKCAQD6FT99LJ3oCCoVC5'
    ]

headers = {'Content-Type' : 'application/json'}

with open('C:\\Users\\jsilverman\\deso.csv', 'w', newline='') as csvfile:
    transferdata = csv.writer(csvfile, delimiter=",")
    transferdata.writerow(['Wallet, Ticker, Hash, Amount, Type, Time, Block Explorer'])
    for a in addrs:
        payload = {'PublicKeyBase58Check' : a}
        transaction_url = url_prefix + '/transaction-info'
        tx = json.loads(requests.post\
            (transaction_url, headers=headers, json=payload).text)['Transactions']
        for t in tx:
            hash = t['TransactionIDBase58Check']
            data_raw = {'BlockHashHex' : t['BlockHashHex']}
            block_url = url_prefix + '/block'
            tstamp = json.loads(requests.post\
                (block_url, headers=headers, json=data_raw).text)\
                    ['Header']['TstampSecs']
            time = datetime.datetime.utcfromtimestamp(tstamp)\
                .strftime('%Y-%m-%d %H:%M:%S')
            #if t['TransactionType'] == 'BASIC_TRANSFER' :
            # if 'Inputs' in t:
            #     for i in t['Inputs'] :
            #         if a in i['PublicKeyBase58Check']:
            #             type = 'Withdrawal'
            #             amount = i['AmountNanos']
            for o in t['Outputs'] :
                if a in o['PublicKeyBase58Check']:
                    type = 'Deposit'
                    amount = o['AmountNanos']
            # elif t['TransactionType'] == 'BLOCK_REWARD' :
            #     type = 'Deposit'
            #     for o in t['Outputs']:
            #         if o['PublicKeyBase58Check'] == a:
            #             amount = o['AmountNanos']
            #             type = 'Deposit'
            # transferdata.writerow\
            # (['Wallet, Ticker, Hash, Amount, Type, Time, Block Explorer'])
            transferdata.writerow([a, 'DeSo', hash, amount, type, time, 'https://explorer.deso.org/'])
        csvfile.write('\n')
    csvfile.write('\n')

        