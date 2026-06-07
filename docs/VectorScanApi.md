# crawlsnap.VectorScanApi

All URIs are relative to *https://api.crawlsnap.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**vector_scan_domain**](VectorScanApi.md#vector_scan_domain) | **GET** /v1/ioc/search/domain | VirusTotal IoC enrichment for a domain.
[**vector_scan_hash**](VectorScanApi.md#vector_scan_hash) | **GET** /v1/ioc/search/hash | VirusTotal IoC enrichment for a file hash.
[**vector_scan_ip**](VectorScanApi.md#vector_scan_ip) | **GET** /v1/ioc/search/ip | VirusTotal IoC enrichment for an IPv4 address.
[**vector_scan_url**](VectorScanApi.md#vector_scan_url) | **GET** /v1/ioc/search/url | VirusTotal IoC enrichment for a URL.


# **vector_scan_domain**
> VectorScanDomainResponse vector_scan_domain(query)

VirusTotal IoC enrichment for a domain.

Returns VirusTotal-derived reputation, WHOIS, DNS records, certificates,
categories, and relationships for the supplied domain.


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.vector_scan_domain_response import VectorScanDomainResponse
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
    api_instance = crawlsnap.VectorScanApi(api_client)
    query = 'google.com' # str | The domain to enrich.

    try:
        # VirusTotal IoC enrichment for a domain.
        api_response = api_instance.vector_scan_domain(query)
        print("The response of VectorScanApi->vector_scan_domain:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VectorScanApi->vector_scan_domain: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The domain to enrich. | 

### Return type

[**VectorScanDomainResponse**](VectorScanDomainResponse.md)

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

# **vector_scan_hash**
> VectorScanHashResponse vector_scan_hash(query)

VirusTotal IoC enrichment for a file hash.

Returns VirusTotal-derived file analysis for the supplied hash
(MD5, SHA-1, or SHA-256 accepted; resolved to SHA-256 upstream).


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.vector_scan_hash_response import VectorScanHashResponse
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
    api_instance = crawlsnap.VectorScanApi(api_client)
    query = '44d88612fea8a8f36de82e1278abb02f' # str | The file hash to enrich (MD5, SHA-1, or SHA-256).

    try:
        # VirusTotal IoC enrichment for a file hash.
        api_response = api_instance.vector_scan_hash(query)
        print("The response of VectorScanApi->vector_scan_hash:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VectorScanApi->vector_scan_hash: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The file hash to enrich (MD5, SHA-1, or SHA-256). | 

### Return type

[**VectorScanHashResponse**](VectorScanHashResponse.md)

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

# **vector_scan_ip**
> VectorScanIpResponse vector_scan_ip(query)

VirusTotal IoC enrichment for an IPv4 address.

Returns VirusTotal-derived reputation, WHOIS, ASN, and relationship
data for the supplied IPv4 address.


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.vector_scan_ip_response import VectorScanIpResponse
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
    api_instance = crawlsnap.VectorScanApi(api_client)
    query = '8.8.8.8' # str | The IPv4 address to enrich.

    try:
        # VirusTotal IoC enrichment for an IPv4 address.
        api_response = api_instance.vector_scan_ip(query)
        print("The response of VectorScanApi->vector_scan_ip:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VectorScanApi->vector_scan_ip: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The IPv4 address to enrich. | 

### Return type

[**VectorScanIpResponse**](VectorScanIpResponse.md)

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

# **vector_scan_url**
> VectorScanUrlResponse vector_scan_url(query)

VirusTotal IoC enrichment for a URL.

Returns VirusTotal-derived reputation, detections, categories, and
network relationships for the supplied URL.


### Example

* Bearer Authentication (bearerAuth):

```python
import crawlsnap
from crawlsnap.models.vector_scan_url_response import VectorScanUrlResponse
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
    api_instance = crawlsnap.VectorScanApi(api_client)
    query = 'https://example.com' # str | The URL to enrich.

    try:
        # VirusTotal IoC enrichment for a URL.
        api_response = api_instance.vector_scan_url(query)
        print("The response of VectorScanApi->vector_scan_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VectorScanApi->vector_scan_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| The URL to enrich. | 

### Return type

[**VectorScanUrlResponse**](VectorScanUrlResponse.md)

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

