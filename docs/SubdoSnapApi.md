# crawlsnap.SubdoSnapApi

All URIs are relative to *https://api.crawlsnap.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**subdo_snap_scan**](SubdoSnapApi.md#subdo_snap_scan) | **GET** /v1/subdo-snap/scan | Paginated subdomain enumeration for a domain.


# **subdo_snap_scan**
> SubdoSnapScanResponse subdo_snap_scan(query, cursor=cursor)

Paginated subdomain enumeration for a domain.

Enumerates known subdomains for the supplied domain. Results are
paginated: when more pages are available the response `data.cursor`
is non-empty — pass it back as the `cursor` query parameter to fetch
the next page.


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.subdo_snap_scan_response import SubdoSnapScanResponse
from crawlsnap.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.crawlsnap.com
# See configuration.py for a list of all supported configuration parameters.
configuration = crawlsnap.Configuration(
    host = "https://api.crawlsnap.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = crawlsnap.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with crawlsnap.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = crawlsnap.SubdoSnapApi(api_client)
    query = 'google.com' # str | The domain to enrich.
    cursor = 'cursor_example' # str | Opaque pagination cursor returned as `data.cursor` by a previous response. Omit on the first request.  (optional)

    try:
        # Paginated subdomain enumeration for a domain.
        api_response = api_instance.subdo_snap_scan(query, cursor=cursor)
        print("The response of SubdoSnapApi->subdo_snap_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SubdoSnapApi->subdo_snap_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The domain to enrich. | 
 **cursor** | **str**| Opaque pagination cursor returned as &#x60;data.cursor&#x60; by a previous response. Omit on the first request.  | [optional] 

### Return type

[**SubdoSnapScanResponse**](SubdoSnapScanResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful enumeration. |  -  |
**400** | Invalid input — malformed URL, hash, IP, or domain. |  -  |
**401** | Missing or invalid API key. |  -  |
**402** | Out of credits, or the subscription&#39;s monthly quota is exceeded. |  -  |
**403** | The subscription tied to this key is not active. |  -  |
**404** | No IoC data was found for the supplied indicator. |  -  |
**429** | The API key&#39;s daily request limit has been exceeded. |  -  |
**500** | Unexpected server-side failure. |  -  |
**503** | The upstream enrichment service was unavailable. |  -  |
**504** | The upstream enrichment service timed out. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

