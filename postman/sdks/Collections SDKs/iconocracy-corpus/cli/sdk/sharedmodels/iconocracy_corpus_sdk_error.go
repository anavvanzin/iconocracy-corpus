package sharedmodels

import (
	"example.com/iconocracy-corpus-sdk/sdk/internal/clients/rest/httptransport"
	"net/http"
)

// IconocracyCorpusSDKError wraps API errors with detailed metadata including status code, headers, and raw response.
// It implements the error interface and provides structured access to error information.
type IconocracyCorpusSDKError[T any] struct {
	Err      error
	Data     *T
	Body     []byte
	Raw      *http.Response
	Metadata IconocracyCorpusSDKErrorMetadata
}

// IconocracyCorpusSDKErrorMetadata contains HTTP metadata associated with an error response.
type IconocracyCorpusSDKErrorMetadata struct {
	Headers    map[string]string
	StatusCode int
}

// NewIconocracyCorpusSDKError creates a new IconocracyCorpusSDKError from an internal transport error.
// It extracts error details, body, status code, and headers into a user-facing error structure.
func NewIconocracyCorpusSDKError[T any](transportError *httptransport.ErrorResponse[T]) *IconocracyCorpusSDKError[T] {
	return &IconocracyCorpusSDKError[T]{
		Err:  transportError.GetError(),
		Data: transportError.Data,
		Body: transportError.GetBody(),
		Raw:  transportError.Raw,
		Metadata: IconocracyCorpusSDKErrorMetadata{
			StatusCode: transportError.GetStatusCode(),
			Headers:    transportError.GetHeaders(),
		},
	}
}

// Error implements the error interface, returning the error message string.
func (e *IconocracyCorpusSDKError[T]) Error() string {
	if e == nil || e.Err == nil {
		return ""
	}
	return e.Err.Error()
}

// Unwrap returns the underlying error, enabling errors.Is and errors.As to traverse the chain.
func (e *IconocracyCorpusSDKError[T]) Unwrap() error {
	return e.Err
}

// GetData returns the deserialized error response data.
// Returns nil if unmarshaling failed or the response body was empty.
func (e *IconocracyCorpusSDKError[T]) GetData() *T {
	return e.Data
}
