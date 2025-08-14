import os 
import Data
#TODO Init program 
def init_file(folder, filename):
    if(not os.path.exists(folder + filename)):
        open(folder + filename, 'x')

def init_processed_data(filename, processed_data) :
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if line and line not in processed_data:
                processed_data.add(line[0])

def init_scraper(filename):
    for company in Data.COMPANY:
        init_file(Data.data_path, filename)
        init_processed_data(Data.data_path + filename, Data.PROCESSED_DATA)