import os
import yfinance as yf
import boto3
from datetime import datetime
from dotenv import load_dotenv
from get_crypto_list import get_yfinance_crypto_list
from boto3.dynamodb.conditions import Attr

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

dynamodb = boto3.resource('dynamodb', 
                          aws_access_key_id=aws_access_key_id, 
                          aws_secret_access_key=aws_secret_access_key, 
                          region_name=region_name)

table = dynamodb.Table('investment_products-dev')

def store_cryptos_data(symbols, names):
    for i in range(len(symbols)):
        symbol = symbols[i]
        name = names[i]

        item = {
            'category': 'Cryptocurrency',
            'name': name,
            'symbol': symbol,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        try:
            # Insert into the table
            table.put_item(
                Item=item,
                ConditionExpression=Attr('symbol').not_exists()
            )
            
            print(f"Data stored for {symbol} - {name}")
            
        except Exception as e:
            print(f"Error storing data for {symbol} - {name}: {e}")
    
if __name__ == "__main__":

    symbols, names = get_yfinance_crypto_list(250)
    store_cryptos_data(symbols, names)