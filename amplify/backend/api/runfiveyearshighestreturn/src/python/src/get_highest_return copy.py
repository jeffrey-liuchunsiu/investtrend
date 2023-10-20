from decimal import Decimal
import os
from dotenv import load_dotenv
import boto3
from flask_cors import CORS
from flask import Flask, request, jsonify
from uuid import uuid4
from datetime import datetime, timedelta

import matt_supertrend as mst

# # Load environment variables from .env file
# load_dotenv()

# aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
# aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
# region_name = os.getenv('AWS_REGION')

# dynamodb = boto3.resource('dynamodb', 
#                           aws_access_key_id=aws_access_key_id, 
#                           aws_secret_access_key=aws_secret_access_key, 
#                           region_name=region_name)

# table = dynamodb.Table('run5yearshighestreturn-dev')

# app = Flask(__name__)
# CORS(app)



symbol_list_length = 10 #(get Top crypto in yfiance)
investment = 10000000
strategy = mst.Supertrend #(Put a strategy function in here)
backtest = mst.backtest_supertrend #(Put a backtest function in here)
commission = 5
start_date = '2023-01-01'
end_date = '2023-05-09'
interval = '1h'#(default is '1hr')
print_result = True
print_detail = True
#threads=True (default is True)
# Enter number of crypto in the list
symbols = mst.get_yfinance_crypto_list(symbol_list_length)

for symbol in symbols:
    fy_df = mst.get_yf_df(symbol, start_date, end_date, interval)

    print(symbol)
    atr_period,multiplier,ROI = mst.find_optimal_parameter(fy_df, strategy, backtest, investment,commission,None, None)
    print(f'Best parameter set: ATR Period={atr_period}, Multiplier={multiplier}, ROI={ROI}%')
    best_df = mst.get_yf_df_with_best_parameters(symbol, start_date, end_date, atr_period,multiplier)
    mst.backtest_supertrend(best_df,investment,commission,True,False)
    print(" ")