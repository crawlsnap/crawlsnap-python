# VectorScanIpResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**IocIpScanData**](IocIpScanData.md) |  | [optional] 
**is_success** | **bool** | True only when &#x60;data&#x60; contains usable enrichment. | 
**message** | **str** | Human-readable summary of the outcome. | 
**response_code** | **int** | Mirrors the HTTP status code. | 

## Example

```python
from crawlsnap.models.vector_scan_ip_response import VectorScanIpResponse

# TODO update the JSON string below
json = "{}"
# create an instance of VectorScanIpResponse from a JSON string
vector_scan_ip_response_instance = VectorScanIpResponse.from_json(json)
# print the JSON string representation of the object
print(VectorScanIpResponse.to_json())

# convert the object into a dict
vector_scan_ip_response_dict = vector_scan_ip_response_instance.to_dict()
# create an instance of VectorScanIpResponse from a dict
vector_scan_ip_response_from_dict = VectorScanIpResponse.from_dict(vector_scan_ip_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


