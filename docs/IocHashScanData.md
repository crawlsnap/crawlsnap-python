# IocHashScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash_id** | **str** | SHA-256 of the queried hash (resolved upstream when md5/sha1 supplied). | 
**search_type** | **str** |  | 
**ssdeep** | **str** |  | [optional] 
**type_tag** | **str** |  | [optional] 
**type_tags** | **List[str]** |  | [optional] 
**magic** | **str** |  | [optional] 
**magika** | **str** |  | [optional] 
**type_description** | **str** |  | [optional] 
**meaningful_name** | **str** |  | [optional] 
**authentihash** | **str** |  | [optional] 
**detectiteasy** | **Dict[str, object]** |  | [optional] 
**trid** | **List[Dict[str, object]]** |  | [optional] 
**type_extension** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**tlsh** | **str** |  | [optional] 
**analysis_date** | **int** |  | [optional] 
**modification_date** | **int** |  | [optional] 
**md5** | **str** |  | [optional] 
**sha1** | **str** |  | [optional] 
**sha256** | **str** |  | [optional] 
**file_size** | **int** |  | [optional] 
**dropped_files** | **List[Dict[str, object]]** |  | [optional] 
**bundled_files** | **List[Dict[str, object]]** |  | [optional] 
**contacted_ips** | **List[Dict[str, object]]** |  | [optional] 
**contacted_domains** | **List[Dict[str, object]]** |  | [optional] 
**sigma** | **Dict[str, object]** |  | [optional] 
**sigma_stats** | **Dict[str, object]** |  | [optional] 
**classification** | **Dict[str, object]** |  | [optional] 
**pe_info** | **Dict[str, object]** |  | [optional] 
**signature** | **Dict[str, object]** |  | [optional] 
**votes_result** | **Dict[str, object]** |  | [optional] 
**sandbox_verdicts** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis_stats** | **Dict[str, object]** |  | [optional] 

## Example

```python
from crawlsnap.models.ioc_hash_scan_data import IocHashScanData

# TODO update the JSON string below
json = "{}"
# create an instance of IocHashScanData from a JSON string
ioc_hash_scan_data_instance = IocHashScanData.from_json(json)
# print the JSON string representation of the object
print(IocHashScanData.to_json())

# convert the object into a dict
ioc_hash_scan_data_dict = ioc_hash_scan_data_instance.to_dict()
# create an instance of IocHashScanData from a dict
ioc_hash_scan_data_from_dict = IocHashScanData.from_dict(ioc_hash_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


