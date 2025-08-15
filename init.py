import os 
import Data
#TODO Init program 

class Init:
    #Function to create folder
    def init_folder(folder):
        try:
            if(not os.path.exists(folder)):
                open(folder, 'x')
        except Exception as e:
            print(f"An error occur when init folder: {e}")

    #Function to create file
    def init_file(folder, filename):
        try:
            if(not os.path.exists(folder + filename)):
                open(folder + filename, 'x')
        except Exception as e:
            print(f"An error occur when init file: {e}")

    #Function to create processed data, contain Time of history data
    #If contain in the set, do not append to the csv
    def init_processed_data(filename, processed_data) :
        try:
            #Clear processed data first, stock may not start scraping at same time
            Data.PROCESSED_DATA.clear()
            with open(filename, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    if line and line not in processed_data:
                        processed_data.add(line[0])
        except Exception as e:
            print(f"An error occur when init processed data: {e}")

    def init_scraper(self, filename):
        try:
            for company in Data.COMPANY:
                self.init_file(Data.DATA_PATH, filename)
                self.init_processed_data(Data.DATA_PATH + filename, Data.PROCESSED_DATA)
        except Exception as e:
            print(f"An error occur when init scraper: {e}")