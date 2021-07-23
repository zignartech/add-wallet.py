import iota_wallet as iw
import os
from dotenv import load_dotenv


# Load the env variables
load_dotenv()

# Get the stronghold password
STRONGHOLD_PASSWORD = os.getenv('STRONGHOLD_PASSWORD')

account_manager = iw.AccountManager(
    storage_path='./alice-database'
)  # note: `storage` and `storage_path` have to be declared together

account_manager.set_stronghold_password(STRONGHOLD_PASSWORD)

# mnemonic (seed) should be set only for new storage
# once the storage has been initialized earlier then you should omit this step
#account_manager.store_mnemonic("Stronghold")

# general Tangle specific options
client_options = {
    "nodes": [
        {
            "url": "https://api.lb-0.testnet.chrysalis2.com",
            "auth": None,
            "disabled": False
        }
    ],
    "local_pow": False,
    'node_sync_interval': 15000, # in milliseconds
}

account = account_manager.get_account("CuentaZ")
print(f'Account: {account.alias()}')
account.set_client_options(client_options)

# an account is generated with the given alias via `account_initialiser`
#account_initialiser = account_manager.create_account(client_options)
#account_initialiser = account_manager.remove_account("wallet-account://14f5ec4290a9aea9261e12bb96988cc21e17d37ce00672943db697fb0938d0ae")
#account_initialiser.alias('Cesar')
#account_initialiser.alias('CuentaZ')

# initialise account based via `account_initialiser`
# store it to db and sync with Tangle
#account = account_initialiser.initialise()
#print(f'Account created: {account.alias()}')