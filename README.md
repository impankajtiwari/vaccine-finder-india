# vaccine-finder-india
Find open/free vaccine slots using a filter criteria

## Install

This project requires [Python](https://www.python.org/downloads/) & [pip](https://pypi.org/project/pip/) to be locally installed.

```python
pip install -r requirements.txt
```

## Run

```
python vaccine-finder.py <age-filter> <district-id> <scan-frequency> <appointment-count-threshold> 
```
### Parameters
* _age-filter_ - Valid values '18' or '45'
* _district-id_ - Use the values from [here](https://cdn-api.co-vin.in/api/v2/admin/location/districts/16)
* _scan-frequency_ - Frequency of checking for slots (default 30 seconds)
* _appointment-count-threshold_ - Notify only when number of free appointments > the threshold value