from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)


@app.route('/convert_currency', methods=['GET'])
def convert_currency():
    amount = request.args.get('amount', type=float)
    from_currency = request.args.get('from_currency', type=str)
    to_currency = request.args.get('to_currency', type=str)

    if amount is None or from_currency is None or to_currency is None:
        return jsonify({'error': 'Missing parameters. Please provide amount, from_currency, and to_currency.'}), 400

    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_currency}&To={to_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        result = soup.find(class_="result__BigRate-sc-1bsijpp-1 dPdXSB").text.strip()
        return jsonify({'result': result})
    else:
        return jsonify({'error': 'Failed to fetch data.'}), 500



if __name__ == '__main__':
    app.run()
