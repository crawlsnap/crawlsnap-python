# IocUrlScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash_id** | **str** | SHA-256 of the queried URL. | 
**search_type** | **str** |  | 
**url** | **str** |  | [optional] 
**modification_date** | **int** | Unix timestamp of the last upstream modification. | [optional] 
**analysis_date** | **int** |  | [optional] 
**reputation** | **int** |  | [optional] 
**threat_names** | **List[str]** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**categories** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis_stats** | **Dict[str, object]** |  | [optional] 
**url_content** | **Dict[str, object]** |  | [optional] 
**network** | **Dict[str, object]** |  | [optional] 

## Example

```python
from crawlsnap.models.ioc_url_scan_data import IocUrlScanData

# TODO update the JSON string below
json = "{}"
# create an instance of IocUrlScanData from a JSON string
ioc_url_scan_data_instance = IocUrlScanData.from_json(json)
# print the JSON string representation of the object
print(IocUrlScanData.to_json())

# convert the object into a dict
ioc_url_scan_data_dict = ioc_url_scan_data_instance.to_dict()
# create an instance of IocUrlScanData from a dict
ioc_url_scan_data_from_dict = IocUrlScanData.from_dict(ioc_url_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


