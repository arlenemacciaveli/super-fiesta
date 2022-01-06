import re
import json

class initialize(object):
    def __init__(self, wallet_address):
        try:
            self.wallet_address=wallet_address
            chain, tail=re.compile("(?<=\D)(?=\d)").split(wallet_address,1)
            if(chain=='star'):
                chain='starname'
            try:
                with open('networks/'+chain+'.json') as f:
                    dummy=json.load(f)
            except:
                print('networks/'+chain+'.json' + ' not found')
            self.ticker=dummy['ticker']
            self.denom=dummy['denom']
            self.api=dummy['api']
            self.chain_name=dummy['chain_name'] 

        except:
            print('Configuration file read error')
                       
           