# PulseSnapUrlResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PulseUrlScanData**](PulseUrlScanData.md) |  | [optional] 
**is_success** | **bool** | True only when &#x60;data&#x60; contains usable enrichment. | 
**message** | **str** | Human-readable summary of the outcome. | 
**response_code** | **int** | Mirrors the HTTP status code. | 

## Example

```python
from crawlsnap.models.pulse_snap_url_response import PulseSnapUrlResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PulseSnapUrlResponse from a JSON string
pulse_snap_url_response_instance = PulseSnapUrlResponse.from_json(json)
# print the JSON string representation of the object
print(PulseSnapUrlResponse.to_json())

# convert the object into a dict
pulse_snap_url_response_dict = pulse_snap_url_response_instance.to_dict()
# create an instance of PulseSnapUrlResponse from a dict
pulse_snap_url_response_from_dict = PulseSnapUrlResponse.from_dict(pulse_snap_url_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


