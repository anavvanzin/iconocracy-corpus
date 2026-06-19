# GetService

A list of all methods in the `GetService` service. Click on the method name to view detailed information about that method.

| Methods               | Description                                                                                                                                                                                                                                                                                                                                                                                 |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [get_data](#get_data) | This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`). A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data. |

## get_data

This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`). A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.

- HTTP Method: `GET`
- Endpoint: `/get`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.get.get_data()

print(result)
```
