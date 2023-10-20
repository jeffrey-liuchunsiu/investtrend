import os
from dotenv import load_dotenv
import boto3
from flask_cors import CORS
from flask import Flask, request, jsonify
from uuid import uuid4

from matt_supertrend import Supertrend, backtest_supertrend, find_optimal_parameter, get_yf_df



# Load environment variables from .env file
load_dotenv()

BASE_ROUTE = "/highestreturn"
TABLE = 'highestreturn-dev'

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name = region_name
)
client = session.client('dynamodb')

app = Flask(__name__)
CORS(app)

@app.route(BASE_ROUTE, methods=['POST'])
def highest_return():
    request_json = request.get_json()
    client.put_item(TableName=TABLE, Item={
        'roi': {
            'S': request_json.get('roi')
        },
        'id': {
            'S': str(uuid4())
        }
    })
    return jsonify(message='item test created')

@app.route('/find_best', methods=['POST'])
def find_best():
    json_data = request.get_json()
    symbol = json_data.get('symbol', 'BTC-USD')
    investment = json_data.get('investment', 10000000)
    commission = json_data.get('commission', 5)
    start_date = json_data.get('start_date', '2023-01-01')
    end_date = json_data.get('end_date', '2023-10-18')
    interval = json_data.get('interval', '1h')
    atr_period = json_data.get('atr_period', 14)
    atr_multiplier = json_data.get('atr_multiplier', None)

    strategy = Supertrend
    backtest = backtest_supertrend
    # test_df = await get_product_data(symbol, start_date, end_date)
    # print('test_df: ', test_df)
    fy_df = get_yf_df(symbol, start_date, end_date,interval=interval,threads=True)
    print('fy_df: ', fy_df)

    atr,multiplier,ROI = find_optimal_parameter(fy_df, strategy, backtest, investment,commission,atr_period,atr_multiplier)
    print('atr,multiplier,ROI : ', atr,multiplier,ROI )
    
    return jsonify({"atr": atr, "multiplier": multiplier, "ROI": ROI})

if __name__ == "__main__":
   app.run(host='0.0.0.0',port=5050 )