import json
import requests
from datetime import datetime
import re
from hashlib import md5
import pandas as pd

class Terra:
    def __init__(self):
        self.ticker = 'TERRA'
    
    def write_tx(wallet, hash, ticker, amount, type, time):
        block_explorer = 'finder.terra.money'
        line = [wallet, hash, ticker, amount, type, time, block_explorer]
        return line

    def write_staking_tx(wallet, hash, amount, type, time, validator, validator_address, unbond_time=None):
        line = [wallet, hash, amount, type, time, validator, validator_address, unbond_time]
        return line

    def create_hash(line):
        string = f'{line[0]}{line[1]}{line[2]}{line[3]}{line[4]}'
        key = md5(string.encode('utf-8')).hexdigest()
        return key  
    
    def create_staking_hash(line):
        string = f'{line[0]}{line[1]}{line[2]}{line[3]}{line[5]}'
        key = md5(string.encode('utf-8')).hexdigest()
        return key 

class AttributeParser(Terra):
    def __init__(self, recipient, sender, amount, date=None):
        super().__init__()
        self.recipient = recipient
        self.sender = sender
        self.amount = amount
        self.date = date
        
    
    def format_amount(value):
        return int(re.findall('\d*\.?\d+', value)[0])

    def format_ticker(value):
        return re.findall('[a-z]+', value)[0].upper()

    def get_type(self, wallet):
        if self.sender ==  wallet :
            return 'Withdrawal'
        elif self.recipient == wallet:
            return 'Deposit'
        else: # Should never be Other!
            return 'Other'
    
    def get_amounts(self):
        amounts = []
        for value in self.amount.split(','):
            amount = AttributeParser.format_amount(value)
            ticker = AttributeParser.format_ticker(value)
            amounts.append[{'amount' : amount, 'ticker' : ticker}]
        return amounts
    

class CoinReceivedEvent(AttributeParser):
    def __init__(self, event):
        self.coin_received = []
        super().__init__()
        for x in range(0, len(event), 2):
            assert event[x]['key'] == 'receiver'
            assert event[x+1]['key'] == 'amount'

            self.coin_received.append(AttributeParser(event[x]['value'], 'contract', event[x+1]['value']))
    

    def process_coin_received(self, addr, hash, time):
        coin_received_data = []
        for coin_received in self.coin_received :
            if coin_received.recepient == addr:
                amount = AttributeParser.format_amount(coin_received.amount)
                ticker = AttributeParser.format_ticker(coin_received.amount)
                coin_received_data.append(coin_received.write_tx(addr, hash, ticker, amount, type, time)) 
        return coin_received_data


class CoinSpentEvent(AttributeParser):
    def __init__(self, event):
        super().__init__()
        self.coin_spent = []
        for x in range(0, len(event), 2):
            assert event[x]['key'] == 'spender'
            assert event[x+1]['key'] == 'amount'

            self.coin_spent.append(AttributeParser('contract', event[0]['value'], event[x+1]['value']))
    
    def process_coin_spent(self, addr, hash, time):
        coin_spent_data = []

        for coin_spent in self.coin_spent :
            if coin_spent.sender == addr:
                amount = AttributeParser.format_amount(coin_spent.amount)
                ticker = AttributeParser.format_ticker(coin_spent.amount)
                coin_spent_data.append(coin_spent.write_tx(addr, hash, ticker, amount, type, time)) 
        return coin_spent_data


class TransferEvent(AttributeParser):
    def __init__(self, event):
        super().__init__()
        self.transfers = []
        for x in range(0, len(event), 3):
            assert event[x]['key'] == 'recipient'
            assert event[x+1]['key'] == 'sender'
            assert event[x+2]['key'] == 'amount'

            self.transfers.append(AttributeParser(event[x]['value'], event[x+1]['value'], event[x+2]['value']))
    
    def process_transfer(self, addr, hash, time):
        transfer_data = []
        for transfer in self.transfers :
            type = transfer.get_type(addr)
            for value in transfer.get_amounts():
                ticker = value['ticker']
                amount = value['amount']
                transfer_data.append(transfer.write_tx(addr, hash, ticker, amount, type, time)) 
        return transfer_data


class WithdrawRewardsEvents(AttributeParser):
    def __init__(self, event, addr):
        super().__init__()
        self.wr = []
        self.type = 'Deposit'
        for x in event:
            if x['key'] == 'amount' :
                self.amount = x['value']
                self.wr.append(AttributeParser(addr, 'sender', self.amount))

    def process_withdraw_rewards(self, addr, hash, time):
        rewards_data = []
        type = self.type
        for withdraw_reward in self.wr:
            for value in withdraw_reward.get_amounts():
                ticker = value['ticker']
                amount = value['amount']
                rewards_data.append(withdraw_reward.write_tx(addr, hash, ticker, amount, type, time)) 
        return rewards_data



class SwapEvent(AttributeParser):
    def __init__(self):
        super().__init__()
        self.swap = []

    def process_swap(raw_event, addr, hash, time):
        swap_data = []   
        for attribute in raw_event['attribute'] :
            amount = AttributeParser.format_amount(attribute['value'])
            ticker = AttributeParser.format_ticker(attribute['value'])

            if attribute['key'] == 'offer' or attribute['key'] == 'swap_fee':
                type = 'Withdrawal'     
            if attribute['key'] == 'swap_coin' :
                type = 'Deposit'

            swap_data.append(SwapEvent().write_tx(addr, hash, ticker, amount, type, time))
        return swap_data

class UnbondEvent(AttributeParser) :
    def __init__(self, event, addr):
        super().__init__()
        self.unbond_event = []
        self.type = 'Withdrawal'
        for x in event:
            if x['key'] == 'amount' :
                amount = x['value']
            if x['key'] == 'completion_time' :
                time = datetime.strptime(x['value'], '%Y-%m-%dT%H:%M:%SZ') #.strftime('%Y-%m-%d %H:%M:%S')
            if x['key'] == 'validator':
                recipient = x['value']
            self.unbond_event.append(AttributeParser(recipient, addr, amount, time))
    
    def get_validator_address(validator):
        url = f'https://fcd.terra.dev/v1/staking/validators/{validator}'
        return json.loads(requests.get(url).text)['accountAddress']
    
    def process_unbond(self, hash,time):
        unbond_data = []
        for event in self.unbond_event:
            validator_address = self.get_validator_address(event.recipient)
            line = unbond_data.append(self.unbond_event.write_staking_tx(\
                self.sender, hash, self.amount, 'Deposit', time, self.recipient, validator_address, unbond_time=self.date))
        return line


terra_addr = [
    'terra18ccykpx2zsck98qgpyhrwx5herd55n4uhk3v2v', 
    'terra133yelhl428xwclf72cu33lcpwuw87cany3mw0l', 
    'terra18c43y4lhch25tdwkrfkflkksz8dfhg4p40gt95'
    ]

def get_transactions(self, addr_list):
    txs = []
    data = {}
    staking_info = []
    
    for addr in terra_addr:

        url = f'https://fcd.terra.dev/v1/txs?account={addr}&limit=100'
        tmp = json.loads(requests.get(url).text)
        #wallet = addr
        txs.extend([t for t in tmp['txs']])

        # Terra API limits to 100 txs per call
        while 'next' in tmp:
            offset = tmp['next']
            url = f'https://fcd.terra.dev/v1/txs?account={addr}&limit=100&offset={offset}'
            tmp = json.loads(requests.get(url).text)
            txs.extend([t for t in tmp['txs']])
            

        for t in txs:
            time = datetime.strptime(t['timestamp'], '%Y-%m-%dT%H:%M:%SZ') #.strftime('%Y-%m-%d %H:%M:%S')
            hash = t['txhash']
            ticker = 'LUNA'
            exp = 1
            try:
                raw_log = json.loads(t['raw_log'])
                for r in raw_log:
                    for raw_event in r['events'] :

                        if raw_event['type'] == 'transfer' :
                            transfer_event = TransferEvent(raw_event)
                            transfer_data = transfer_event.process_transfer(addr, hash, time)
                            for line in transfer_data:
                                key = transfer_event.create_hash(line)
                                data[key] = line

                        if raw_event['type'] == 'swap' :
                            swap_event = SwapEvent()
                            swap_data = swap_event.process_swap(raw_event, addr, hash, time)
                            for line in swap_data:
                                key = swap_event.create_hash(line)
                                data[key] = line

                        if raw_event['type'] == 'coin_received' :
                            coin_received_event = CoinReceivedEvent(raw_event)
                            coin_received_data = coin_received_event.process_coin_received(addr, hash, time)
                            for line in coin_received_data:
                                key = coin_received_event.create_hash(line)
                                data[key] = line

                        if raw_event['type'] == 'coin_spent' :
                            coin_spent_event = CoinSpentEvent(raw_event)
                            coin_spent_data = coin_spent_event.process_coin_spent( addr, hash, time)
                            for line in coin_spent_data:
                                key = coin_spent_event.create_hash(line)
                                data[key] = line

                        if raw_event['type'] == 'withdraw_rewards' :
                            wr = WithdrawRewardsEvents(raw_event)
                            wr_received_data = wr.process_withdraw_rewards(addr, hash, time)
                            for line in wr_received_data:
                                key = wr.create_hash(line)
                                data[key] = line

                        if raw_event['type'] == 'unbond' or raw_event['type'] == 'delegate' :
                            staking_info.append(raw_event) 
                                    
                        # for a in e['attributes'] :
                        #     if a['key'] == 'to' and a['value'] == addr:
                        #         type = 'Deposit'
                        #     if a['key'] == 'from' and a['value'] == addr:
                        #         type = 'Withdrawal'
                        #     if a['key'] == 'amount' :
                        #         amount = int(a['value'])
                        #     if a['key'] == 'contract_address':
                        #         contract_addr = a['value']
                        #         url = f'https://fcd.terra.dev/v1/wasm/contract/{contract_addr}'
                        #         con_addr = json.loads(requests.get(url).text)['init_msg']
                        #         for k,v in con_addr.items():
                        #             if k == 'symbol':
                        #                 ticker = v
                        #             if k == 'decimals':
                        #                 exp = v
                        #             if k.endswith('_token'):
                        #                 contract_address = v 
                        #                 url = f'https://fcd.terra.dev/v1/wasm/contract/{contract_address}'
                        #                 ticker = json.loads(requests.get(url).text)['init_msg']['symbol']
                        #                 exp = json.loads(requests.get(url).text)['init_msg']['decimals']
                    
            
            except:
                pass

    transaction_list = [v for v in data.values()]
    return pd.DataFrame(transaction_list)#.to_csv(r'C:\Users\jsilverman\Terra.csv', index=False)


def get_staking_info(staking_info):
    staking_data = []
    for event in staking_info :
        if event['type'] == 'unbond' :
            type = 'Deposit'
        if event['type'] == 'delegate' :
            type = 'Withdrawal'
    return pd.DataFrame(staking_data)