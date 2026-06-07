# crawlsnap.PulseSnapApi

All URIs are relative to *https://api.crawlsnap.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pulse_snap_domain**](PulseSnapApi.md#pulse_snap_domain) | **GET** /v1/pulse-snap/scan/domain | AlienVault OTX pulse enrichment for a domain.
[**pulse_snap_hash**](PulseSnapApi.md#pulse_snap_hash) | **GET** /v1/pulse-snap/scan/hash | AlienVault OTX pulse + sandbox enrichment for a file hash.
[**pulse_snap_ip**](PulseSnapApi.md#pulse_snap_ip) | **GET** /v1/pulse-snap/scan/ip | AlienVault OTX pulse enrichment for an IPv4 address.
[**pulse_snap_url**](PulseSnapApi.md#pulse_snap_url) | **GET** /v1/pulse-snap/scan/url | AlienVault OTX pulse enrichment for a URL.


# **pulse_snap_domain**
> PulseSnapDomainResponse pulse_snap_domain(query)

AlienVault OTX pulse enrichment for a domain.

AlienVault OTX pulse summary, associated malware, and passive DNS for
the supplied domain.


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.pulse_snap_domain_response import PulseSnapDomainResponse
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
    api_instance = crawlsnap.PulseSnapApi(api_client)
    query = 'google.com' # str | The domain to enrich.

    try:
        # AlienVault OTX pulse enrichment for a domain.
        api_response = api_instance.pulse_snap_domain(query)
        print("The response of PulseSnapApi->pulse_snap_domain:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseSnapApi->pulse_snap_domain: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The domain to enrich. | 

### Return type

[**PulseSnapDomainResponse**](PulseSnapDomainResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful enrichment. |  -  |
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

# **pulse_snap_hash**
> PulseSnapHashResponse pulse_snap_hash(query)

AlienVault OTX pulse + sandbox enrichment for a file hash.

AlienVault OTX pulse summary plus sandbox (Hybrid Analysis / Cuckoo)
analysis for the supplied file hash.


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.pulse_snap_hash_response import PulseSnapHashResponse
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
    api_instance = crawlsnap.PulseSnapApi(api_client)
    query = '44d88612fea8a8f36de82e1278abb02f' # str | The file hash to enrich (MD5, SHA-1, or SHA-256).

    try:
        # AlienVault OTX pulse + sandbox enrichment for a file hash.
        api_response = api_instance.pulse_snap_hash(query)
        print("The response of PulseSnapApi->pulse_snap_hash:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseSnapApi->pulse_snap_hash: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The file hash to enrich (MD5, SHA-1, or SHA-256). | 

### Return type

[**PulseSnapHashResponse**](PulseSnapHashResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful enrichment. |  -  |
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

# **pulse_snap_ip**
> PulseSnapIpResponse pulse_snap_ip(query)

AlienVault OTX pulse enrichment for an IPv4 address.

AlienVault OTX pulse summary, associated malware, and passive DNS for
the supplied IPv4 address.


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.pulse_snap_ip_response import PulseSnapIpResponse
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
    api_instance = crawlsnap.PulseSnapApi(api_client)
    query = '8.8.8.8' # str | The IPv4 address to enrich.

    try:
        # AlienVault OTX pulse enrichment for an IPv4 address.
        api_response = api_instance.pulse_snap_ip(query)
        print("The response of PulseSnapApi->pulse_snap_ip:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseSnapApi->pulse_snap_ip: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The IPv4 address to enrich. | 

### Return type

[**PulseSnapIpResponse**](PulseSnapIpResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful enrichment. |  -  |
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

# **pulse_snap_url**
> PulseSnapUrlResponse pulse_snap_url(query)

AlienVault OTX pulse enrichment for a URL.

AlienVault OTX pulse summary for the supplied URL.

### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.pulse_snap_url_response import PulseSnapUrlResponse
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
    api_instance = crawlsnap.PulseSnapApi(api_client)
    query = 'https://example.com' # str | The URL to enrich.

    try:
        # AlienVault OTX pulse enrichment for a URL.
        api_response = api_instance.pulse_snap_url(query)
        print("The response of PulseSnapApi->pulse_snap_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseSnapApi->pulse_snap_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The URL to enrich. | 

### Return type

[**PulseSnapUrlResponse**](PulseSnapUrlResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful enrichment. |  -  |
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

