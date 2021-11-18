import yfinance as yf
import json
import sqls
import time;
#symbol = stock symbol EX: "TSLA" or "0388.HK"
def stock(symbol):
    data = yf.download(symbol,period='3d',time='1m')
    price_date = data[['Close']]
    price_date_dict = price_date.to_dict(orient='list')
    price_date_list = price_date_dict.get('Close')
    #previous_close = round(price_date_list[0],2)
    current_price = round(price_date_list[1],2)
    percent_change = str(round((((price_date_list[1] - price_date_list[0]) / price_date_list[0]) *100),2)) + "%"
    price_dict = {"stock_name": symbol, "live_price": current_price, "percentage_change": percent_change}
    json_object = json.dumps(price_dict, indent = 4)
    return json_object



symbol_list = ["0005.HK","0388.HK","0700.HK","AAPL","BTC-USD","ETH-USD","FB","TSLA"]


def stock_update():
    while (True):
        for i in symbol_list:
            json_data = json.loads(stock(i))
            print(json_data["stock_name"])
            sqls.updateStock(json_data["stock_name"],json_data["live_price"],json_data["percentage_change"])
        time.sleep(6)
