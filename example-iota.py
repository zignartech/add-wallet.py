# Copyright 2020 IOTA Stiftung
# SPDX-License-Identifier: Apache-2.0


import iota_wallet as iw
import os
from dotenv import load_dotenv

load_dotenv()

# Get the stronghold password
STRONGHOLD_PASSWORD = os.getenv('STRONGHOLD_PASSWORD')
# This example checks the account balance.
account_manager = iw.AccountManager(
    storage_path='./alice-database'
)
account_manager.set_stronghold_password(STRONGHOLD_PASSWORD)
# get a specific instance of some account
account = account_manager.get_account("CuentaZ")
print(f'Account: {account.alias()}')
# Always sync before doing anything with the account
print('Syncing...')
synced = account.sync().execute()

# Update alias
#account.set_alias('the new alias')

# Get unspent addresses
#unspend_addresses = account.list_unspent_addresses()
#print(f'Unspend addresses: {unspend_addresses}')

# Get spent addresses
#spent_addresses = account.list_spent_addresses()
#print(f'\nSpent addresses: {spent_addresses}')

# Get all addresses
addresses = account.addresses()
print(f'\nAll addresses: {addresses}')

# You can also get the latest unused address
last_address_obj = account.latest_address()
print(f"\nLast address: {last_address_obj['address']['inner']}")

# Generate a new unused address
#new_address = account.generate_address()
#print(f'New address: {new_address}')

# List messages
#messages = account.list_messages(5, 0, message_type='Failed')
#print(f'\nMessages: {messages}')