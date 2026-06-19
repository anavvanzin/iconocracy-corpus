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

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.getDiary();

  console.log(data);
})();
```

## updateDiary

- HTTP Method: `PUT`
- Endpoint: `/api/diary`

**Parameters**

| Name          | Type   | Required | Description       |
| :------------ | :----- | :------- | :---------------- |
| body          | any[]  | ✅       | The request body. |
| authorization | string | ✅       |                   |

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.updateDiary([], {
    authorization: 'Bearer {{diarySecret}}',
  });

  console.log(data);
})();
```

## getScoutData

- HTTP Method: `GET`
- Endpoint: `/api/scout`

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.getScoutData();

  console.log(data);
})();
```

## getCorpusStats

- HTTP Method: `GET`
- Endpoint: `/api/corpus/stats`

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.getCorpusStats();

  console.log(data);
})();
```

## getCorpusCountries

- HTTP Method: `GET`
- Endpoint: `/api/corpus/countries`

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.getCorpusCountries();

  console.log(data);
})();
```

## searchCorpusAnalysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis/search`

**Parameters**

| Name   | Type   | Required | Description |
| :----- | :----- | :------- | :---------- |
| attr   | string | ❌       |             |
| figure | string | ❌       |             |

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.searchCorpusAnalysis({
    attr: '{{attr}}',
    figure: '{{figure}}',
  });

  console.log(data);
})();
```

## listCorpusAnalysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis`

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.listCorpusAnalysis();

  console.log(data);
})();
```

## listCorpusItems

- HTTP Method: `GET`
- Endpoint: `/api/corpus`

**Parameters**

| Name    | Type   | Required | Description |
| :------ | :----- | :------- | :---------- |
| country | string | ❌       |             |
| regime  | string | ❌       |             |
| q       | string | ❌       |             |

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.listCorpusItems({
    country: '{{country}}',
    regime: '{{regime}}',
    q: '{{q}}',
  });

  console.log(data);
})();
```

## getCorpusItem

- HTTP Method: `GET`
- Endpoint: `/api/corpus/{itemId}`

**Return Type**

`any`

**Example Usage Code Snippet**

```typescript
import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.implementedApi.getCorpusItem();

  console.log(data);
})();
```
