package com.iconocracycorpussdk;

import com.iconocracycorpussdk.config.IconocracyCorpusSdkConfig;
import com.iconocracycorpussdk.http.Environment;
import com.iconocracycorpussdk.http.interceptors.DefaultHeadersInterceptor;
import com.iconocracycorpussdk.http.interceptors.RetryInterceptor;
import com.iconocracycorpussdk.services.GetService;
import com.iconocracycorpussdk.services.ImplementedApiService;
import com.iconocracycorpussdk.services.PostService;
import java.util.concurrent.TimeUnit;
import okhttp3.OkHttpClient;

/**
 * Main SDK client class for IconocracyCorpusSdk.
 * Provides centralized access to all service endpoints with configurable authentication,
 * environment management, hooks, and HTTP client settings.
 */
public class IconocracyCorpusSdk {

  public final GetService get;
  public final ImplementedApiService implementedApi;
  public final PostService post;

  private final IconocracyCorpusSdkConfig config;

  /**
   * Constructs a new instance of IconocracyCorpusSdk with default configuration.
   */
  public IconocracyCorpusSdk() {
    // Default configs
    this(IconocracyCorpusSdkConfig.builder().build());
  }

  /**
   * Constructs a new instance of IconocracyCorpusSdk with custom configuration.
   * Initializes all services, HTTP client, and optional OAuth token manager.
   *
   * @param config The SDK configuration including base URL, authentication, timeout, and retry settings
   */
  public IconocracyCorpusSdk(IconocracyCorpusSdkConfig config) {
    this.config = config;

    final OkHttpClient httpClient = new OkHttpClient.Builder()
      .addInterceptor(new DefaultHeadersInterceptor(config))
      .addInterceptor(new RetryInterceptor(config.getRetryConfig()))
      .readTimeout(config.getTimeout(), TimeUnit.MILLISECONDS)
      .build();

    this.get = new GetService(httpClient, config);
    this.implementedApi = new ImplementedApiService(httpClient, config);
    this.post = new PostService(httpClient, config);
  }

  /**
   * Sets the environment for all API requests.
   *
   * @param environment The environment to use (e.g., DEFAULT, PRODUCTION, STAGING)
   */
  public void setEnvironment(Environment environment) {
    setBaseUrl(environment.getUrl());
  }

  /**
   * Sets the base URL for all API requests.
   *
   * @param baseUrl The base URL to use for API requests
   */
  public void setBaseUrl(String baseUrl) {
    this.config.setBaseUrl(baseUrl);
  }
}
// c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
