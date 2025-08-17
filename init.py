import os 
import Data 

#Function to create folder
def init_folder(folder):
    try:
        if(not os.path.exists(folder)):
            open(folder, 'x')
    except Exception as e:
        print(f"An error occur when init folder: {e}")

#Function to create file
def init_file(filename):
    try:
        full_path = Data.DATA_PATH + "/" + filename
        if(not os.path.exists(full_path)):
            open(full_path, 'x')
    except Exception as e:
        print(f"An error occur when init file: {e}")

#Function to create processed data, contain Time of history data
#If contain in the set, do not append to the csv
def init_processed_data(filename) :
    try:
        file_path = "./data/" + filename
        #Clear processed data first, stock may not start scraping at same time
        Data.PROCESSED_DATA.clear()
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                if line and line not in Data.PROCESSED_DATA:
                    Data.PROCESSED_DATA.add(line[0])
    except Exception as e:
        print(f"An error occur when init processed data: {e}")