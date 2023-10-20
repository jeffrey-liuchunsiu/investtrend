import json
from requests_html import HTMLSession
import pandas as pd

def get_yfinance_crypto_list(number_of_crypto: int):
    session = HTMLSession()
    num_currencies = number_of_crypto
    resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
    tables = pd.read_html(resp.html.raw_html)
    df = tables[0].copy()
    symbols_yf_list = df.Symbol.tolist()[0:]
    Name_yf_list = df.Name.tolist()[0:]
    return symbols_yf_list, Name_yf_list

def lambda_handler(event, context):
    number_of_crypto = event['number_of_crypto']
    symbols, names = get_yfinance_crypto_list(number_of_crypto)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "symbols": symbols[0],
            "names": names[0]
        })
    }