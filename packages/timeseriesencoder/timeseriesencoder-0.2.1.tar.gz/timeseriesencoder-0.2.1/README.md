A module for encoding timeseries data, with helper functions for parsing JSON and CSV files into smaller sizes for caching and transmitting through APIs.

# Installation
```
pip install timeseriesencoder
```

# Use
## JSON
To use pass any json into TimeSeriesEncoder.encode_json(data, ts_key, ts_value) where ts_key and ts_value are the timestamp key and the value key in the json.

```python
from timeseriesencoder import *
encoded = JSONEncoder.encode_json(myJson, ts_key='UTC', ts_value='Value')
```

To decode you can apply the reverse:
```python
decoded = JSONEncoder.decode_json(encoded)
```

The encoder will encode all time series it finds in the json or csv file. Each will get their own encoding that is optimal for the data sparsity and values. Sorting the data before encoding can improve compression. If you'd like the encoder to sort for you, you can include sort_values = True on the encode_json call. This will sort each time series by the timeseries key before encoding.

## CSV
```python
from timeseriesencoder import *
csv = get_csv_sample()
encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
```

To decode you can apply the reverse:
```python
decoded = CSVEncoder.decode_csv(encoded)
```

Additionally, non time series data will be encoded in CSV files as able. Static columns will be compressed, and string value columns will be replaced with encoded lookups if it saves space in the encoded file size. 

# Updates

## 0.2.0 

    - Released a csv module that allows encoding of CSV time series files, it is accessible on CSVEncoder.
    - Migrated JSON function from TimeSeriesEncoder to JSONEncoder, which extends TimeSeriesEncoder
    - Fixed a few bugs, added more tests

## 0.1.17

    - Added gzip compression as an optional output for all encoding and decoding calls
    - Added tests for gzip


# Tests
To run tests call pytests on the tests folder from the base package folder.
```
pytest ./tests/ -v -s
```

![image](https://user-images.githubusercontent.com/8877753/115096228-d00ccb00-9ee9-11eb-815a-8d837ffc66f3.png)


# Examples
Example of encoding a json file, with the inputs/outputs below.

*Note: The numpyencoder module is not required, but is used in the example to read/write the json to a file easily.*
```python
from timeseriesencoder import *
import json
from numpyencoder import NumpyEncoder

with open('sample.json', 'r') as rfile:
    data = json.load(rfile)

data['Response'][0]['ForecastWeather'] = data['Response'][0]['ForecastWeather'][:3]

with open('data.json', 'w') as rfile:
    json.dump(data, rfile, cls=NumpyEncoder)

encoded = TimeSeriesEncoder.encode_json(data, ts_key='UTC', ts_value='Value', sort_values=True)

with open('encoded.json', 'w') as rfile:
    json.dump(encoded, rfile, cls=NumpyEncoder)
```

# Size

Size before and after encoding. Encoding reduced package size by 10x.

![image](https://user-images.githubusercontent.com/8877753/115103478-d023bf80-9f17-11eb-9681-b03835097da1.png)

In 0.1.17 the optional gzip parameter was added to encode_json and decode_json. This allows the final package to be smaller, which allows for lower data size for sending across networks, or storing in a cache system like Redis.

![image](https://user-images.githubusercontent.com/8877753/150624141-81691e29-2004-4444-831c-802c52754fa9.jpeg)

The raw sample.json had a size of 281KB. 
The encoded json that is output from the program that is sorted and is using base64 style encoding is 27KB. 
The raw zipped sample.json is 26KB
The programs gzipped, encoded file is just 8KB. This is 1/3rd the size of the regular zip file, and just 1/35th of the original data size.

Data
Output
```json
{
    "Request": {
        "locations": [
            "XXX"
        ],
        "attributes": null,
        "aggregate": true,
        "startDate": "2021-04-12T01:46:08.8622635Z"
    },
    "Response": [
        {
            "LocationName": "XXX",
            "EntityType": "WIND_TURBINE",
            "DisplayName": "XXX",
            "Latitude": -1,
            "Longitude": -1,
            "Timezone": "Europe/Brussels",
            "DataSource": "ECMWF-IFS",
            "AsOfDateUTC": "2021-04-08T00:00:00Z",
            "ForecastWeather": [
                {
                    "AttributeName": "fresh_snow_6h:cm",
                    "AttributeUnitOfMeasure": "cm",
                    "AttributeDescription": "fresh snow of previous 6h [cm]",
                    "AttributeDataType": "Numeric",
                    "Values": {
                        "encoder": "TimeSeriesEncoder",
                        "start": 1618192800.0,
                        "ts_key": "UTC",
                        "ts_value": "Value",
                        "interval": 3600.0,
                        "static_value": 0.0,
                        "static_count": 143
                    }
                },
                {
                    "AttributeName": "precip_1h:mm",
                    "AttributeUnitOfMeasure": "mm",
                    "AttributeDescription": "amount of precipitation in the previous 1h [mm]",
                    "AttributeDataType": "Numeric",
                    "Values": {
                        "encoder": "TimeSeriesEncoder",
                        "start": 1618192800.0,
                        "ts_key": "UTC",
                        "ts_value": "Value",
                        "encoding_size": 64,
                        "data": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000KKKKKK888888TTTTTT888888000000",
                        "interval": 3600.0,
                        "encoding_depth": 1,
                        "float_precision": 2,
                        "signed": false
                    }
                },
                {
                    "AttributeName": "relative_humidity_100m:p",
                    "AttributeUnitOfMeasure": "%",
                    "AttributeDescription": "relative humidity at 100m [%]",
                    "AttributeDataType": "Numeric",
                    "Values": {
                        "encoder": "TimeSeriesEncoder",
                        "start": 1618192800.0,
                        "ts_key": "UTC",
                        "ts_value": "Value",
                        "encoding_size": 64,
                        "data": "BkBUBJB7AyAA9Q8i887b726d6B5m6P747m808H8Y8F7x7c7u8B8U9LAAA-AzAyAy9u8r7q7t7w7z8V939e9h9l9o9Y9I918y8u8p8l8g8c8K837o7Y7J74797F7K7Q7W7c7p818E8S8g8u8t8t8t8t8t8s8h8W8K897-7p828I8X8m909G9kADAiBBBgCACGCMCSCYCeCjC4BSAqAE9e939H9W9l9zACARB6BnCTD9DrEXEgEpExF4FCFKEtEQDzDWD4CdCBBmBKAuATA1ADAQAcAoA-BA",
                        "interval": 3600.0,
                        "encoding_depth": 2,
                        "float_precision": 1,
                        "signed": false
                    }
                }
            ]
        }
    ]
}
```
Input
```json
{
    "Request": {
        "locations": [
            "XXX"
        ],
        "attributes": null,
        "aggregate": true,
        "startDate": "2021-04-12T01:46:08.8622635Z"
    },
    "Response": [
        {
            "LocationName": "XXX",
            "EntityType": "XXX",
            "DisplayName": "BEZ_E01",
            "Latitude": -1,
            "Longitude": -1,
            "Timezone": "Europe/Brussels",
            "DataSource": "ECMWF-IFS",
            "AsOfDateUTC": "2021-04-08T00:00:00Z",
            "ForecastWeather": [
                {
                    "AttributeName": "fresh_snow_6h:cm",
                    "AttributeUnitOfMeasure": "cm",
                    "AttributeDescription": "fresh snow of previous 6h [cm]",
                    "AttributeDataType": "Numeric",
                    "Values": [
                        {
                            "UTC": "2021-04-12T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-18T00:00:00Z",
                            "Value": 0.0
                        }
                    ]
                },
                {
                    "AttributeName": "precip_1h:mm",
                    "AttributeUnitOfMeasure": "mm",
                    "AttributeDescription": "amount of precipitation in the previous 1h [mm]",
                    "AttributeDataType": "Numeric",
                    "Values": [
                        {
                            "UTC": "2021-04-12T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T19:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T20:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T21:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T22:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T23:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-17T00:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-17T01:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T02:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T03:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T04:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T05:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T06:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T07:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T08:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T09:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T10:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T11:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T12:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T13:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T14:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T15:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T16:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T17:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T18:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-18T00:00:00Z",
                            "Value": 0.0
                        }
                    ]
                },
                {
                    "AttributeName": "relative_humidity_100m:p",
                    "AttributeUnitOfMeasure": "%",
                    "AttributeDescription": "relative humidity at 100m [%]",
                    "AttributeDataType": "Numeric",
                    "Values": [
                        {
                            "UTC": "2021-04-12T02:00:00Z",
                            "Value": 75.0
                        },
                        {
                            "UTC": "2021-04-12T03:00:00Z",
                            "Value": 73.4
                        },
                        {
                            "UTC": "2021-04-12T04:00:00Z",
                            "Value": 72.3
                        },
                        {
                            "UTC": "2021-04-13T03:00:00Z",
                            "Value": 54.2
                        },
                        {
                            "UTC": "2021-04-13T04:00:00Z",
                            "Value": 59.7
                        },
                        {
                            "UTC": "2021-04-13T05:00:00Z",
                            "Value": 65.0
                        },
                        {
                            "UTC": "2021-04-13T06:00:00Z",
                            "Value": 70.2
                        },
                        {
                            "UTC": "2021-04-13T07:00:00Z",
                            "Value": 70.1
                        },
                        {
                            "UTC": "2021-04-13T08:00:00Z",
                            "Value": 70.0
                        },
                        {
                            "UTC": "2021-04-13T09:00:00Z",
                            "Value": 70.0
                        },
                        {
                            "UTC": "2021-04-13T10:00:00Z",
                            "Value": 63.2
                        },
                        {
                            "UTC": "2021-04-13T11:00:00Z",
                            "Value": 56.5
                        },
                        {
                            "UTC": "2021-04-13T12:00:00Z",
                            "Value": 50.0
                        },
                        {
                            "UTC": "2021-04-13T13:00:00Z",
                            "Value": 50.3
                        },
                        {
                            "UTC": "2021-04-13T14:00:00Z",
                            "Value": 50.6
                        },
                        {
                            "UTC": "2021-04-13T15:00:00Z",
                            "Value": 50.9
                        },
                        {
                            "UTC": "2021-04-13T16:00:00Z",
                            "Value": 54.3
                        },
                        {
                            "UTC": "2021-04-13T17:00:00Z",
                            "Value": 57.9
                        },
                        {
                            "UTC": "2021-04-13T18:00:00Z",
                            "Value": 61.6
                        },
                        {
                            "UTC": "2021-04-13T19:00:00Z",
                            "Value": 61.9
                        },
                        {
                            "UTC": "2021-04-13T20:00:00Z",
                            "Value": 62.3
                        },
                        {
                            "UTC": "2021-04-13T21:00:00Z",
                            "Value": 62.6
                        },
                        {
                            "UTC": "2021-04-13T22:00:00Z",
                            "Value": 61.0
                        },
                        {
                            "UTC": "2021-04-13T23:00:00Z",
                            "Value": 59.4
                        },
                        {
                            "UTC": "2021-04-14T00:00:00Z",
                            "Value": 57.7
                        },
                        {
                            "UTC": "2021-04-12T05:00:00Z",
                            "Value": 71.1
                        },
                        {
                            "UTC": "2021-04-12T06:00:00Z",
                            "Value": 70.0
                        },
                        {
                            "UTC": "2021-04-12T07:00:00Z",
                            "Value": 65.0
                        },
                        {
                            "UTC": "2021-04-12T08:00:00Z",
                            "Value": 60.2
                        },
                        {
                            "UTC": "2021-04-12T09:00:00Z",
                            "Value": 55.6
                        },
                        {
                            "UTC": "2021-04-12T10:00:00Z",
                            "Value": 52.0
                        },
                        {
                            "UTC": "2021-04-12T11:00:00Z",
                            "Value": 48.5
                        },
                        {
                            "UTC": "2021-04-12T12:00:00Z",
                            "Value": 45.0
                        },
                        {
                            "UTC": "2021-04-12T13:00:00Z",
                            "Value": 42.3
                        },
                        {
                            "UTC": "2021-04-12T14:00:00Z",
                            "Value": 39.5
                        },
                        {
                            "UTC": "2021-04-12T15:00:00Z",
                            "Value": 36.8
                        },
                        {
                            "UTC": "2021-04-12T16:00:00Z",
                            "Value": 40.9
                        },
                        {
                            "UTC": "2021-04-12T17:00:00Z",
                            "Value": 45.2
                        },
                        {
                            "UTC": "2021-04-12T18:00:00Z",
                            "Value": 49.6
                        },
                        {
                            "UTC": "2021-04-12T19:00:00Z",
                            "Value": 51.2
                        },
                        {
                            "UTC": "2021-04-12T20:00:00Z",
                            "Value": 52.9
                        },
                        {
                            "UTC": "2021-04-12T21:00:00Z",
                            "Value": 54.6
                        },
                        {
                            "UTC": "2021-04-12T22:00:00Z",
                            "Value": 52.7
                        },
                        {
                            "UTC": "2021-04-12T23:00:00Z",
                            "Value": 50.7
                        },
                        {
                            "UTC": "2021-04-13T00:00:00Z",
                            "Value": 48.6
                        },
                        {
                            "UTC": "2021-04-13T01:00:00Z",
                            "Value": 50.4
                        },
                        {
                            "UTC": "2021-04-13T02:00:00Z",
                            "Value": 52.3
                        },
                        {
                            "UTC": "2021-04-14T01:00:00Z",
                            "Value": 57.2
                        },
                        {
                            "UTC": "2021-04-14T02:00:00Z",
                            "Value": 56.8
                        },
                        {
                            "UTC": "2021-04-14T03:00:00Z",
                            "Value": 56.3
                        },
                        {
                            "UTC": "2021-04-14T04:00:00Z",
                            "Value": 55.9
                        },
                        {
                            "UTC": "2021-04-14T05:00:00Z",
                            "Value": 55.4
                        },
                        {
                            "UTC": "2021-04-14T06:00:00Z",
                            "Value": 55.0
                        },
                        {
                            "UTC": "2021-04-14T07:00:00Z",
                            "Value": 53.2
                        },
                        {
                            "UTC": "2021-04-14T08:00:00Z",
                            "Value": 51.5
                        },
                        {
                            "UTC": "2021-04-14T09:00:00Z",
                            "Value": 49.8
                        },
                        {
                            "UTC": "2021-04-14T10:00:00Z",
                            "Value": 48.2
                        },
                        {
                            "UTC": "2021-04-14T11:00:00Z",
                            "Value": 46.7
                        },
                        {
                            "UTC": "2021-04-14T12:00:00Z",
                            "Value": 45.2
                        },
                        {
                            "UTC": "2021-04-14T13:00:00Z",
                            "Value": 45.7
                        },
                        {
                            "UTC": "2021-04-14T14:00:00Z",
                            "Value": 46.3
                        },
                        {
                            "UTC": "2021-04-14T15:00:00Z",
                            "Value": 46.8
                        },
                        {
                            "UTC": "2021-04-14T16:00:00Z",
                            "Value": 47.4
                        },
                        {
                            "UTC": "2021-04-14T17:00:00Z",
                            "Value": 48.0
                        },
                        {
                            "UTC": "2021-04-14T18:00:00Z",
                            "Value": 48.6
                        },
                        {
                            "UTC": "2021-04-14T19:00:00Z",
                            "Value": 49.9
                        },
                        {
                            "UTC": "2021-04-14T20:00:00Z",
                            "Value": 51.3
                        },
                        {
                            "UTC": "2021-04-14T21:00:00Z",
                            "Value": 52.6
                        },
                        {
                            "UTC": "2021-04-14T22:00:00Z",
                            "Value": 54.0
                        },
                        {
                            "UTC": "2021-04-14T23:00:00Z",
                            "Value": 55.4
                        },
                        {
                            "UTC": "2021-04-15T00:00:00Z",
                            "Value": 56.8
                        },
                        {
                            "UTC": "2021-04-15T01:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T02:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T03:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T04:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T05:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T06:00:00Z",
                            "Value": 56.6
                        },
                        {
                            "UTC": "2021-04-15T07:00:00Z",
                            "Value": 55.5
                        },
                        {
                            "UTC": "2021-04-15T08:00:00Z",
                            "Value": 54.4
                        },
                        {
                            "UTC": "2021-04-15T09:00:00Z",
                            "Value": 53.2
                        },
                        {
                            "UTC": "2021-04-15T10:00:00Z",
                            "Value": 52.1
                        },
                        {
                            "UTC": "2021-04-15T11:00:00Z",
                            "Value": 51.0
                        },
                        {
                            "UTC": "2021-04-15T12:00:00Z",
                            "Value": 49.9
                        },
                        {
                            "UTC": "2021-04-15T13:00:00Z",
                            "Value": 51.4
                        },
                        {
                            "UTC": "2021-04-15T14:00:00Z",
                            "Value": 53.0
                        },
                        {
                            "UTC": "2021-04-15T15:00:00Z",
                            "Value": 54.5
                        },
                        {
                            "UTC": "2021-04-15T16:00:00Z",
                            "Value": 56.0
                        },
                        {
                            "UTC": "2021-04-15T17:00:00Z",
                            "Value": 57.6
                        },
                        {
                            "UTC": "2021-04-15T18:00:00Z",
                            "Value": 59.2
                        },
                        {
                            "UTC": "2021-04-15T19:00:00Z",
                            "Value": 62.2
                        },
                        {
                            "UTC": "2021-04-15T20:00:00Z",
                            "Value": 65.3
                        },
                        {
                            "UTC": "2021-04-15T21:00:00Z",
                            "Value": 68.4
                        },
                        {
                            "UTC": "2021-04-15T22:00:00Z",
                            "Value": 71.5
                        },
                        {
                            "UTC": "2021-04-15T23:00:00Z",
                            "Value": 74.6
                        },
                        {
                            "UTC": "2021-04-16T00:00:00Z",
                            "Value": 77.8
                        },
                        {
                            "UTC": "2021-04-16T01:00:00Z",
                            "Value": 78.4
                        },
                        {
                            "UTC": "2021-04-16T02:00:00Z",
                            "Value": 79.0
                        },
                        {
                            "UTC": "2021-04-16T03:00:00Z",
                            "Value": 79.6
                        },
                        {
                            "UTC": "2021-04-16T04:00:00Z",
                            "Value": 80.2
                        },
                        {
                            "UTC": "2021-04-16T05:00:00Z",
                            "Value": 80.8
                        },
                        {
                            "UTC": "2021-04-16T06:00:00Z",
                            "Value": 81.3
                        },
                        {
                            "UTC": "2021-04-16T07:00:00Z",
                            "Value": 77.2
                        },
                        {
                            "UTC": "2021-04-16T08:00:00Z",
                            "Value": 73.2
                        },
                        {
                            "UTC": "2021-04-16T09:00:00Z",
                            "Value": 69.2
                        },
                        {
                            "UTC": "2021-04-16T10:00:00Z",
                            "Value": 65.4
                        },
                        {
                            "UTC": "2021-04-16T11:00:00Z",
                            "Value": 61.6
                        },
                        {
                            "UTC": "2021-04-16T12:00:00Z",
                            "Value": 57.9
                        },
                        {
                            "UTC": "2021-04-16T13:00:00Z",
                            "Value": 59.3
                        },
                        {
                            "UTC": "2021-04-16T14:00:00Z",
                            "Value": 60.8
                        },
                        {
                            "UTC": "2021-04-16T15:00:00Z",
                            "Value": 62.3
                        },
                        {
                            "UTC": "2021-04-16T16:00:00Z",
                            "Value": 63.7
                        },
                        {
                            "UTC": "2021-04-16T17:00:00Z",
                            "Value": 65.2
                        },
                        {
                            "UTC": "2021-04-16T18:00:00Z",
                            "Value": 66.7
                        },
                        {
                            "UTC": "2021-04-16T19:00:00Z",
                            "Value": 71.0
                        },
                        {
                            "UTC": "2021-04-16T20:00:00Z",
                            "Value": 75.3
                        },
                        {
                            "UTC": "2021-04-16T21:00:00Z",
                            "Value": 79.7
                        },
                        {
                            "UTC": "2021-04-16T22:00:00Z",
                            "Value": 84.1
                        },
                        {
                            "UTC": "2021-04-16T23:00:00Z",
                            "Value": 88.5
                        },
                        {
                            "UTC": "2021-04-17T00:00:00Z",
                            "Value": 92.9
                        },
                        {
                            "UTC": "2021-04-17T01:00:00Z",
                            "Value": 93.8
                        },
                        {
                            "UTC": "2021-04-17T02:00:00Z",
                            "Value": 94.7
                        },
                        {
                            "UTC": "2021-04-17T03:00:00Z",
                            "Value": 95.5
                        },
                        {
                            "UTC": "2021-04-17T04:00:00Z",
                            "Value": 96.4
                        },
                        {
                            "UTC": "2021-04-17T05:00:00Z",
                            "Value": 97.2
                        },
                        {
                            "UTC": "2021-04-17T06:00:00Z",
                            "Value": 98.0
                        },
                        {
                            "UTC": "2021-04-17T07:00:00Z",
                            "Value": 95.1
                        },
                        {
                            "UTC": "2021-04-17T08:00:00Z",
                            "Value": 92.2
                        },
                        {
                            "UTC": "2021-04-17T09:00:00Z",
                            "Value": 89.3
                        },
                        {
                            "UTC": "2021-04-17T10:00:00Z",
                            "Value": 86.4
                        },
                        {
                            "UTC": "2021-04-17T11:00:00Z",
                            "Value": 83.6
                        },
                        {
                            "UTC": "2021-04-17T12:00:00Z",
                            "Value": 80.7
                        },
                        {
                            "UTC": "2021-04-17T13:00:00Z",
                            "Value": 77.9
                        },
                        {
                            "UTC": "2021-04-17T14:00:00Z",
                            "Value": 75.2
                        },
                        {
                            "UTC": "2021-04-17T15:00:00Z",
                            "Value": 72.4
                        },
                        {
                            "UTC": "2021-04-17T16:00:00Z",
                            "Value": 69.6
                        },
                        {
                            "UTC": "2021-04-17T17:00:00Z",
                            "Value": 66.9
                        },
                        {
                            "UTC": "2021-04-17T18:00:00Z",
                            "Value": 64.1
                        },
                        {
                            "UTC": "2021-04-17T19:00:00Z",
                            "Value": 65.3
                        },
                        {
                            "UTC": "2021-04-17T20:00:00Z",
                            "Value": 66.6
                        },
                        {
                            "UTC": "2021-04-17T21:00:00Z",
                            "Value": 67.8
                        },
                        {
                            "UTC": "2021-04-17T22:00:00Z",
                            "Value": 69.0
                        },
                        {
                            "UTC": "2021-04-17T23:00:00Z",
                            "Value": 70.2
                        },
                        {
                            "UTC": "2021-04-18T00:00:00Z",
                            "Value": 71.4
                        }
                    ]
                }
            ]
        }
    ]
}
```
