import json
import requests
import pandas as pd
import datetime


start_time = '2021-01-01 0:00:00'
time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
start_time = datetime.datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, tzinfo=datetime.timezone.utc).timestamp()

end_time = '2021-01-01 0:00:00'
time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
end_time = datetime.datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, tzinfo=datetime.timezone.utc).timestamp()

mina_addr = [
    'B62qnDczgqibMNMnATpdsv6wXWtF63AdNz2bMncXwxo7i4QcMMhwwL5', 
    'B62qoY2cuwsNXaBE3yUwSqwEaovhwRqmGWjBhNL2AH5vCeeRgVsaxCG', 
    'B62qqoCMCrMCJ3Maw6RcKz565cJnapjiAXwXXjBYfH1oEuv8xND94zc', 
    'B62qknBg1mTvb9uXy9exbBsxs16BXgMQiJ5N73eEFXmWBLaRetqMvMb'
    ]
title = ['Wallet', 'Hash', 'Ticker', 'Amount', 'Type', 'Time', 'Block Explorer']
data = []
for addr in mina_addr:
    url = f'https://mina--mainnet--indexer.datahub.figment.io/apikey/fb726f8f6f2a73f02e51da311fb209f1/transactions?account={addr}'
    tx = json.loads(requests.get(url).text)

    for t in tx:
        timestamp = datetime.datetime.strptime(t['time'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
        if timestamp >= start_time and timestamp <= end_time :
            hash = t['hash']
            time = datetime.datetime.strptime(t['time'], '%Y-%m-%dT%H:%M:%SZ')#.strftime('%Y-%m-%d %H:%M:%S')
            if t['sender'] == addr :
                    type = 'Withdrawal'
                    amount = int(t['fee'])/1e9
                    line = [addr, hash, 'MINA', amount, type, time, 'minaexplorer.com']
                    data.append(line)
                    amount = int(t['amount'])/1e9
                    line = [addr, hash, 'MINA', amount, type, time, 'minaexplorer.com']
                    data.append(line)
            if t['receiver'] == addr:
                type = 'Deposit'
                line = [addr, hash, 'MINA', amount, type, time, 'minaexplorer.com']
                data.append(line)


pd.DataFrame(data, columns=title).to_csv('C:\\Users\\jsilverman\\MINA.csv', index=False)