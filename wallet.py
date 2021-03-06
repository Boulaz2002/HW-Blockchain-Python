# Import dependencies
from constant import *
import os
from dotenv import load_dotenv
import subprocess
import json
from eth_account import Account
from bit import PrivateKeyTestnet
from web3 import Web3
from web3.middleware import geth_poa_middleware
from bit.network import NetworkAPI

w3=Web3(Web3.HTTPProvider('http://localhost:7545'))

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constant import *
 
 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = f"./derive -g --mnemonic='{mnemonic}' --coin='{coin}' --numderive='{numderive}' --format=json"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    'btc-test' : derive_wallets(mnemonic, BTCTEST, 3), 
    'eth' : derive_wallets(mnemonic, ETH, 3)
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    if coin==ETH:
        return Account.privateKeyToAccount(priv_key)

def privat_key(coin, index):
    if index > 3 and index < 0:
       return print("Index must be between 0 and 3")
    else :
        return coins[coin][index]['privkey']



# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == ETH:
        return {
            "from": account.address,
            "to": to,
            "value": w3.toWei(amount,'ether'),
            "gas": w3.eth.estimateGas({
                "from": account.address,
                "to": to,
                "value": w3.toWei(amount, 'ether')
            }),
            "gasPrice": w3.eth.gasPrice,
            "nonce": w3.eth.getTransactionCount(account.address)
            #"chainID":
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, accoun, to, amount, index):
    raw_tx = create_tx(coin, accoun, to, amount)
    

    if coin == ETH:
        signed_tx = Account.sign_transaction(raw_tx, privat_key(coin, index))
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result

    elif coin == BTCTEST:
        signed_tx = accoun.sign_transaction(raw_tx) 
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

def get_balance(address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether
