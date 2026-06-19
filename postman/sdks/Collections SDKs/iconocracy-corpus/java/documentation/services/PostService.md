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

| Name            | Type                                            | Required | Description  |
| :-------------- | :---------------------------------------------- | :------- | :----------- |
| postDataRequest | [PostDataRequest](../models/PostDataRequest.md) | ✅       | Request Body |

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;
import com.iconocracycorpussdk.models.PostDataRequest;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    PostDataRequest postDataRequest = PostDataRequest.builder()
      .name("Add your name in the body")
      .build();

    Object response = iconocracyCorpusSdk.post.postData(postDataRequest);

    System.out.println(response);
  }
}

```
