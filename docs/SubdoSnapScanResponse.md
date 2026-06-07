# SubdoSnapScanResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**SubdoSnapScanData**](SubdoSnapScanData.md) |  | [optional] 
**is_success** | **bool** | True only when &#x60;data&#x60; contains usable enrichment. | 
**message** | **str** | Human-readable summary of the outcome. | 
**response_code** | **int** | Mirrors the HTTP status code. | 

## Example

```python
from crawlsnap.models.subdo_snap_scan_response import SubdoSnapScanResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubdoSnapScanResponse from a JSON string
subdo_snap_scan_response_instance = SubdoSnapScanResponse.from_json(json)
# print the JSON string representation of the object
print(SubdoSnapScanResponse.to_json())

# convert the object into a dict
subdo_snap_scan_response_dict = subdo_snap_scan_response_instance.to_dict()
# create an instance of SubdoSnapScanResponse from a dict
subdo_snap_scan_response_from_dict = SubdoSnapScanResponse.from_dict(subdo_snap_scan_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


