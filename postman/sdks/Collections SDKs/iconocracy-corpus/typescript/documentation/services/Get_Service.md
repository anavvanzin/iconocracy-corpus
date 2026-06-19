# Get_Service

A list of all methods in the `Get_Service` service. Click on the method name to view detailed information about that method.

| Methods             | Description                                                                                                                                                                                                                                                                                                                                                                                 |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [getData](#getdata) | This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`). A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data. |

## getData

This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`). A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.

- HTTP Method: `GET`
- Endpoint: `/get`

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.get_.getData();

  console.log(data);
})();
```
