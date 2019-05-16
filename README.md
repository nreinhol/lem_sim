# LEM Simulation
**A blockchain-based local energy market (LEM) simulation.**

## Motivation of LEM
The generation from distributed renewable energy sources (RES) is constantly increasing. In contrast to power plants which run by non-renewable fossil fuels, distributed RES produce energy in a decentralized and volatile way, which is hard to predict. These characteristics of the distributed RES challenge the current energy system. The existing electric grid is build for centralized generation by large power plants and the design of the current wholesale markets is not able to react in real-time to a significant amount of distributed RES. Therefore, new market approaches are needed, to successfully integrate the increasing amount of distributed RES. A possible solution to the technical and market problems is Peer-to-Peer (P2P) energy trading in local energy markets (LEM).  
LEM, also called microgrid energy markets, consist of small scale prosumers, consumers and a market platform which enables the trading of locally generated energy between the parties of a community.

## Requirements
* Python 3.6
* Truffle v5.0
* Docker v18.0
* GNU Make

## Installation
1. First of all, we have to start the local blockchain. For this type in:

```docker-compose up ganache```

2. After that, we need to deploy the smart contract into the running local blockchain. Therefore, we open another terminal window and change the directory to:

```cd /path/to/lem_sim/dealer```

3. To deploy the smart contract, type in the following expression:

```truffle migrate --network development```

4. After these steps, the blockchain and the smart contract are ready for communication. 
Now, we move to the python application. Therefore, change the directory to:

```cd path/to/lem_sim/pyapp```

5. Now, you need to set up the python virtual environment. Therefore, type in the following expression:

```make requirements```

6. This expression will create a virtual environment in the folder ```pyapp/env``` and install all required python packages into this virtual environment.
After the successful set up, type in the following expression to run the python simulation

```make simulate```

