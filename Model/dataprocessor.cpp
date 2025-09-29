#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <limits>
#include <math.h>
#include <direct.h>

using namespace std;

/*
Data Normalization, use z-score normalization
Change working directory to the project root folder
When you add new instruments, add the csv file to the stockList vector in main function
*/

struct fileRecord
{
    public:
        fileRecord(
            long time = 0,
            double open = 0,
            double high = 0,
            double low = 0, 
            double close = 0,
            double volume = 0
        ) {
            Time = time;
            Open = open;
            High = high;
            Low = low;
            Close = close;
            Volume = volume;
        }

        void display() {
            cout << "Time: " << Time << ", Open: " << Open << ", High: " << High 
                 << ", Low: " << Low << ", Close: " << Close 
                 << ", Volume: " << Volume << endl;
        }

        long Time = 0;
        double Open = 0;
        double High = 0;
        double Low = 0;
        double Close = 0;   
        double Volume = 0;
};


class dataprocessor{
    private:
        vector<fileRecord> Data;
        vector<fileRecord> normalizedData;
        vector<double> Open_Array;
        vector<double> High_Array;
        vector<double> Low_Array;
        vector<double> Close_Array;
        vector<double> Volume_Array;
    public:
        int readData(string filename){
            ifstream file;
            
            file.open("./data/" + filename, ios::in);
            if (!file) {
                std::cerr << "Unable to open file!" << std::endl;
                return 1;
            }

            string line = "";
            getline(file, line);
            while(getline(file, line)){
                long int Time = 0;
                double Open = 0, High = 0, Low = 0, Close = 0, Volume = 0;
                string dumpStuff = "";
                string tempString = "";

                stringstream inputString(line);

                getline(inputString, dumpStuff, ','); // Skip the Index
                dumpStuff = ""; 

                getline(inputString, dumpStuff, ','); //  Time
                Time = stof(dumpStuff.c_str());

                getline(inputString, tempString, ','); // Open
                Open = stof(tempString.c_str());
                Open_Array.push_back(Open);
                tempString = "";

                getline(inputString, tempString, ','); // High
                High = stof(tempString.c_str());
                High_Array.push_back(High);
                tempString = "";
                
                getline(inputString, tempString, ','); // Low
                Low = stof(tempString.c_str());
                Low_Array.push_back(Low);
                tempString = "";

                getline(inputString, tempString, ','); // Close
                Close = stof(tempString.c_str());
                Close_Array.push_back(Close);
                tempString = "";

                getline(inputString, tempString, ','); // Volume
                Volume = stof(tempString.c_str());
                Volume_Array.push_back(Volume);
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

        double getMean(vector<double> Data){
            double mean = 0, sum = 0, count = 0;
            for(auto data : Data){
                sum += data;
                count++;
            }
            mean = sum / count;
            return mean;
        }

        double getStandardDeviation(vector<double> Data, double mean){
            double variance = 0, sum = 0, count = 0;
            for(auto data : Data){
                sum += (data - mean) * (data - mean);
                count++;
            }
            sum /= count;
            variance = sqrt(sum);
            return variance;
        }

        void standardize(){
            double meanOpen = getMean(Open_Array);
            double stdDevOpen = getStandardDeviation(Open_Array, meanOpen);
            double meanHigh = getMean(High_Array);
            double stdDevHigh = getStandardDeviation(High_Array, meanHigh);
            double meanLow = getMean(Low_Array);
            double stdDevLow = getStandardDeviation(Low_Array, meanLow);
            double meanClose = getMean(Close_Array);
            double stdDevClose = getStandardDeviation(Close_Array, meanClose);
            double meanVolume = getMean(Volume_Array);
            double stdDevVolume = getStandardDeviation(Volume_Array, meanVolume);
            for(auto data : Data){
                double standardizedOpen = (data.Open - meanOpen) / stdDevOpen;
                double standardizedHigh = (data.High - meanHigh) / stdDevHigh;
                double standardizedLow = (data.Low - meanLow) / stdDevLow;
                double standardizedClose = (data.Close - meanClose) / stdDevClose;
                double standardizedVolume = (data.Volume - meanVolume) / stdDevVolume;
                fileRecord record(
                    data.Time,
                    standardizedOpen,
                    standardizedHigh,
                    standardizedLow,
                    standardizedClose,
                    standardizedVolume
                );
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
    chdir("E:/code/Stock-Prediction");
    vector<std::string> stockList = {
        "gold.csv",
        "nvda.csv",
        "msft.csv",
        "tsla.csv",
        "googl.csv",
        "es1.csv",
    };
    for(int i = 0; i < stockList.size(); i++){
        dataprocessor dp;
        cout << "Processing: " << stockList[i] << endl;
        dp.readData(stockList[i]);
        dp.standardize();
        dp.exportFile("./norm_data/norm_" + stockList[i]);
    }
    return 0;
}


