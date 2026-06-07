# PulseSnapDomainResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PulseDomainScanData**](PulseDomainScanData.md) |  | [optional] 
**is_success** | **bool** | True only when &#x60;data&#x60; contains usable enrichment. | 
**message** | **str** | Human-readable summary of the outcome. | 
**response_code** | **int** | Mirrors the HTTP status code. | 

## Example

```python
from crawlsnap.models.pulse_snap_domain_response import PulseSnapDomainResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PulseSnapDomainResponse from a JSON string
pulse_snap_domain_response_instance = PulseSnapDomainResponse.from_json(json)
# print the JSON string representation of the object
print(PulseSnapDomainResponse.to_json())

# convert the object into a dict
pulse_snap_domain_response_dict = pulse_snap_domain_response_instance.to_dict()
# create an instance of PulseSnapDomainResponse from a dict
pulse_snap_domain_response_from_dict = PulseSnapDomainResponse.from_dict(pulse_snap_domain_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


