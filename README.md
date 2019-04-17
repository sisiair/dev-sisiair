# About the project

This is a open source project, which is designed to serve for the simple market making purposes as well as the traditional simple quantitative trading requirements for cryptocurrencies

This system will for now include some basic building blocks of a trading system, such as alpha model, risk model, might include transaction cost model and optimization model. It depends on the time. 

## The current structure of the project:

accounts: multi-exchange account management

exchanges: exchange apis

files: abis for contractland's terra chain

handlers: independent tasks such as auto placing buy orders, sell orders and so on 

utils: the helper functions and classes of the system

system.ini: used to store the related properties

## Instruction

1. set set up a mongo database see: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

2. change the system.ini.example to system.ini, and fill out the config file system.ini

a. ContractLand's Terra Chain config

;testnet
;SOURCE_SALT=
;RPC_URL=https://gaia.terrachain.network/
;EXCHANGE_ADDRESS=0x856753Ab1D15779a2feeCE242c9f83F7D44D7322
;ETH_TOKEN_ADDRESS=0x664C933aE196bEe37d4A1225059cd0aF9444883e

;mainnet
SOURCE_SALT=
RPC_URL=https://mainnet.terrachain.network/
EXCHANGE_ADDRESS=0xF3aA5e90623e9deFc9273355E5253df07D28A928
ETH_TOKEN_ADDRESS=0x01E85faB199F183FA4821ebBB184a4Dfc5dd459a

ERC827abi_FILE = ERC827.abi.json
Exchange_FILE = Exchange.abi.json
MyERC827Token_FILE=MyERC827Token.abi.json


GET_RECEIPT_INTERVAL_IN_MILLISECONDS=3000
CLC_ADDRESS = 0x0000000000000000000000000000000000000000

b. Mongodb info

MONGO_HOST=127.0.0.1
MONGO_PORT=27017
MONGO_DATABASE=

c. Redis (ToDo)

d. Kafka (ToDo)

4. create an account

if you are using DEX on ContractLand's Terra Chain go to acounts/terra_aacount.py 

replace account = CornAccount("test1", "address", "private key") address and private key with yours, and run this python script

Likewise for Huobi and Binance

3. Under the shell folder use 

python batch_trade.py --account clc1 --batch_type buy -a 1 --amount_func uniform_distribution --amount_para {"start":10,"end":10} --price_func normal_distribution --price_para {"mu":0,"sigma":0.0001}

## TODOs:
1. major exchange api integration

2. balance manage management/ tracking system

3. real time data feeds messaging system

4. strategy templates

