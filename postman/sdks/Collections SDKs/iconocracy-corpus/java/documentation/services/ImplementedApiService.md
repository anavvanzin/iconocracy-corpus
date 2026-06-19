# ImplementedApiService

A list of all methods in the `ImplementedApiService` service. Click on the method name to view detailed information about that method.

| Methods                                       | Description |
| :-------------------------------------------- | :---------- |
| [getDiary](#getdiary)                         |             |
| [updateDiary](#updatediary)                   |             |
| [getScoutData](#getscoutdata)                 |             |
| [getCorpusStats](#getcorpusstats)             |             |
| [getCorpusCountries](#getcorpuscountries)     |             |
| [searchCorpusAnalysis](#searchcorpusanalysis) |             |
| [listCorpusAnalysis](#listcorpusanalysis)     |             |
| [listCorpusItems](#listcorpusitems)           |             |
| [getCorpusItem](#getcorpusitem)               |             |

## getDiary

- HTTP Method: `GET`
- Endpoint: `/api/diary`

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    Object response = iconocracyCorpusSdk.implementedApi.getDiary();

    System.out.println(response);
  }
}

```

## updateDiary

- HTTP Method: `PUT`
- Endpoint: `/api/diary`

**Parameters**

| Name              | Type                                                        | Required | Description               |
| :---------------- | :---------------------------------------------------------- | :------- | :------------------------ |
| requestParameters | [UpdateDiaryParameters](../models/UpdateDiaryParameters.md) | ✅       | Request Parameters Object |

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;
import com.iconocracycorpussdk.models.UpdateDiaryParameters;
import java.util.Arrays;
import java.util.List;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    List<Object> requestBodyList = Arrays.asList(new Object());

    UpdateDiaryParameters requestParameters = UpdateDiaryParameters.builder()
      .authorization("Bearer {{diarySecret}}")
      .requestBody(requestBodyList)
      .build();

    Object response = iconocracyCorpusSdk.implementedApi.updateDiary(requestParameters);

    System.out.println(response);
  }
}

```

## getScoutData

- HTTP Method: `GET`
- Endpoint: `/api/scout`

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    Object response = iconocracyCorpusSdk.implementedApi.getScoutData();

    System.out.println(response);
  }
}

```

## getCorpusStats

- HTTP Method: `GET`
- Endpoint: `/api/corpus/stats`

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    Object response = iconocracyCorpusSdk.implementedApi.getCorpusStats();

    System.out.println(response);
  }
}

```

## getCorpusCountries

- HTTP Method: `GET`
- Endpoint: `/api/corpus/countries`

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    Object response = iconocracyCorpusSdk.implementedApi.getCorpusCountries();

    System.out.println(response);
  }
}

```

## searchCorpusAnalysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis/search`

**Parameters**

| Name              | Type                                                                          | Required | Description               |
| :---------------- | :---------------------------------------------------------------------------- | :------- | :------------------------ |
| requestParameters | [SearchCorpusAnalysisParameters](../models/SearchCorpusAnalysisParameters.md) | ❌       | Request Parameters Object |

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;
import com.iconocracycorpussdk.models.SearchCorpusAnalysisParameters;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    SearchCorpusAnalysisParameters requestParameters = SearchCorpusAnalysisParameters.builder()
      .attr("{{attr}}")
      .figure("{{figure}}")
      .build();

    Object response = iconocracyCorpusSdk.implementedApi.searchCorpusAnalysis(requestParameters);

    System.out.println(response);
  }
}

```

## listCorpusAnalysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis`

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    Object response = iconocracyCorpusSdk.implementedApi.listCorpusAnalysis();

    System.out.println(response);
  }
}

```

## listCorpusItems

- HTTP Method: `GET`
- Endpoint: `/api/corpus`

**Parameters**

| Name              | Type                                                                | Required | Description               |
| :---------------- | :------------------------------------------------------------------ | :------- | :------------------------ |
| requestParameters | [ListCorpusItemsParameters](../models/ListCorpusItemsParameters.md) | ❌       | Request Parameters Object |

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;
import com.iconocracycorpussdk.models.ListCorpusItemsParameters;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    ListCorpusItemsParameters requestParameters = ListCorpusItemsParameters.builder()
      .country("{{country}}")
      .regime("{{regime}}")
      .q("{{q}}")
      .build();

    Object response = iconocracyCorpusSdk.implementedApi.listCorpusItems(requestParameters);

    System.out.println(response);
  }
}

```

## getCorpusItem

- HTTP Method: `GET`
- Endpoint: `/api/corpus/{itemId}`

**Return Type**

`Object`

**Example Usage Code Snippet**

```java
import com.iconocracycorpussdk.IconocracyCorpusSdk;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    Object response = iconocracyCorpusSdk.implementedApi.getCorpusItem();

    System.out.println(response);
  }
}

```
