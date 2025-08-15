import websocket
import rel
import json
import pandas as pd
import csv
import Data
#TODO Fix one stock write to all csv

class Scraper: 
    def format(self, data):
        start = data.find('"s":[')
        end = data.find(',"ns":')
        pretty = json.loads(data[start + 4 : end])
        
        formatted_data = []

        for item in pretty:
            if item["v"][0] not in Data.PROCESSED_DATA:
                Data.PROCESSED_DATA.add(item["v"][0])
                formatted_data.append(item["v"])
        print(pd.DataFrame(formatted_data))
        
        #append_to_csv(formatted_data, Data.DATA_PATH + company[0])

    def read_last_line(self, path):
        with open(path, "r", encoding="utf-8", errors="ignore") as file: 
            lines = file.readlines()
            if not lines:
                return None
            last_line = lines[-1].strip().split(",")
        return last_line

    def append_to_csv(self, data, filename) : 
        self.write_header(filename)
        lastrow = self.read_last_line(filename)
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
