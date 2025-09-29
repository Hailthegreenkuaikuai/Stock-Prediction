import websocket
import json
import pandas as pd
import csv
import Data
import rel
import threading
import os 
os.chdir(Data.PATH)
#Format data 
def format(data, instrument, ws):
    start = data.find('"s":[')
    end = data.find(',"ns":')
    pretty = json.loads(data[start + 4 : end])

    filename = "./data/" + instrument[0]

    formatted_data = []

    for item in pretty:
        if item["v"][0] not in Data.PROCESSED_DATA:
            Data.PROCESSED_DATA.add(item["v"][0])
            formatted_data.append(item["v"])
    print(pd.DataFrame(formatted_data))
    
    append_to_csv(formatted_data, filename, ws)

    return 

def read_last_line(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as file: 
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip().split(",")
    return last_line

def append_to_csv(data, filename, ws) : 
    write_header(filename)
    lastrow = read_last_line(filename)
    with open(filename, 'a', newline = '') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = Data.FIELDNAMES)
        for i, item in enumerate(data):
            if(lastrow and lastrow[1] != 'Time'): #Make sure the file have data and not the fieldnames
                if(float(lastrow[1]) < float(item[0])): #If the time of the new data is smaller than the last data, skip it 
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
    return
    
#Function for writing header for csv file 
def write_header(filename):
    with open(filename, 'a', newline = '') as csvfile :
        writer = csv.DictWriter(csvfile, fieldnames = Data.FIELDNAMES)
        csvfile.seek(0, 2)
        if(csvfile.tell() == 0):
            writer.writeheader()
