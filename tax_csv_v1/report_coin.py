# -*- coding: utf-8 -*-
import logging
import requests
from urllib.parse import urlunparse, urlencode
SCHEME = "https"

import coin.processor
from common import report_util
from common.Exporter import Exporter

def _query_get(netloc, uri_path, query_params):
    url = urlunparse((
        SCHEME,
        netloc,
        uri_path,
        None,
        urlencode(query_params),
        None,
    ))

    logging.info("Querying url=%s...", url)
    response = requests.get(url)

    return response.json()

import time

#LIMIT = 25

from common.super_global import initialize
def _query(uri_path, query_params={}, sleep_seconds=1):
    result = _query_get(app.api, uri_path, query_params)
    time.sleep(sleep_seconds)
    return result

def get_count_txs(app):
#    uri_path = f"/cosmos/tx/v1beta1/txs?events=message.sender=%27{address}%27"
    uri_path = f"/txs?message.sender={app.wallet_address}&limit=20"
    data = _query(uri_path)
    total_transactions=data['total_count']
    pages =data["page_total"]
    return pages,total_transactions

def get_txs(app):
#    uri_path = f"/cosmos/tx/v1beta1/txs?events=message.sender=%27{address}%27"
    uri_path = f"/txs?message.sender={app.wallet_address}&limit=20"
    data = _query(uri_path)
    transactions= data["txs"]
    for page in range(2,int(data['page_total'])+1): #total no of pages
        uri_path_page=uri_path + f"&page={page}"
        data = _query(uri_path_page)
        transactions.extend(data['txs'])
    data_trans=list()
    for elem in transactions:
        txid = elem["txhash"]
        data=get_tx(txid)
        data_trans.extend([data])
    return data_trans


def get_tx(txid):
    uri_path = f"/cosmos/tx/v1beta1/txs/{txid}"
    data = _query(uri_path)
    return data

def txhistory(app, job=None):
    # Fetch count of transactions to estimate progress more accurately
    pages,total_transactions = get_count_txs(app)
    print("Transactions: {} in {} pages ".format(total_transactions,pages))
    # Fetch transactions
    elems = get_txs(app)
    print("Processing {} COIN transactions... ".format(len(elems)))
    exporter = Exporter(app)
 #   print(elems,type(elems))
    coin.processor.process_txs(app,elems,exporter)
    return exporter
# Now the fun begins

if __name__ == '__main__':
# Now the fun begins 
    with open("wallet.txt",'r',encoding = 'utf-8') as f:
        wallet_address= (f.read()).strip()
    app = initialize(wallet_address)
    exporter = txhistory(app, job=None)
    report_util.run_exports(app, exporter, 'koinly')



