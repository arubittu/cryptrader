import json
from bson import json_util
import numpy as np
import pandas as pd
import boto3
from binance.client import Client
import time
import math
from datetime import datetime
#from getData import *
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
#def lambda_handler(event, context):
    client = MongoClient("mongodb+srv://cryptobit:WDeT0OwPJYnokcOQ@bitbotusers.tqa6n.mongodb.net/bitbot-data?retryWrites=true&w=majority")
    myDB = client['bitbot-data']
    mycollection = myDB.users
    data = myDB.users.find({})
    BIT = []
    DOG = []
    for i in data:
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
    print(BIT,DOG)
    return 
        