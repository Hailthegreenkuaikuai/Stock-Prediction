# Data.py Configuration

This file contains various data configurations used in the project.

---


## Folder Paths

- **Current Working Directory:**  
    ```python
    PATH = "E:\code\Stock-Prediction"
    ```

- **Original Data Folder:**  
    ```python
    DATA_PATH = "./data"
    ```
- **Normalized Data Folder:** 
    ```python
    NORM_DATA_PATH = "./norm_data"
    ```

## Company List
A list of instrument to scrape:

1. **[0]**: CSV file
2. **[1]**: Session identifier
3. **[2]**: Symbol identifier

For [1] and [2], check the websocket and find `"resolve_symbol"`.
```python
INSTRUMENT = [
    ["tsla.csv", "cs_ABCDEFGHIJKLM", "NASDAQ:TSLA"],
    ["tsla.csv", "cs_ABCDEFGHIJKLM", "NASDAQ:TSLA"],
    ["tsla.csv", "cs_ABCDEFGHIJKLM", "NASDAQ:TSLA"],
]
```

## CSV Field Names
The field names used in the CSV files:
```python
FIELDNAMES = ['Index', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
```
_Last Update: **2025-08-17**_


## Folder Paths

- **Original Data Folder:**  
    ```python
    DATA_PATH = "./data"
    ```
- **Normalized Data Folder:** 
    ```python
    NORM_DATA_PATH = "./norm_data"
    ```

## Company List
A list of instrument to scrape:

1. **[0]**: CSV file
2. **[1]**: Session identifier
3. **[2]**: Symbol identifier

For [1] and [2], check the websocket and find `"resolve_symbol"`.
```python
INSTRUMENT = [
    ["tsla.csv", "cs_ABCDEFGHIJKLM", "NASDAQ:TSLA"],
    ["tsla.csv", "cs_ABCDEFGHIJKLM", "NASDAQ:TSLA"],
    ["tsla.csv", "cs_ABCDEFGHIJKLM", "NASDAQ:TSLA"],
]
```

## CSV Field Names
The field names used in the CSV files:
```python
FIELDNAMES = ['Index', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
```
_Last Update: **2025-09-07**_