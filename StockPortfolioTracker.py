# Josh Bennett
# COMP112-02
# Professor Thayer
# Final Project

'''
For my project, I made a "Stock Tracker Application" that tracks the current
value of a selected stock, while providing graphical images to support it. In
addition, the user can create a diverse portfolio that can accumulate as many
stocks as they want, which will then give the user the total value of their
portfolio.

'''

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np




def stock_checker(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        if 'previousClose' in info and info['previousClose'] is not None:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False




def stock_data(symbol):
    symbol = symbol.upper()
    if not stock_checker(symbol):
        print(f"{symbol} is not a real stock. Try again.")
        return

    try:
        stock = yf.Ticker(symbol)
        hist_data = stock.history(period="1y")
        if hist_data.empty:
            print("No data found for this stock.")
            return

        plt.plot(hist_data.index, hist_data['Close'])
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.title(f'Stock Price Trend for {symbol} - Last Year')

        info = stock.info
        current_price = info['previousClose']
        last_date = hist_data.index[-1]
        plt.annotate(f'Current Price: ${current_price}',
                     xy=(last_date, current_price),
                     xytext=(last_date, current_price),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     horizontalalignment='right')

        plt.show()

        data = {'Current Price': current_price}
        return data
    except Exception as e:
        print(f"Error: {e}")




def stock_value(symbol, shares):
    data = stock_data(symbol)
    if data:
        return data['Current Price'] * shares
    return 0




def add_shares(portfolio, symbol, shares):
    if stock_checker(symbol):
        if symbol in portfolio:
            portfolio[symbol] += shares
        else:
            portfolio[symbol] = shares
    else:
        print(f"{symbol} is not a real stock.")

    if symbol in portfolio:
        portfolio[symbol] += shares
    else:
        portfolio[symbol] = shares




def portfolio_summary(portfolio):
    total_value = 0
    stock_values = []
    for symbol, shares in list(portfolio.items()):
        symbol = symbol.upper()  
        data = stock_data(symbol)
        if not data:
            print(f"{symbol} is not a real stock. Try again.")
            portfolio.pop(symbol)  
            continue

        current_price = data['Current Price']
        value = current_price * shares
        stock_values.append({'Symbol': symbol, 'Shares': shares, 'Value': value, 'Price': current_price})
        total_value += value


    symbols = [stock['Symbol'] for stock in stock_values]
    values = [stock['Value'] for stock in stock_values]
    prices = [stock['Price'] for stock in stock_values]
    colors = plt.cm.viridis(np.linspace(0, 1, len(stock_values)))  
    bars = plt.bar(symbols, values, color=colors)


    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'${value:.2f}', 
                 ha='center', va='bottom', color='black')

    for bar, price in zip(bars, prices):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 0.5, f'Current Price: ${price:.2f}', 
                 ha='center', va='center', color='blue', rotation=90)

    plt.text(len(symbols)-1, max(values), f'Total Value: ${total_value:.2f}', 
             ha='right', va='top', fontsize=10, color='green')

    plt.xlabel('Stock Symbols')
    plt.ylabel('Value in $')
    plt.title('Portfolio')
    plt.xticks(rotation=45)  
    plt.show()





import csv

def export_portfolio_to_csv(portfolio):
    with open('portfolio_summary.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Stock Symbol', 'Shares Owned', 'Current Price', 'Total Value'])

        for symbol, shares in portfolio.items():
            data = stock_data(symbol)
            if data:
                price = data['Current Price']
                total_value = price * shares
                writer.writerow([symbol.upper(), shares, f"${price:.2f}", f"${total_value:.2f}"])
    print("Portfolio exported to portfolio_summary.csv")


def main():
    portfolio = {}

    while True:
        print("\nStock Analysis App")
        print("1. Get Current Stock Data")
        print("2. View Portfolio")
        print("3. Add stock to portfolio")
        print("4. Export Portfolio to CSV")
        print("5. Exit Application")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ")
            data = stock_data(symbol)
            if data:
                print(data)


        elif choice == '2':
            portfolio_summary(portfolio)


        elif choice == '3':
            while True:
                symbol = input("Enter stock symbol: ")
                if stock_checker(symbol):
                    try:
                        shares = int(input("Enter number of shares: "))
                        add_shares(portfolio, symbol, shares)
                        break
                    except ValueError:
                        print("Invalid number of shares.")
                else:
                    print("Invalid stock choice. Try again.")


        
        elif choice == '4':
            export_portfolio_to_csv(portfolio)

        elif choice == '5':
            print("Exiting the application.")
            break


        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
