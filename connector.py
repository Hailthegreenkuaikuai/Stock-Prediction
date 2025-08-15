import websocket
import rel
import json
import Data
import scraper

def on_message(ws, message):
    scraper.format(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

def create_msg(ws, m, p):
    ms = json.dumps({"m": m, "p": p})
    msg = "~m~"+ str(len(ms)) + "~m~" + ms
    ws.send(msg)

def make_connection():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://data.tradingview.com/socket.io/websocket",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
    ws.run_forever(dispatcher=rel, reconnect = 5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly

    #For each time, the session id need to be changed
    for company in Data.COMPANY:
        create_msg(ws, "chart_create_session", [company[1],""])
        create_msg(ws, "resolve_symbol", [company[1],"sds_sym_1",f'={{"adjustment":"splits","session":"regular","symbol":"{company[2]}"}}'])
        create_msg(ws, "create_series", [company[1],"sds_1","s1","sds_sym_1","1",10000,""])
    
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()  