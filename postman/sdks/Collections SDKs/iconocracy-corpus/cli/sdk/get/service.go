package get

import (
	"context"
	"example.com/iconocracy-corpus-sdk/sdk/iconocracycorpussdkconfig"
	restClient "example.com/iconocracy-corpus-sdk/sdk/internal/clients/rest"
	"example.com/iconocracy-corpus-sdk/sdk/internal/clients/rest/hooks"
	"example.com/iconocracy-corpus-sdk/sdk/internal/clients/rest/httptransport"
	"example.com/iconocracy-corpus-sdk/sdk/internal/configmanager"
	"example.com/iconocracy-corpus-sdk/sdk/sharedmodels"
	"time"
)

// Service provides methods to interact with Get-related API endpoints.
// It uses a configuration manager for settings and supports custom hooks for request/response interception.
type Service struct {
	manager       *configmanager.ConfigManager
	hook          hooks.Hook
	getDataConfig []iconocracycorpussdkconfig.RequestOption
}

func NewService() *Service {
	return &Service{
		manager: configmanager.NewConfigManager(iconocracycorpussdkconfig.Config{}),
	}
}

// WithConfigManager sets the configuration manager for this service.
// Returns the service instance for method chaining.
func (api *Service) WithConfigManager(manager *configmanager.ConfigManager) *Service {
	api.manager = manager
	return api
}

// WithHook sets a custom hook for request/response interception.
// Returns the service instance for method chaining.
func (api *Service) WithHook(hook hooks.Hook) *Service {
	api.hook = hook
	return api
}

func (api *Service) config() *iconocracycorpussdkconfig.Config {
	return api.manager.GetGet()
}

func (api *Service) getHook() hooks.Hook {
	return api.hook
}

func (api *Service) SetBaseURL(baseURL string) {
	config := api.config()
	config.SetBaseURL(baseURL)
}

func (api *Service) SetTimeout(timeout time.Duration) {
	config := api.config()
	config.SetTimeout(timeout)
}

// SetGetDataConfig sets method-level configuration for GetData.
// Options are applied to every future call to GetData and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetGetDataConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.getDataConfig = opts
	return api
}

// This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).
//
// A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.
func (api *Service) GetData(ctx context.Context, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.getDataConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/get").
		WithConfig(config).
		WithContentType(httptransport.ContentTypeJSON).
		WithResponseContentType(httptransport.ContentTypeJSON).
		Build()

	httpClient := restClient.NewRestClient[[]byte, []byte](config, api.getHook())
	resp, err := httpClient.Call(*httpRequest)
	if err != nil {
		return nil, sharedmodels.NewIconocracyCorpusSDKError[[]byte](err)
	}

	return resp.Data, nil
}
