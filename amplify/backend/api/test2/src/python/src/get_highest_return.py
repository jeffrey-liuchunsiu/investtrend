from decimal import Decimal
import os
from dotenv import load_dotenv
import boto3
from flask_cors import CORS
from flask import Flask, request, jsonify
from uuid import uuid4
from datetime import datetime, timedelta


import pandas as pd
import numpy as np
import yfinance as yf
import math
import datetime as dt
import matt_supertrend as mst

# Load environment variables from .env file
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

dynamodb = boto3.resource('dynamodb', 
                          aws_access_key_id=aws_access_key_id, 
                          aws_secret_access_key=aws_secret_access_key, 
                          region_name=region_name)

table = dynamodb.Table('run5yearshighestreturn-dev')

app = Flask(__name__)
CORS(app)



def perform_backtest(symbol_list_length=10, investment=10000000, commission=5, start_date=None, end_date=None, interval='1h', print_result=True, print_detail=True):
    
    # if no start_date or end_date is provided, use default values
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=1*365)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    strategy = mst.Supertrend
    backtest = mst.backtest_supertrend

    symbols, names = mst.get_yfinance_crypto_list(symbol_list_length)
    print('symbols: ', symbols)

    results = []

    for symbol in symbols:
        fy_df = mst.get_yf_df(symbol, start_date, end_date, interval, threads=True)
        print('fy_df: ', fy_df)

        print(symbol)
        atr_period, multiplier, ROI = mst.find_optimal_parameter(fy_df, strategy, backtest, investment, commission, None, None)
    #     print(f'Best parameter set: ATR Period={atr_period}, Multiplier={multiplier}, ROI={ROI}%')
    #     best_df = mst.get_yf_df_with_best_parameters(symbol, start_date, end_date, atr_period, multiplier)
    #     mst.backtest_supertrend(best_df, investment, commission, True, False)
    #     print(" ")

    #     results.append({
    #         "symbol": symbol,
    #         "ROI": ROI,
    #         "start_date": start_date,
    #         "end_date": end_date,
    #     })
        
        # for result in results:
        #     print(result)
            # table.put_item(
            #     Item={
            #         'id': str(uuid4()),  # Generate a unique id
            #         'symbol': result['symbol'],
            #         'product_category': 'Cryptocurrency',
            #         'roi': Decimal(str(result['ROI']/100)),
            #         "start_date": start_date,
            #         "end_date": end_date,
            #         'strategy_category': 'Supertrend',
            #         'created_at': str(dt.datetime.now()),  # DynamoDB doesn't support datetime, so convert it to string
            #         'updated_at': str(dt.datetime.now()),
            #     }
            # )
            

perform_backtest()