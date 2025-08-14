# This file contains various data configurations used in the project.
#  `Data.py`


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
A list of companies to scrape:

1. **[0]**: CSV file
2. **[1]**: Session identifier
3. **[2]**: Symbol identifier

For [1] and [2], check the websocket and find `"resolve_symbol"`.
```python
COMPANY = [
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
Last Update: 2025-08-14