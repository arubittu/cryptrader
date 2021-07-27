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

#----- configure and initialize mongodb -----

#CONNECTION_STRING =



#-------- api keys and for binance-------------

api_key = 'Yle1i6iRKbbvx2YMsIjczwHIV3tthRAO3X3MLNe5wbE24f4mTQr26gY8M7DD8wWY'
secret_key = '4JLW7Tkj3xe2k6MOeqluwITVKAFlEbTlvnRQyRtss5RPxF0V5ylGtyhCRHmkknWi'

# wrapper for time syncing

#---------
#lambda_handler is defined as the function which shall run after receiving an event from event bus, can be changed below in runtime se
def lambda_handler(event, context):
    #connect to test api to get price
    client=Binance(sync=True)
    #get price and time
    current_price=client.client.get_symbol_ticker(symbol="BTCUSDT") 
    srv_time=client.client.get_server_time()
    cur_time=time.time()
    timestamp=datetime.fromtimestamp(int(srv_time['serverTime']/1000))
    
    # connect to mongodb 
    client = MongoClient("mongodb+srv://testuser:testuser@test.zvbl0.mongodb.net/test?retryWrites=true&w=majority")
    myDB = client['pricedb']
    mycollection = myDB.price
    
    # insert document/item in db
    item_to_insert={'price':current_price['price'],
                    'action':-1,
                    'timestamp':str(timestamp)
                }
                
    myDB.price.insert_one(item_to_insert)
    
    #data = myDB.price.find({})
    #for i in data:
        #print(i)
        
    client.close()
    return 
    