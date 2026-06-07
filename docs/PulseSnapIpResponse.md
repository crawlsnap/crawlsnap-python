# PulseSnapIpResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PulseIpScanData**](PulseIpScanData.md) |  | [optional] 
**is_success** | **bool** | True only when &#x60;data&#x60; contains usable enrichment. | 
**message** | **str** | Human-readable summary of the outcome. | 
**response_code** | **int** | Mirrors the HTTP status code. | 

## Example

```python
from crawlsnap.models.pulse_snap_ip_response import PulseSnapIpResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PulseSnapIpResponse from a JSON string
pulse_snap_ip_response_instance = PulseSnapIpResponse.from_json(json)
# print the JSON string representation of the object
print(PulseSnapIpResponse.to_json())

# convert the object into a dict
pulse_snap_ip_response_dict = pulse_snap_ip_response_instance.to_dict()
# create an instance of PulseSnapIpResponse from a dict
pulse_snap_ip_response_from_dict = PulseSnapIpResponse.from_dict(pulse_snap_ip_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


