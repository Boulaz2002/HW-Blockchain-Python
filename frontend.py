from bit import transaction
import streamlit as st
from wallet import *




st.title("Send Token to any Address")

token = st.selectbox("Select Your Coin", (BTCTEST, ETH))
index = st.selectbox("Token Index", (0, 1, 2))
receiver_address = st.text_input("Receiver Address")
amount_to_send = st.number_input("Amount in Ether")

priv_key = privat_key(token, index)

accoun = priv_key_to_account(token, priv_key)



st.sidebar.write(accoun.address)
if token == ETH:
    balance = get_balance(accoun.address)
    st.sidebar.write(balance)


if st.button("SEND TOKEN"):
    trans = send_tx(token, accoun, receiver_address, amount_to_send, index)
    

    st.sidebar.write(f"the Account Address {accoun.address} successfull sent")
    st.sidebar.write(f"{amount_to_send} Ether" )
    st.sidebar.write(f"To {receiver_address}" )
