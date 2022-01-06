from common.make_tx import make_transfer_out_tx, make_transfer_in_tx, make_reward_tx
from common.super_global import initialize


with open("wallet.txt",'r',encoding = 'utf-8') as f:
  wallet_address= f.read()
  app = initialize(wallet_address)

def make_transfer_receive_tx(txinfo, received_amount, received_currency=None):
    if not received_currency:
        received_currency = app.ticker if txinfo.fee else ""

    return make_transfer_in_tx(txinfo, received_amount, received_currency)


def make_transfer_send_tx(txinfo, sent_amount, sent_currency=None):
    if not sent_currency:
        sent_currency = app.ticker if txinfo.fee else ""

    return make_transfer_out_tx(txinfo, sent_amount, sent_currency, None)


def make_coin_reward_tx(txinfo, reward_amount):
    return make_reward_tx(txinfo, reward_amount, app.ticker)
