# IocIpScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash_id** | **str** |  | 
**search_type** | **str** |  | 
**ip** | **str** |  | [optional] 
**country** | **str** |  | [optional] 
**reputation** | **int** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**whois** | **str** |  | [optional] 
**whois_update_date** | **int** |  | [optional] 
**asn** | **int** |  | [optional] 
**as_owner** | **str** |  | [optional] 
**network** | **str** |  | [optional] 
**internet_registry** | **str** |  | [optional] 
**continent** | **str** |  | [optional] 
**modification_date** | **int** |  | [optional] 
**analysis_date** | **int** |  | [optional] 
**votes_result** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis_stats** | **Dict[str, object]** |  | [optional] 
**referrer_files** | **List[Dict[str, object]]** |  | [optional] 
**communicating_files** | **List[Dict[str, object]]** |  | [optional] 
**resolutions** | **List[Dict[str, object]]** |  | [optional] 

## Example

```python
from crawlsnap.models.ioc_ip_scan_data import IocIpScanData

# TODO update the JSON string below
json = "{}"
# create an instance of IocIpScanData from a JSON string
ioc_ip_scan_data_instance = IocIpScanData.from_json(json)
# print the JSON string representation of the object
print(IocIpScanData.to_json())

# convert the object into a dict
ioc_ip_scan_data_dict = ioc_ip_scan_data_instance.to_dict()
# create an instance of IocIpScanData from a dict
ioc_ip_scan_data_from_dict = IocIpScanData.from_dict(ioc_ip_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


