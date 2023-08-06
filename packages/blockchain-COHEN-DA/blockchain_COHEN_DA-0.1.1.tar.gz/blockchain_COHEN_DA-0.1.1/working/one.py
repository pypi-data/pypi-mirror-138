from pyhmy import account 
from datetime import datetime
import pandas as pd
import csv

main_net = 'https://rpc.s0.t.hmny.io'
main_net_shard_1 = 'https://rpc.s1.t.hmny.io'
end_point = 'https://g.s0.t.hmny.io/archival'

address = [
    'one12vyznqd6lz6wwr9gkvd6q5zy9sswx792dh2eyv', 
    'one1a39hd09sc7lfyhp8yhejeyj6jc8mfp7qsd4tvs', 
    'one1fdtcrkpkhm2ppnu05zmddgqvledqh7g6r2tgdy',
    'one1v63cck8d08708mlgz8rmrku4l9jgvtmfn8a6wh'
     ]

block_num = 7331339 # Last block of 12/13/20 (found with trial and error)

tx_dict = {}
ticker = 'ONE'
explorer = 'explorer.harmony.one'

for a in address:
    tx_dict[a]=(account.get_transaction_history(a, include_full_tx=True, endpoint=end_point))
    tx_dict[a].extend(account.get_transaction_history(a, include_full_tx=True, endpoint=main_net_shard_1))

with open('harmonyONE_new.csv', 'w') as w:
    #tx_data = csv.writer(w, delimiter=",")

    for a in address:
        #tx_per_account = {}
        #tx_per_account = tx_data[a]
        for t in tx_dict[a]:
            amount = int(t['value'], base=16)/1e18
            timestamp = int(t['timestamp'], base=16)
            blocktime = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            if t['to'] == a:
                transaction_type = 'Deposit'
            elif t['from'] == a:
                transaction_type = 'Withdrawal'
            else:
                transaction_type = 'Other'
            w.write(a +", "+ ticker + ", " +t['hash'] +", "+str(amount) + ", " + transaction_type +", "+blocktime +", "+ explorer +"\n")
        w.write('\n')
    w.write("\n")




