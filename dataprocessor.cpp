#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <limits>

using namespace std;

struct fileRecord
{
    public:
        fileRecord(
            float time,
            float open,
            float high,
            float low, 
            float close,
            float volume
        ) {
            Time = time;
            Open = open;
            High = high;
            Low = low;
            Close = close;
            Volume = volume;
        }

        void display() {
            cout << "Time: " << Time << "Open: " << Open << ", High: " << High 
                 << ", Low: " << Low << ", Close: " << Close 
                 << ", Volume: " << Volume << endl;
        }

        float Time;
        float Open;
        float High;
        float Low;
        float Close;   
        float Volume;
};


class dataprocessor{
    private:
        vector<fileRecord> Data;
        float maxAll[5] = {0, 0, 0, 0, 0};
        float minAll[5] = {0, 0, 0, 0, 0};
        float max15[5] = {0, 0, 0, 0, 0};
        float min15[5]  = {0, 0, 0, 0, 0};
        vector<fileRecord> normalizedData;
    public:
        int readData(string filename){
            ifstream file;
            
            file.open(filename, ios::in);
            if (!file) {
                std::cerr << "Unable to open file!" << std::endl;
                return 1;
            }

            string line = "";
            getline(file, line);
            while(getline(file, line)){
                float Time, Open, High, Low, Close, Volume;
                string dumpStuff = "";
                string tempString = "";

                stringstream inputString(line);

                getline(inputString, dumpStuff, ','); // Skip the Index
                dumpStuff = ""; 

                getline(inputString, dumpStuff, ','); //  Time
                Time = stof(dumpStuff.c_str());

                getline(inputString, tempString, ','); // Open
                Open = stof(tempString.c_str());
                tempString = "";

                getline(inputString, tempString, ','); // High
                High = stof(tempString.c_str());
                tempString = "";
                
                getline(inputString, tempString, ','); // Low
                Low = stof(tempString.c_str());
                tempString = "";

                getline(inputString, tempString, ','); // Close
                Close = stof(tempString.c_str());
                tempString = "";

                getline(inputString, tempString, ','); // Volume
                Volume = stof(tempString.c_str());
                tempString = "";

                fileRecord record(Time, Open, High, Low, Close, Volume);
                Data.push_back(record);
            }
            file.close();
            return 0;
        }

        void printRecord(){
            for(auto data : Data){
                data.display();
            }
        }

        void getMaxAll(){
            for(auto data : Data){
                if(data.Open > maxAll[0]) maxAll[0] = data.Open;
                if(data.High > maxAll[1]) maxAll[1] = data.High;
                if(data.Low > maxAll[2]) maxAll[2] = data.Low;
                if(data.Close > maxAll[3]) maxAll[3] = data.Close;
                if(data.Volume > maxAll[4]) maxAll[4] = data.Volume;
            }
        }

        void getMinAll(){
            for(auto data : Data){
                if(data.Open < minAll[0] || minAll[0] == 0) minAll[0] = data.Open;
                if(data.High < minAll[1] || minAll[1] == 0) minAll[1] = data.High;
                if(data.Low < minAll[2] || minAll[2] == 0) minAll[2] = data.Low;
                if(data.Close < minAll[3] || minAll[3] == 0) minAll[3] = data.Close;
                if(data.Volume < minAll[4] || minAll[4] == 0) minAll[4] = data.Volume;
            }
        }

        void getMax15(int index){
            for(int i = index; i < index + 15 && i < Data.size() - 15; i++){
                if(Data[i].Open > max15[0]) max15[0] = Data[i].Open;
                if(Data[i].High > max15[1]) max15[1] = Data[i].High;
                if(Data[i].Low > max15[2]) max15[2] = Data[i].Low;
                if(Data[i].Close > max15[3]) max15[3] = Data[i].Close;
                if(Data[i].Volume > max15[4]) max15[4] = Data[i].Volume;
            }
        }

        void getMin15(int index){
            for(int i = index; i < index + 15 && i < Data.size() - 15; i++){
                if(Data[i].Open < min15[0] || min15[0] == 0) min15[0] = Data[i].Open;
                if(Data[i].High < min15[1] || min15[1] == 0) min15[1] = Data[i].High;
                if(Data[i].Low < min15[2] || min15[2] == 0) min15[2] = Data[i].Low;
                if(Data[i].Close < min15[3] || min15[3] == 0) min15[3] = Data[i].Close;
                if(Data[i].Volume < min15[4] || min15[4] == 0) min15[4] = Data[i].Volume;
            }
        }

        float equation(float value, float minValue, float maxValue, float max15, float min15){
            float normValue = 0;
            float temp = 0;
            temp = (value - minValue) / (maxValue - minValue);
            normValue = (temp * (max15 - min15)) + min15;
            return normValue;
        }

        void normalize(){
            for(int i = 0; i < Data.size() - 15; i++){
                getMax15(i);
                getMin15(i);
                float Time = Data[i].Time; 
                float normOpen = equation(Data[i].Open, minAll[0], maxAll[0], max15[0], min15[0]);
                float normHigh = equation(Data[i].High, minAll[1], maxAll[1], max15[1], min15[1]);
                float normLow = equation(Data[i].Low, minAll[2], maxAll[2], max15[2], min15[2]);
                float normClose = equation(Data[i].Close, minAll[3], maxAll[3], max15[3], min15[3]);
                float normVolume = equation(Data[i].Volume, minAll[4], maxAll[4], max15[4], min15[4]);

                fileRecord record(Time, normOpen, normHigh, normLow, normClose, normVolume);
                
                normalizedData.push_back(record);
            }
        }

        void printNormalizedData(){
            for(int i = 0; i < normalizedData.size(); i++){
                cout << normalizedData[i].Time << ", "
                     << normalizedData[i].Open << ", "
                     << normalizedData[i].High << ", "
                     << normalizedData[i].Low << ", "
                     << normalizedData[i].Close << ", "
                     << normalizedData[i].Volume << endl;
            }
        }

        bool fileExists(const string& filename) {
            ifstream file(filename);
            return file.good();
        }

        void exportFile(string filename){
            if(fileExists(filename)){
                cout << "Exporting normalized data to: " << filename << endl;
                remove(filename.c_str());
                writeToFile(filename);
            }else{
                cout << "Creating export file: " << filename << endl;
                writeToFile(filename);
            }
        }

        void writeToFile(string filename) {
            ofstream file(filename);
            if (!file) {
                cerr << "Error opening file for writing!" << endl;
                return;
            }
            file << "Time,Open,High,Low,Close,Volume" << endl;
            for (const auto& record : normalizedData) {
                file << record.Time << ", "
                     << record.Open << ", "
                     << record.High << ", "
                     << record.Low << ", "
                     << record.Close << ", "
                     << record.Volume << endl;
            }
            file.close();
        }
};




int main() {
    vector<string> stockList = {
        "nvda.csv",
        "msft.csv",
        "tsla.csv"
    };

    for(int i = 0; i < stockList.size(); i++){
        dataprocessor dp;
        cout << "Processing: " << stockList[i] << endl;
        dp.readData(stockList[i]);
        dp.getMaxAll();
        dp.getMinAll();
        dp.normalize();
        dp.exportFile("norm_" + stockList[i]);
        cout << "Finished processing: " << stockList[i] << endl;
    }
    return 0;
}
