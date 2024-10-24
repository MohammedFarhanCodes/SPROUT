from django.shortcuts import render
from .utils import fetch_stock_list
from .models import Stock
import yfinance as yf


def stock_list(request):
    stocks = Stock.objects.all()

    context = {
        'stock_list': stocks
    }
    return render(request, 'stock/stock_list.html', context)


# Fetch historical data for a stock (e.g., 'AAPL')
def get_stock_history(symbol, period="1mo"):
    stock = yf.Ticker(symbol)
    stock_history = stock.history(period=period)

    return stock_history


def stock_chart(request, symbol):
    # Fetch historical data for the stock
    stock = yf.Ticker(symbol)
    stock_history = stock.history(period="1mo")  # Last 1 month of data

    # Prepare data for the chart
    dates = stock_history.index.strftime('%Y-%m-%d').tolist()
    prices = stock_history['Close'].tolist()

    context = {
        'symbol': symbol,
        'dates': dates,
        'prices': prices
    }

    return render(request, 'stock/stock chart.html', context)


def user_stocks(request):
    return render(request, 'stock/user_stocks.html')
