package implementedapi

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

// Service provides methods to interact with ImplementedAPI-related API endpoints.
// It uses a configuration manager for settings and supports custom hooks for request/response interception.
type Service struct {
	manager                    *configmanager.ConfigManager
	hook                       hooks.Hook
	getDiaryConfig             []iconocracycorpussdkconfig.RequestOption
	updateDiaryConfig          []iconocracycorpussdkconfig.RequestOption
	getScoutDataConfig         []iconocracycorpussdkconfig.RequestOption
	getCorpusStatsConfig       []iconocracycorpussdkconfig.RequestOption
	getCorpusCountriesConfig   []iconocracycorpussdkconfig.RequestOption
	searchCorpusAnalysisConfig []iconocracycorpussdkconfig.RequestOption
	listCorpusAnalysisConfig   []iconocracycorpussdkconfig.RequestOption
	listCorpusItemsConfig      []iconocracycorpussdkconfig.RequestOption
	getCorpusItemConfig        []iconocracycorpussdkconfig.RequestOption
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
	return api.manager.GetImplementedAPI()
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

// SetGetDiaryConfig sets method-level configuration for GetDiary.
// Options are applied to every future call to GetDiary and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetGetDiaryConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.getDiaryConfig = opts
	return api
}

// SetUpdateDiaryConfig sets method-level configuration for UpdateDiary.
// Options are applied to every future call to UpdateDiary and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetUpdateDiaryConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.updateDiaryConfig = opts
	return api
}

// SetGetScoutDataConfig sets method-level configuration for GetScoutData.
// Options are applied to every future call to GetScoutData and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetGetScoutDataConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.getScoutDataConfig = opts
	return api
}

// SetGetCorpusStatsConfig sets method-level configuration for GetCorpusStats.
// Options are applied to every future call to GetCorpusStats and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetGetCorpusStatsConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.getCorpusStatsConfig = opts
	return api
}

// SetGetCorpusCountriesConfig sets method-level configuration for GetCorpusCountries.
// Options are applied to every future call to GetCorpusCountries and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetGetCorpusCountriesConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.getCorpusCountriesConfig = opts
	return api
}

// SetSearchCorpusAnalysisConfig sets method-level configuration for SearchCorpusAnalysis.
// Options are applied to every future call to SearchCorpusAnalysis and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetSearchCorpusAnalysisConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.searchCorpusAnalysisConfig = opts
	return api
}

// SetListCorpusAnalysisConfig sets method-level configuration for ListCorpusAnalysis.
// Options are applied to every future call to ListCorpusAnalysis and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetListCorpusAnalysisConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.listCorpusAnalysisConfig = opts
	return api
}

// SetListCorpusItemsConfig sets method-level configuration for ListCorpusItems.
// Options are applied to every future call to ListCorpusItems and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetListCorpusItemsConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.listCorpusItemsConfig = opts
	return api
}

// SetGetCorpusItemConfig sets method-level configuration for GetCorpusItem.
// Options are applied to every future call to GetCorpusItem and take
// precedence over service-level config. Per-call options still take highest precedence.
func (api *Service) SetGetCorpusItemConfig(opts ...iconocracycorpussdkconfig.RequestOption) *Service {
	api.getCorpusItemConfig = opts
	return api
}

func (api *Service) GetDiary(ctx context.Context, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.getDiaryConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/diary").
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

func (api *Service) UpdateDiary(ctx context.Context, params UpdateDiaryRequestParams, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.updateDiaryConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("PUT").
		WithPath("/api/diary").
		WithConfig(config).
		AddHeader("CONTENT-TYPE", "application/json").
		WithOptions(params).
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

func (api *Service) GetScoutData(ctx context.Context, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.getScoutDataConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/scout").
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

func (api *Service) GetCorpusStats(ctx context.Context, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.getCorpusStatsConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/corpus/stats").
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

func (api *Service) GetCorpusCountries(ctx context.Context, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.getCorpusCountriesConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/corpus/countries").
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

func (api *Service) SearchCorpusAnalysis(ctx context.Context, params SearchCorpusAnalysisRequestParams, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.searchCorpusAnalysisConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/corpus/analysis/search").
		WithConfig(config).
		WithOptions(params).
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

func (api *Service) ListCorpusAnalysis(ctx context.Context, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.listCorpusAnalysisConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/corpus/analysis").
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

func (api *Service) ListCorpusItems(ctx context.Context, params ListCorpusItemsRequestParams, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.listCorpusItemsConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/corpus").
		WithConfig(config).
		WithOptions(params).
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

func (api *Service) GetCorpusItem(ctx context.Context, opts ...iconocracycorpussdkconfig.RequestOption) ([]byte, error) {
	config := *api.config()
	for _, opt := range api.getCorpusItemConfig {
		opt(&config)
	}
	for _, opt := range opts {
		opt(&config)
	}

	httpRequest := httptransport.NewRequestBuilder().WithContext(ctx).
		WithMethod("GET").
		WithPath("/api/corpus/{itemId}").
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
