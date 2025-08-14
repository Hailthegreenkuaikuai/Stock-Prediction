import websocket
import rel
import json
import pandas as pd
import csv
import Data
#TODO Fix one stock write to all csv
def on_message(ws, message):
    format(message)

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

def format(data):
    start = data.find('"s":[')
    end = data.find(',"ns":')
    pretty = json.loads(data[start + 4 : end])
    
    formatted_data = []

    for item in pretty:
        if item["v"][0] not in Data.PROCESSED_DATA:
            Data.PROCESSED_DATA.add(item["v"][0])
            formatted_data.append(item["v"])
    print(pd.DataFrame(formatted_data))
    
    append_to_csv(formatted_data, Data.data_path + company[0])

def read_last_line(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as file: 
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip().split(",")
    return last_line

def append_to_csv(data, filename) : 
    write_header(filename)
    lastrow = read_last_line(filename)
    with open(filename, 'a', newline = '') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = Data.FIELDNAMES)
        for i, item in enumerate(data):
            if(lastrow):
                if(float(lastrow[1]) < float(item[0])):
                    row = {
                        'Index': i,
                        'Time': item[0],
                        'Open': item[1],
                        'High': item[2],
                        'Low': item[3],
                        'Close': item[4],
                        'Volume': item[5]
                    }
                    writer.writerow(row)
            else:
                row = {
                        'Index': i,
                        'Time': item[0],
                        'Open': item[1],
                        'High': item[2],
                        'Low': item[3],
                        'Close': item[4],
                        'Volume': item[5]
                    }
                writer.writerow(row)

def write_header(filename):
    with open(filename, 'a', newline = '') as csvfile :
        writer = csv.DictWriter(csvfile, fieldnames = Data.FIELDNAMES)
        csvfile.seek(0, 2)
        if(csvfile.tell() == 0):
            writer.writeheader()

if __name__ == "__main__":

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
