package configmanager

import (
	"example.com/iconocracy-corpus-sdk/sdk/iconocracycorpussdkconfig"
	"time"
)

// ConfigManager manages configuration across all services with synchronized updates.
// Provides centralized configuration management and OAuth token handling for multiple services.
type ConfigManager struct {
	get            iconocracycorpussdkconfig.Config
	implementedAPI iconocracycorpussdkconfig.Config
	post           iconocracycorpussdkconfig.Config
}

// NewConfigManager creates a new configuration manager with the provided config and optional OAuth token service.
// Initializes service-specific configs and sets up OAuth token management if enabled.
func NewConfigManager(config iconocracycorpussdkconfig.Config) *ConfigManager {
	return &ConfigManager{
		get:            config,
		implementedAPI: config,
		post:           config,
	}
}

// SetBaseURL updates the BaseURL configuration parameter across all services.
// Changes are applied synchronously to all registered service configurations.
func (c *ConfigManager) SetBaseURL(baseURL string) {
	c.get.SetBaseURL(baseURL)
	c.implementedAPI.SetBaseURL(baseURL)
	c.post.SetBaseURL(baseURL)
}

// SetTimeout updates the Timeout configuration parameter across all services.
// Changes are applied synchronously to all registered service configurations.
func (c *ConfigManager) SetTimeout(timeout time.Duration) {
	c.get.SetTimeout(timeout)
	c.implementedAPI.SetTimeout(timeout)
	c.post.SetTimeout(timeout)
}

// SetRetryConfig updates the retry configuration across all services.
// Changes are applied synchronously to all registered service configurations.
func (c *ConfigManager) SetRetryConfig(retry iconocracycorpussdkconfig.RetryConfig) {
	c.get.SetRetryConfig(retry)
	c.implementedAPI.SetRetryConfig(retry)
	c.post.SetRetryConfig(retry)
}

// GetGet returns the configuration for the Get service.
// Returns a pointer to the service-specific config for use in API calls.
func (c *ConfigManager) GetGet() *iconocracycorpussdkconfig.Config {
	return &c.get
}

// GetImplementedAPI returns the configuration for the ImplementedAPI service.
// Returns a pointer to the service-specific config for use in API calls.
func (c *ConfigManager) GetImplementedAPI() *iconocracycorpussdkconfig.Config {
	return &c.implementedAPI
}

// GetPost returns the configuration for the Post service.
// Returns a pointer to the service-specific config for use in API calls.
func (c *ConfigManager) GetPost() *iconocracycorpussdkconfig.Config {
	return &c.post
}

// GetBaseURL returns the currently configured base URL.
// All services share the same base URL; this reads it from the first service's config.
func (c *ConfigManager) GetBaseURL() string {
	return c.get.BaseURL
}
