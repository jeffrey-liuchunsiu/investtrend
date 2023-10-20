from flask import Flask, Response


server = Flask(__name__)

@server.route('/images')
def hello():
    
    # data = yf.download("SPY AAPL", period="1mo")

    # # Convert DataFrame to JSON
    # json_data = data.to_json()
    # print('json_data: ', json_data)

    return print("hihihihi")

if __name__ == "__main__":
   server.run(host='0.0.0.0')