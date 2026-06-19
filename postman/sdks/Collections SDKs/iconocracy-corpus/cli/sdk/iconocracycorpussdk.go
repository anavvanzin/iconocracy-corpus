package iconocracycorpussdk

import (
	"example.com/iconocracy-corpus-sdk/sdk/get"
	"example.com/iconocracy-corpus-sdk/sdk/implementedapi"
	"example.com/iconocracy-corpus-sdk/sdk/internal/clients/rest/hooks"
	"example.com/iconocracy-corpus-sdk/sdk/internal/configmanager"
	"example.com/iconocracy-corpus-sdk/sdk/post"
	"time"
)

// IconocracyCorpusSDK is the main SDK client that provides access to all service endpoints.
// It manages configuration, authentication, and service instances with centralized settings.
type IconocracyCorpusSDK struct {
	Get            *get.Service
	ImplementedAPI *implementedapi.Service
	Post           *post.Service
	manager        *configmanager.ConfigManager
}

func NewIconocracyCorpusSDK(config Config) *IconocracyCorpusSDK {
	get := get.NewService()
	implementedAPI := implementedapi.NewService()
	post := post.NewService()

	manager := configmanager.NewConfigManager(config)
	hook := hooks.NewDefaultHook()
	get.WithConfigManager(manager)
	implementedAPI.WithConfigManager(manager)
	post.WithConfigManager(manager)
	get.WithHook(hook)
	implementedAPI.WithHook(hook)
	post.WithHook(hook)

	return &IconocracyCorpusSDK{
		Get:            get,
		ImplementedAPI: implementedAPI,
		Post:           post,
		manager:        manager,
	}
}

func (i *IconocracyCorpusSDK) SetBaseURL(baseURL string) {
	i.manager.SetBaseURL(baseURL)
}

func (i *IconocracyCorpusSDK) SetTimeout(timeout time.Duration) {
	i.manager.SetTimeout(timeout)
}

// SetEnvironment configures the SDK to use the specified environment's base URL.
func (i *IconocracyCorpusSDK) SetEnvironment(environment Environment) {
	i.manager.SetBaseURL(string(environment))
}

// c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
