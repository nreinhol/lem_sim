import time
from web3 import Web3, HTTPProvider


def get_network_connection(connection):
    
    if(connection == 'docker'):
        network_address = 'HTTP://ganache:8545'
        time.sleep(10)
    elif(connection == 'port'):
        network_address = 'HTTP://0.0.0.0:8545'
    else:
        click.secho('No connection address specified!', fg='red')
        quit()

    return Web3(HTTPProvider(network_address))
