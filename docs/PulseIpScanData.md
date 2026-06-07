# PulseIpScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**crawlsnap_hash_id** | **str** |  | 
**search_type** | **str** |  | 
**pulse_detail** | **Dict[str, object]** |  | [optional] 
**malware** | **List[Dict[str, object]]** |  | [optional] 
**passive_dns** | **List[Dict[str, object]]** |  | [optional] 

## Example

```python
from crawlsnap.models.pulse_ip_scan_data import PulseIpScanData

# TODO update the JSON string below
json = "{}"
# create an instance of PulseIpScanData from a JSON string
pulse_ip_scan_data_instance = PulseIpScanData.from_json(json)
# print the JSON string representation of the object
print(PulseIpScanData.to_json())

# convert the object into a dict
pulse_ip_scan_data_dict = pulse_ip_scan_data_instance.to_dict()
# create an instance of PulseIpScanData from a dict
pulse_ip_scan_data_from_dict = PulseIpScanData.from_dict(pulse_ip_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


