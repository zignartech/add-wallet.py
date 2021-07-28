# Copyright 2020 IOTA Stiftung
# SPDX-License-Identifier: Apache-2.0


import iota_wallet as iw
import os
from dotenv import load_dotenv



def account_manager(user):
    # Load the env variables
    load_dotenv()

    # Get the stronghold password
    STRONGHOLD_PASSWORD = os.getenv('STRONGHOLD_PASSWORD')
    # This example checks the account balance.
    account_manager = iw.AccountManager(
        storage_path='./alice-database'
    )

    account_manager.set_stronghold_password(STRONGHOLD_PASSWORD)

    # get a specific instance of some account
    account = account_manager.get_account(user)
    print(f'Account: {account.alias()}')

    return account



