# PulseSnapHashResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PulseHashScanData**](PulseHashScanData.md) |  | [optional] 
**is_success** | **bool** | True only when &#x60;data&#x60; contains usable enrichment. | 
**message** | **str** | Human-readable summary of the outcome. | 
**response_code** | **int** | Mirrors the HTTP status code. | 

## Example

```python
from crawlsnap.models.pulse_snap_hash_response import PulseSnapHashResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PulseSnapHashResponse from a JSON string
pulse_snap_hash_response_instance = PulseSnapHashResponse.from_json(json)
# print the JSON string representation of the object
print(PulseSnapHashResponse.to_json())

# convert the object into a dict
pulse_snap_hash_response_dict = pulse_snap_hash_response_instance.to_dict()
# create an instance of PulseSnapHashResponse from a dict
pulse_snap_hash_response_from_dict = PulseSnapHashResponse.from_dict(pulse_snap_hash_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


