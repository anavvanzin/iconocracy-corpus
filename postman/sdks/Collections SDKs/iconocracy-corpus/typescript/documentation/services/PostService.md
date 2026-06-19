# PostService

A list of all methods in the `PostService` service. Click on the method name to view detailed information about that method.

| Methods               | Description                                                                                                                                                                                                                               |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [postData](#postdata) | This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. A successful POST request typically returns a `200 OK` or `201 Created` response code. |

## postData

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. A successful POST request typically returns a `200 OK` or `201 Created` response code.

- HTTP Method: `POST`
- Endpoint: `/post`

**Parameters**

| Name | Type                                            | Required | Description       |
| :--- | :---------------------------------------------- | :------- | :---------------- |
| body | [PostDataRequest](../models/PostDataRequest.md) | ✅       | The request body. |

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk, PostDataRequest } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const postDataRequest: PostDataRequest = {
    name: 'Add your name in the body',
  };

  const data = await iconocracyCorpusSdk.post.postData(postDataRequest);

  console.log(data);
})();
```
