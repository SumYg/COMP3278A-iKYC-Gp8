import yfinance as yf
import json

#symbol = stock symbol EX: "TSLA" or "0388.HK"
def stock(symbol):
    data = yf.download(symbol,period='2d',time='1m')
    price_date = data[['Close']]
    price_date_dict = price_date.to_dict(orient='list')
    price_date_list = price_date_dict.get('Close')
    previous_close = round(price_date_list[0],2)
    current_price = round(price_date_list[1],2)
    percent_change = str(round((((price_date_list[1] - price_date_list[0]) / price_date_list[0]) *100),2)) + "%"
    price_dict = {"Previous close": previous_close, "Current price": current_price, "Percent change": percent_change}
    json_object = json.dumps(price_dict, indent = 4)
    return json_object

