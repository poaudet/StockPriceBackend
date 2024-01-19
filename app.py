from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import pandas_market_calendars as mcal

app = Flask(__name__)

def get_last_trading_day():
    nyse = mcal.get_calendar("XNYS")
    today = datetime.today().date()
    last_trading_day = nyse.valid_days(start_date=today - timedelta(days=10), end_date=today)[-2]
    return last_trading_day

def get_last_price_for_symbol(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        last_trading_day = get_last_trading_day()
        historical_data = stock_data.history(start=last_trading_day, end=datetime.today().date())
        last_day_price = historical_data['Close'].iloc[-1]
        last_price = stock_data.history(period="1d")['Close'].iloc[-1]
        print(last_price, last_day_price)
        price_change = last_price - last_day_price
        return {'symbol': symbol, 'last_price': last_price, 'price_change': price_change}
    except Exception as e:
        return {'symbol': symbol, 'error': f'Error fetching data: {str(e)}'}

@app.route('/get_last_prices', methods=['GET'])
def get_last_prices():
    symbols_param = request.args.get('symbols')

    if not symbols_param:
        return jsonify({'error': 'Stock symbols are required'}), 400

    symbols = symbols_param.split(';')
    results = [get_last_price_for_symbol(symbol) for symbol in symbols]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)