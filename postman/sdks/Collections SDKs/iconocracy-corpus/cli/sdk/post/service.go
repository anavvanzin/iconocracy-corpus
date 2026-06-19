package post

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

// Service provides methods to interact with Post-related API endpoints.
// It uses a configuration manager for settings and supports custom hooks for request/response interception.
type Service struct {
	manager        *configmanager.ConfigManager
	hook           hooks.Hook
	postDataConfig []iconocracycorpussdkconfig.RequestOption
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
	return api.manager.GetPost()
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

// SetPostDataConfig sets method-level configuration for PostData.
// Options are applied to every future call to PostData and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetPostDataConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.postDataConfig = opts
	return api
}

// This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.
//
// A successful POST request typically returns a `200 OK` or `201 Created` response code.
func (api *Service) PostData(ctx context.Context, postDataRequest PostDataRequest, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.postDataConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("POST").
		WithPath("/post").
		WithConfig(config).
		WithBody(postDataRequest).
		AddHeader("CONTENT-TYPE", "application/json").
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
