from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

def get_last_price_for_symbol(symbol):
    try:
        # Fetch the stock data using the Yahoo Finance library
        stock_data = yf.Ticker(symbol)
        last_price = stock_data.history(period='1d')['Close'].iloc[-1]
        return {'symbol': symbol, 'last_price': last_price}
    except Exception as e:
        return {'symbol': symbol, 'error': f'Error fetching data: {str(e)}'}

@app.route('/get_last_prices', methods=['GET'])
def get_last_prices():
    # Get the stock symbols from the request parameters
    symbols_param = request.args.get('symbols')

    if not symbols_param:
        return jsonify({'error': 'Stock symbols are required'}), 400

    # Split symbols using semi-colon as a delimiter
    symbols = symbols_param.split(';')

    # Get last prices for each symbol
    results = [get_last_price_for_symbol(symbol) for symbol in symbols]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)