import json
from bson import json_util
import numpy as np
import pandas as pd
import boto3
from binance.client import Client
import time
import math
from datetime import datetime
from getData import *
import pymongo
from pymongo import MongoClient
from main import *
from strategy import *
from bson.objectid import ObjectId
#----- configure and initialize mongodb -----



#-------- api keys and for binance-------------

#api_key = 'Yle1i6iRKbbvx2YMsIjczwHIV3tthRAO3X3MLNe5wbE24f4mTQr26gY8M7DD8wWY'
#secret_key = '4JLW7Tkj3xe2k6MOeqluwITVKAFlEbTlvnRQyRtss5RPxF0V5ylGtyhCRHmkknWi'

# wrapper for time syncing

#---------
#lambda_handler is defined as the function which shall run after receiving an event from event bus, can be changed below in runtime se
def lambda_handler(event, context):
    # code for getting all api keys of users who are running live strategies
    client_user = MongoClient("mongodb+srv://cryptobit:WDeT0OwPJYnokcOQ@bitbotusers.tqa6n.mongodb.net/bitbot-data?retryWrites=true&w=majority")
    myDB_user = client_user['bitbot-data']
    mycollection_user = myDB_user.users
    data_user = myDB_user.users.find({})
    BIT = []
    DOG = []
    for i in data_user:
        if(i.get('broker')):
            if(i['broker']['apiKey']!= ''):
                var = {
                    'apiKey' : i['broker']['apiKey'] ,
                    'secretKey':i['broker']['secretKey'],
                    'budget':i['cryptoInfo']['budget']
                }
                if(i['cryptoInfo']['cryptoCode'] == 'BIT'):
                    BIT.append(var)
                else:
                    DOG.append(var)
    print(BIT,DOG)# bitcoin and dogecoin live strategy user's apikeys 
    #client_user.close()
    
    #------------- time to get the data from mongodb price database in proper format so strategy and main.py can run
    
    client_price = MongoClient("mongodb+srv://testuser:testuser@test.zvbl0.mongodb.net/test?retryWrites=true&w=majority")
    myDB_price = client_price['pricedb']
    mycollection_price = myDB_price.price
    data_price = myDB_price.price.find({}).skip(myDB_price.price.estimated_document_count()-20)
    price_list=[]
    for i in data_price:
        price_list.append(i)
        
    # create pandas df    
    pandas_df=pd.DataFrame(price_list)
    #df.to_csv('database.csv',index=False)
    print(len(pandas_df))
    
    
    #-------------- use above data and run strategy for each live user
    for live_strategies in BIT: # doing only for bit cuurently , add doge later
        api_key=live_strategies['apiKey']
        secret_key=live_strategies['secretKey']
        binanceClient=Binance( public_key = api_key, secret_key = secret_key,sync=True)
        order=main(binanceClient,pandas_df,myDB_price) # make order
        print('BTC balance is {}'.format(binanceClient.client.get_asset_balance(asset='BTC')))
        print('USDT balance is {}'.format(binanceClient.client.get_asset_balance(asset='USDT')))
        print('order is {}'.format(order))
    client_price.close()   
    client_user.close()
    return 
        