# IocDomainScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash_id** | **str** |  | 
**search_type** | **str** |  | 
**domain** | **str** |  | [optional] 
**reputation** | **int** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**whois** | **str** |  | [optional] 
**whois_update_date** | **int** |  | [optional] 
**modification_date** | **int** |  | [optional] 
**tld** | **str** |  | [optional] 
**dns_records_update_date** | **int** |  | [optional] 
**http_certificate_update_date** | **int** |  | [optional] 
**jarm** | **str** |  | [optional] 
**registrar** | **str** |  | [optional] 
**analysis_date** | **int** |  | [optional] 
**votes_result** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis** | **Dict[str, object]** |  | [optional] 
**security_vendor_analysis_stats** | **Dict[str, object]** |  | [optional] 
**categories** | **Dict[str, object]** |  | [optional] 
**popularity_ranks** | **Dict[str, object]** |  | [optional] 
**dns_records** | **List[Dict[str, object]]** |  | [optional] 
**http_certificate** | **Dict[str, object]** |  | [optional] 
**referrer_files** | **List[Dict[str, object]]** |  | [optional] 
**communicating_files** | **List[Dict[str, object]]** |  | [optional] 
**subdomains** | **List[Dict[str, object]]** |  | [optional] 
**resolutions** | **List[Dict[str, object]]** |  | [optional] 
**siblings** | **List[Dict[str, object]]** |  | [optional] 

## Example

```python
from crawlsnap.models.ioc_domain_scan_data import IocDomainScanData

# TODO update the JSON string below
json = "{}"
# create an instance of IocDomainScanData from a JSON string
ioc_domain_scan_data_instance = IocDomainScanData.from_json(json)
# print the JSON string representation of the object
print(IocDomainScanData.to_json())

# convert the object into a dict
ioc_domain_scan_data_dict = ioc_domain_scan_data_instance.to_dict()
# create an instance of IocDomainScanData from a dict
ioc_domain_scan_data_from_dict = IocDomainScanData.from_dict(ioc_domain_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


