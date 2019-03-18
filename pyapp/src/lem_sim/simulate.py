from lem_sim import agent
from lem_sim import linear_optimization as lp

from web3 import Web3, HTTPProvider
from scipy.optimize import linprog
import time

#connection to local blockchain
time.sleep(10)
web3 = Web3(HTTPProvider('HTTP://ganache:8545'))

#get all existing accounts 
accounts = web3.eth.accounts

#instantiate agents and assign accounts
agents_list = []
for account in accounts:
    agents_list.append(agent.Agent(account, web3))

#create optimization problem
target_coefs = [-1, -2, -1, -3]
constraint_coefs = [[2, 0, 1, 1], [1, 0, 3, 1], [0, 2, 2, 1], [0, 3, 1, 1]]
constraint_bounds = [4, 9, 8, 5]
central_problem = lp.OptimizationProblem(target_coefs, constraint_coefs, constraint_bounds)

#get two specific agents out of list
agent_one = agents_list[0]
agent_two = agents_list[1]

print('balance before tx: {}'.format(agent_two.balance))
agent_one.send_transaction(agent_two.account_address, 1000000000000000000)
print('balance after tx: {}'.format(agent_two.balance))
