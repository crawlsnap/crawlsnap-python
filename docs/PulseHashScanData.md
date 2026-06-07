# PulseHashScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**crawlsnap_hash_id** | **str** |  | 
**search_type** | **str** |  | 
**pulse_detail** | **Dict[str, object]** |  | [optional] 
**analysis** | **Dict[str, object]** | Hybrid Analysis sandbox + Cuckoo plugin output (free-form). The Cuckoo output is curated before return/cache: low-value raw dumps are removed and long-tail arrays capped; all IOCs are preserved.  | [optional] 

## Example

```python
from crawlsnap.models.pulse_hash_scan_data import PulseHashScanData

# TODO update the JSON string below
json = "{}"
# create an instance of PulseHashScanData from a JSON string
pulse_hash_scan_data_instance = PulseHashScanData.from_json(json)
# print the JSON string representation of the object
print(PulseHashScanData.to_json())

# convert the object into a dict
pulse_hash_scan_data_dict = pulse_hash_scan_data_instance.to_dict()
# create an instance of PulseHashScanData from a dict
pulse_hash_scan_data_from_dict = PulseHashScanData.from_dict(pulse_hash_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


