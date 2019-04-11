#About the project

This is a open source project, which is designed to serve for the simple market making purposes as well as the traditional simple quantitative trading requirements for cryptocurrencies

This system will for now include some basic building blocks of a trading system, such as alpha model, risk model, might include transaction cost model and optimization model. It depends on the time. 

##The current structure of the project:

accounts: multi-exchange account management
exchanges: exchange apis
files: abis for contractland's terra chain
handlers: independent tasks such as auto placing buy orders, sell orders and so on 
utils: the helper functions and classes of the system
system.ini: used to store the related properties
