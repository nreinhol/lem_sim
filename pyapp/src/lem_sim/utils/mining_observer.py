import time

def wait_for_new_block(var):
    while var.latest_block >= var.web3.eth.getBlock('latest')['number']:
        time.sleep(0.5)
    
    var.latest_block = var.web3.eth.getBlock('latest')['number']
