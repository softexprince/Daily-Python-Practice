ALGO FOR 5 EMA STRATEGY
#GET DATA FUNCTION 
def getdata():
    cdata = {
            "symbol":"NSE:NIFTYBANK-INDEX",
            "resolution":"5",
            "date_format":"1",
            "range_from":"2023-10-03",
            "range_to":"2023-10-04",
            "cont_flag":"0"
            }
    response = fyers.history(data=cdata)
    data = pd.DataFrame.from_dict(response['candles'])
    cols = ['datetime', 'open', 'high','low','close', 'volume']
    data.columns = cols
    data['datetime'] = pd.to_datetime(data['datetime'], unit="s")
    data['datetime'] = data['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    data['datetime'] = data['datetime'].dt.tz_localize(None)
    data = data.set_index('datetime')
    data["ema"] = data["close"].ewm(span = 5 , min_periods=5).mean()
    global emadata
    emadata = data
# on message function 
def onmessage(message):
    #symb = message['symbol']
    #ltp = message['ltp']
    #print(message)
    t = time.localtime()
    cmin = time.strftime("%M", t)
    csec = time.strftime("%S", t)
    global pos, stoploss, exit, strike, target, flag
    if (int(cmin) % 5 == 0 and int(csec) < 3):
        print("5 ema data updated")
        getdata()
        time.sleep(1)
        if (pos == 0):
            flag = 0
    symb = "NSE:NIFTYBANK-INDEX"
    ema = emadata['ema'].iloc[-2]
    l =  emadata['low'].iloc[-2]
    print(f"{message} | low {l} |ema {ema} | ")
    if (emadata['close'].iloc[-2] > emadata['ema'].iloc[-2] 
        and emadata['high'].iloc[-2] > emadata['ema'].iloc[-2]
        and emadata['open'].iloc[-2] > emadata['ema'].iloc[-2]
        and emadata['low'].iloc[-2] > emadata['ema'].iloc[-2]
        and message['ltp'] < emadata['low'].iloc[-2]):
        ltp = message['ltp']
        sp = int(round(ltp,-2))
        if (pos==0 and flag==0):
            strike = "NSE:BANKNIFTY23O04" + str(sp) + "PE"
            data = {
                "symbol": str(strike),
                "qty":15,
                "type":2,
                "side":1,
                "productType":"MARGIN",
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
                }
            print(f"entry {strike}")
            response = fyers.place_order(data=data)
            pos = flag = 1
            entry = message['ltp']
            stoploss = emadata['high'].iloc[-2]
            target = message['ltp'] - ((emadata['high'].iloc[-2] - emadata['low'].iloc[-2])*3)
            print(response)
    if (pos==1 and message['ltp'] >= stoploss):
            data = {
            "symbol": str(strike),
            "qty":15,
            "type":2,
            "side":-1,
            "productType":"MARGIN",
            "limitPrice":0,
            "stopPrice":0,
            "validity":"DAY",
            "disclosedQty":0,
            "offlineOrder":False,
            }
            print("stop loss")
            response = fyers.place_order(data=data)
            print(response)
            pos = 0
            stoploss = 0
            entry = 0
            target = 0
            time.sleep(1)
            data_type = "SymbolUpdate"
            symbols_to_unsubscribe = ['NSE:NIFTYBANK-INDEX']
            fyersdata.unsubscribe(symbols=symbols_to_unsubscribe, data_type=data_type)
    if (pos==1 and message['ltp'] <= target):
            data = {
            "symbol": str(strike),
            "qty":15,
            "type":2,
            "side":-1,
            "productType":"MARGIN",
            "limitPrice":0,
            "stopPrice":0,
            "validity":"DAY",
            "disclosedQty":0,
            "offlineOrder":False,
            }
            print("traget ")
            response = fyers.place_order(data=data)
            print(response)
            pos = 0
            stoploss = 0
            entry = 0
            target = 0
            time.sleep(1)
            data_type = "SymbolUpdate"
            symbols_to_unsubscribe = ['NSE:NIFTYBANK-INDEX']
            fyersdata.unsubscribe(symbols=symbols_to_unsubscribe, data_type=data_type)
            print(f"symbol {symb} and ltp {ltp} | low {l} |ema {ema} | ")
            print(f"success {message}")
def onerror(message):
    print("Error:", message)
def onclose(message):
    print("Connection closed:", message)
def onopen():
    data_type = "SymbolUpdate"
    symbols = ['NSE:NIFTYBANK-INDEX']
    fyersdata.subscribe(symbols=symbols, data_type=data_type)
    fyersdata.keep_running()
# Replace the sample access token with your actual access token obtained from Fyers
access_token = client_id + ":" + tk
# Create a FyersDataSocket instance with the provided parameters
fyersdata = data_ws.FyersDataSocket(
    access_token=access_token,       # Access token in the format "appid:accesstoken"
    log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
    litemode=True,                  # Lite mode disabled. Set to True if you want a lite response.
    write_to_file=False,              # Save response in a log file instead of printing it.
    reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
    on_connect=onopen,               # Callback function to subscribe to data upon connection.
    on_close=onclose,                # Callback function to handle WebSocket connection close events.
    on_error=onerror,                # Callback function to handle WebSocket errors.
    on_message=onmessage             # Callback function to handle incoming messages from the WebSocket.
)
# Establish a connection to the Fyers WebSocket
fyersdata.connect()
