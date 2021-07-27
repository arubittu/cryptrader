# running strategies and sending broker signal every time new price is appended to db
#----------
import os
from binance.client import Client
import numpy as np
import pandas as pd
from strategy import *
from datetime import datetime
import time
import math
from bson.objectid import ObjectId
#----------

def main(client,pandas_df,myDB_price):

    action=strategy1(pandas_df)
    order=None

    if action==0:
        buy_order = client.client.create_test_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=0.5)
        order=buy_order
    elif action ==1:
        sell_order = client.client.create_test_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity=0.5)
        order=sell_order

    print(action)

    #btc_df=pd.read_csv('database.csv')
    #btc_df.at[len(btc_df)-1,'action']=action
    #btc_df.to_csv('database.csv',index=False)
    

    #item_to_change=[i for i in myDB_price.price.find({"_id": ObjectId(str(pandas_df['_id'][-1:].item()))})]
    
    # code for updating the mongodb action column
    myDB_price.price.update_one(
        {"_id":ObjectId(str(pandas_df['_id'][-1:].item()))},
        {
                "$set":{
                        "action":action
                        }
                }
        )
    return order
    

if __name__=='__main__':
    pass
