# ImplementedAPI

A list of all methods in the `ImplementedAPI` service. Click on the method name to view detailed information about that method.

| Methods                                       | Description |
| :-------------------------------------------- | :---------- |
| [GetDiary](#getdiary)                         |             |
| [UpdateDiary](#updatediary)                   |             |
| [GetScoutData](#getscoutdata)                 |             |
| [GetCorpusStats](#getcorpusstats)             |             |
| [GetCorpusCountries](#getcorpuscountries)     |             |
| [SearchCorpusAnalysis](#searchcorpusanalysis) |             |
| [ListCorpusAnalysis](#listcorpusanalysis)     |             |
| [ListCorpusItems](#listcorpusitems)           |             |
| [GetCorpusItem](#getcorpusitem)               |             |

## GetDiary

- HTTP Method: `GET`
- Endpoint: `/api/diary`

**Parameters**

| Name | Type    | Required | Description                 |
| :--- | :------ | :------- | :-------------------------- |
| ctx  | Context | ✅       | Default go language context |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## UpdateDiary

- HTTP Method: `PUT`
- Endpoint: `/api/diary`

**Parameters**

| Name   | Type                     | Required | Description                   |
| :----- | :----------------------- | :------- | :---------------------------- |
| ctx    | Context                  | ✅       | Default go language context   |
| body   | []byte                   | ✅       |                               |
| params | UpdateDiaryRequestParams | ✅       | Additional request parameters |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## GetScoutData

- HTTP Method: `GET`
- Endpoint: `/api/scout`

**Parameters**

| Name | Type    | Required | Description                 |
| :--- | :------ | :------- | :-------------------------- |
| ctx  | Context | ✅       | Default go language context |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## GetCorpusStats

- HTTP Method: `GET`
- Endpoint: `/api/corpus/stats`

**Parameters**

| Name | Type    | Required | Description                 |
| :--- | :------ | :------- | :-------------------------- |
| ctx  | Context | ✅       | Default go language context |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## GetCorpusCountries

- HTTP Method: `GET`
- Endpoint: `/api/corpus/countries`

**Parameters**

| Name | Type    | Required | Description                 |
| :--- | :------ | :------- | :-------------------------- |
| ctx  | Context | ✅       | Default go language context |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## SearchCorpusAnalysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis/search`

**Parameters**

| Name   | Type                              | Required | Description                   |
| :----- | :-------------------------------- | :------- | :---------------------------- |
| ctx    | Context                           | ✅       | Default go language context   |
| params | SearchCorpusAnalysisRequestParams | ✅       | Additional request parameters |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## ListCorpusAnalysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis`

**Parameters**

| Name | Type    | Required | Description                 |
| :--- | :------ | :------- | :-------------------------- |
| ctx  | Context | ✅       | Default go language context |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## ListCorpusItems

- HTTP Method: `GET`
- Endpoint: `/api/corpus`

**Parameters**

| Name   | Type                         | Required | Description                   |
| :----- | :--------------------------- | :------- | :---------------------------- |
| ctx    | Context                      | ✅       | Default go language context   |
| params | ListCorpusItemsRequestParams | ✅       | Additional request parameters |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```

## GetCorpusItem

- HTTP Method: `GET`
- Endpoint: `/api/corpus/{itemId}`

**Parameters**

| Name | Type    | Required | Description                 |
| :--- | :------ | :------- | :-------------------------- |
| ctx  | Context | ✅       | Default go language context |

**Return Type**

`[]byte`

**Example Usage Code Snippet**

```go

```
