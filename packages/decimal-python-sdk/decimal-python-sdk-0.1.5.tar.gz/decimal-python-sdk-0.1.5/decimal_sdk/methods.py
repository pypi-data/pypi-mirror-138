import json

from .wallet import Wallet
from .api import DecimalAPI
from .transactions import SendCoinTransaction


def SendAllCoin(api: DecimalAPI, wallet: Wallet, receiver: str, coin_name: str, options = {}):
    ''' Send all coins from wallet '''

    try:
        wallet_data = json.loads(api.get_address(wallet.get_address()))
        balance = '0'
        if wallet_data["ok"]:
            balance = wallet_data["result"]["address"]["balance"][coin_name]
            print(wallet_data["result"]["address"]["balance"])
        balance = int(balance) * pow(10, -18)

        tx = SendCoinTransaction(wallet.get_address(), receiver, coin_name, balance) #transaction for calculation commission
        wallet_balance = balance
        if(coin_name == 'del' or coin_name == 'tdel'):
            wallet_balance = wallet_balance -  api.estimate_tx_fee(tx, wallet, options)

        tx1 = SendCoinTransaction(wallet.get_address(), receiver, coin_name, wallet_balance)

        return api.send_tx(tx1, wallet, options)

    except Exception as e:
        return str(e)