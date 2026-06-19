# PostService

A list of all methods in the `PostService` service. Click on the method name to view detailed information about that method.

| Methods                 | Description                                                                                                                                                                                                                               |
| :---------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [post_data](#post_data) | This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. A successful POST request typically returns a `200 OK` or `201 Created` response code. |

## post_data

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. A successful POST request typically returns a `200 OK` or `201 Created` response code.

- HTTP Method: `POST`
- Endpoint: `/post`

**Parameters**

| Name         | Type                                            | Required | Description       |
| :----------- | :---------------------------------------------- | :------- | :---------------- |
| request_body | [PostDataRequest](../models/PostDataRequest.md) | ✅       | The request body. |

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment
from iconocracy_corpus_sdk.models import PostDataRequest

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

request_body = PostDataRequest(
    name="Add your name in the body"
)

result = sdk.post.post_data(request_body=request_body)

print(result)
```
