# ImplementedApiService

A list of all methods in the `ImplementedApiService` service. Click on the method name to view detailed information about that method.

| Methods                                           | Description |
| :------------------------------------------------ | :---------- |
| [get_diary](#get_diary)                           |             |
| [update_diary](#update_diary)                     |             |
| [get_scout_data](#get_scout_data)                 |             |
| [get_corpus_stats](#get_corpus_stats)             |             |
| [get_corpus_countries](#get_corpus_countries)     |             |
| [search_corpus_analysis](#search_corpus_analysis) |             |
| [list_corpus_analysis](#list_corpus_analysis)     |             |
| [list_corpus_items](#list_corpus_items)           |             |
| [get_corpus_item](#get_corpus_item)               |             |

## get_diary

- HTTP Method: `GET`
- Endpoint: `/api/diary`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.get_diary()

print(result)
```

## update_diary

- HTTP Method: `PUT`
- Endpoint: `/api/diary`

**Parameters**

| Name          | Type      | Required | Description       |
| :------------ | :-------- | :------- | :---------------- |
| request_body  | List[Any] | ✅       | The request body. |
| authorization | str       | ✅       |                   |

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

request_body = [
    ""
]

result = sdk.implemented_api.update_diary(
    request_body=request_body,
    authorization="Bearer {{diarySecret}}"
)

print(result)
```

## get_scout_data

- HTTP Method: `GET`
- Endpoint: `/api/scout`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.get_scout_data()

print(result)
```

## get_corpus_stats

- HTTP Method: `GET`
- Endpoint: `/api/corpus/stats`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.get_corpus_stats()

print(result)
```

## get_corpus_countries

- HTTP Method: `GET`
- Endpoint: `/api/corpus/countries`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.get_corpus_countries()

print(result)
```

## search_corpus_analysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis/search`

**Parameters**

| Name   | Type | Required | Description |
| :----- | :--- | :------- | :---------- |
| attr   | str  | ❌       |             |
| figure | str  | ❌       |             |

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.search_corpus_analysis(
    attr="{{attr}}",
    figure="{{figure}}"
)

print(result)
```

## list_corpus_analysis

- HTTP Method: `GET`
- Endpoint: `/api/corpus/analysis`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.list_corpus_analysis()

print(result)
```

## list_corpus_items

- HTTP Method: `GET`
- Endpoint: `/api/corpus`

**Parameters**

| Name    | Type | Required | Description |
| :------ | :--- | :------- | :---------- |
| country | str  | ❌       |             |
| regime  | str  | ❌       |             |
| q       | str  | ❌       |             |

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.list_corpus_items(
    country="{{country}}",
    regime="{{regime}}",
    q="{{q}}"
)

print(result)
```

## get_corpus_item

- HTTP Method: `GET`
- Endpoint: `/api/corpus/{itemId}`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.implemented_api.get_corpus_item()

print(result)
```
