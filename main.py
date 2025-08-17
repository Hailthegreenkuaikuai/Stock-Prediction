import Init
import Data
import Scraper
import Connector
import websocket

if __name__ == "__main__":
    for folder in Data.FOLDER_LIST:
        Init.init_folder(folder)
    for instrument in Data.INSTRUMENT:
        Init.init_file(instrument[0])
        Init.init_processed_data(instrument[0])
        Connector.make_connection(instrument)
        