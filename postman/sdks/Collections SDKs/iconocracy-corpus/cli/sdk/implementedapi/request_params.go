package implementedapi

import (
	"example.com/iconocracy-corpus-sdk/sdk/param"
)

// UpdateDiaryRequestParams holds the optional parameters for the API request.
type UpdateDiaryRequestParams struct {
	Authorization *param.Nullable[string] `explode:"false" serializationStyle:"simple" headerParam:"Authorization" required:"true"`
}

// SearchCorpusAnalysisRequestParams holds the optional parameters for the API request.
type SearchCorpusAnalysisRequestParams struct {
	Attr   *param.Nullable[string] `explode:"true" serializationStyle:"form" queryParam:"attr"`
	Figure *param.Nullable[string] `explode:"true" serializationStyle:"form" queryParam:"figure"`
}

// ListCorpusItemsRequestParams holds the optional parameters for the API request.
type ListCorpusItemsRequestParams struct {
	Country *param.Nullable[string] `explode:"true" serializationStyle:"form" queryParam:"country"`
	Regime  *param.Nullable[string] `explode:"true" serializationStyle:"form" queryParam:"regime"`
	Q       *param.Nullable[string] `explode:"true" serializationStyle:"form" queryParam:"q"`
}
