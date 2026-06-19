# Post

A list of all methods in the `Post` service. Click on the method name to view detailed information about that method.

| Methods               | Description                                                                                                                                                                                                                               |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [PostData](#postdata) | This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. A successful POST request typically returns a `200 OK` or `201 Created` response code. |

## PostData

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. A successful POST request typically returns a `200 OK` or `201 Created` response code.

- HTTP Method: `POST`
- Endpoint: `/post`

**Parameters**

| Name            | Type            | Required | Description                 |
| :-------------- | :-------------- | :------- | :-------------------------- |
| ctx             | Context         | ✅       | Default go language context |
| postDataRequest | PostDataRequest | ✅       |                             |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```
