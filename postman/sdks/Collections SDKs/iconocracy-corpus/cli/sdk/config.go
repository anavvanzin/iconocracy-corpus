package iconocracycorpussdk

import (
	"example.com/iconocracy-corpus-sdk/sdk/iconocracycorpussdkconfig"
	"example.com/iconocracy-corpus-sdk/sdk/param"
)

// The type aliases below let consumers use a single import path for the entire SDK.
// Internally the concrete types live in iconocracycorpussdkconfig and param.

// Config holds all configuration parameters for the SDK client.
type Config = iconocracycorpussdkconfig.Config

// RequestOption is a function that configures a single request.
type RequestOption = iconocracycorpussdkconfig.RequestOption

// Environment defines the available API base URLs.
type Environment = iconocracycorpussdkconfig.Environment

// RetryConfig holds all runtime-configurable retry parameters.
type RetryConfig = iconocracycorpussdkconfig.RetryConfig

// NewConfig creates a Config with spec-derived defaults.
var NewConfig = iconocracycorpussdkconfig.NewConfig

// NewRetryConfig returns a RetryConfig initialized with spec-derived defaults.
var NewRetryConfig = iconocracycorpussdkconfig.NewRetryConfig

// WithBaseURL returns a RequestOption that overrides BaseURL for a single request.
var WithBaseURL = iconocracycorpussdkconfig.WithBaseURL

// WithTimeout returns a RequestOption that overrides Timeout for a single request.
var WithTimeout = iconocracycorpussdkconfig.WithTimeout

// WithRetryConfig returns a RequestOption that overrides the RetryConfig for a single request.
var WithRetryConfig = iconocracycorpussdkconfig.WithRetryConfig

// Nullable returns a *param.Nullable[T] set to v — use for nullable fields with a value.
func Nullable[T any](v T) *param.Nullable[T] { return &param.Nullable[T]{Value: v} }

// Null returns a *param.Nullable[T] with IsNull set to true, signalling an explicit JSON null.
func Null[T any]() *param.Nullable[T] { return param.Null[T]() }

// Ptr returns a pointer to v — use when no type-specific helper exists.
func Ptr[T any](v T) *T { return param.Ptr(v) }

// Environment constants for the available API base URLs.
const (
	DefaultEnvironment       Environment = iconocracycorpussdkconfig.DefaultEnvironment
	PostmanEchoEnvironment   Environment = iconocracycorpussdkconfig.PostmanEchoEnvironment
	Localhost8787Environment Environment = iconocracycorpussdkconfig.Localhost8787Environment
)
