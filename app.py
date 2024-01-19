from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import pandas_market_calendars as mcal
import pytz

app = Flask(__name__)
today = datetime.now(pytz.timezone('US/Eastern')).date()

def get_last_trading_day():
    nyse = mcal.get_calendar("XNYS")    
    last_trading_day = nyse.valid_days(start_date=today - timedelta(days=10), end_date=today)[-2]
    return last_trading_day

def get_last_price_for_symbol(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        last_trading_day = get_last_trading_day()
        
        # Fetch historical data for the previous trading day
        historical_data_last_day = stock_data.history(start=last_trading_day, end=today)
        last_day_price = historical_data_last_day['Close'].iloc[-1]

        # Fetch historical data for the current day
        historical_data_current_day = stock_data.history(period="1d")
        last_price = historical_data_current_day['Close'].iloc[-1]
        price_change = last_price - last_day_price
        
        return {'symbol': symbol, 'last_price': last_price, 'last_day_price': last_day_price, 'price_change': price_change}
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