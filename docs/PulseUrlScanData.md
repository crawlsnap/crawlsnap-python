# PulseUrlScanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**crawlsnap_hash_id** | **str** | SHA-256 of the queried URL. | 
**search_type** | **str** |  | 
**pulse_detail** | **Dict[str, object]** | OTX-derived pulse summary. Inner shape evolves with upstream; kept free-form on purpose (see phase-2 plan Decision #5).  | [optional] 

## Example

```python
from crawlsnap.models.pulse_url_scan_data import PulseUrlScanData

# TODO update the JSON string below
json = "{}"
# create an instance of PulseUrlScanData from a JSON string
pulse_url_scan_data_instance = PulseUrlScanData.from_json(json)
# print the JSON string representation of the object
print(PulseUrlScanData.to_json())

# convert the object into a dict
pulse_url_scan_data_dict = pulse_url_scan_data_instance.to_dict()
# create an instance of PulseUrlScanData from a dict
pulse_url_scan_data_from_dict = PulseUrlScanData.from_dict(pulse_url_scan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


