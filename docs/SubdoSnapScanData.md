# SubdoSnapScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash_id** | **str** |  | 
**search_type** | **str** |  | 
**subdomains** | **List[Dict[str, object]]** |  | [optional] 
**cursor** | **str** | Opaque pagination cursor for the next page (empty when no more pages). | [optional] 
**count** | **int** | Total subdomain count reported by upstream. | [optional] 

## Example

```python
from crawlsnap.models.subdo_snap_scan_data import SubdoSnapScanData

# TODO update the JSON string below
json = "{}"
# create an instance of SubdoSnapScanData from a JSON string
subdo_snap_scan_data_instance = SubdoSnapScanData.from_json(json)
# print the JSON string representation of the object
print(SubdoSnapScanData.to_json())

# convert the object into a dict
subdo_snap_scan_data_dict = subdo_snap_scan_data_instance.to_dict()
# create an instance of SubdoSnapScanData from a dict
subdo_snap_scan_data_from_dict = SubdoSnapScanData.from_dict(subdo_snap_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


