package sharedmodels

import (
	"encoding/json"
	"example.com/iconocracy-corpus-sdk/sdk/internal/clients/rest/httptransport"
	"net/http"
)

// IconocracyCorpusSDKResponse is the user-facing wrapper for API responses.
// It contains the deserialized data, raw HTTP response, and metadata like headers and status code.
type IconocracyCorpusSDKResponse[T any] struct {
	Data     T
	Raw      *http.Response
	Metadata IconocracyCorpusSDKResponseMetadata
}

// IconocracyCorpusSDKResponseMetadata contains HTTP metadata from the API response.
// Includes status code and headers for inspection and debugging.
type IconocracyCorpusSDKResponseMetadata struct {
	Headers    map[string]string
	StatusCode int
}

// NewIconocracyCorpusSDKResponse creates a new response wrapper from an internal transport response.
// Extracts data and metadata into a user-facing structure.
func NewIconocracyCorpusSDKResponse[T any](resp *httptransport.Response[T]) *IconocracyCorpusSDKResponse[T] {
	return &IconocracyCorpusSDKResponse[T]{
		Data: resp.Data,
		Raw:  resp.Raw,
		Metadata: IconocracyCorpusSDKResponseMetadata{
			StatusCode: resp.StatusCode,
			Headers:    resp.Headers,
		},
	}
}

// GetData returns the deserialized response data.
func (r *IconocracyCorpusSDKResponse[T]) GetData() T {
	return r.Data
}

// String returns a JSON representation of the response for debugging.
// Returns an error message if JSON marshaling fails.
func (r IconocracyCorpusSDKResponse[T]) String() string {
	jsonData, err := json.MarshalIndent(r, "", "  ")
	if err != nil {
		return "error converting struct: IconocracyCorpusSDKResponse to string"
	}
	return string(jsonData)
}
