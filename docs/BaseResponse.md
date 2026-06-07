# BaseResponse

The envelope wrapping every CrawlSnap API response. Inspect `is_success` before reading `data`. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **object** | Endpoint-specific payload, refined per endpoint via allOf wrappers. Null on failure (&#x60;is_success: false&#x60;).  | [optional] 
**is_success** | **bool** | True only when &#x60;data&#x60; contains usable enrichment. | 
**message** | **str** | Human-readable summary of the outcome. | 
**response_code** | **int** | Mirrors the HTTP status code. | 

## Example

```python
from crawlsnap.models.base_response import BaseResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BaseResponse from a JSON string
base_response_instance = BaseResponse.from_json(json)
# print the JSON string representation of the object
print(BaseResponse.to_json())

# convert the object into a dict
base_response_dict = base_response_instance.to_dict()
# create an instance of BaseResponse from a dict
base_response_from_dict = BaseResponse.from_dict(base_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


