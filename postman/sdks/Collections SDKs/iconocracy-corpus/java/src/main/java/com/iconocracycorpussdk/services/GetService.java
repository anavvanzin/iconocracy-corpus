package com.iconocracycorpussdk.services;

import com.fasterxml.jackson.core.type.TypeReference;
import com.iconocracycorpussdk.config.IconocracyCorpusSdkConfig;
import com.iconocracycorpussdk.config.RequestConfig;
import com.iconocracycorpussdk.exceptions.ApiError;
import com.iconocracycorpussdk.http.Environment;
import com.iconocracycorpussdk.http.HttpMethod;
import com.iconocracycorpussdk.http.ModelConverter;
import com.iconocracycorpussdk.http.util.RequestBuilder;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import lombok.NonNull;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

/**
 * GetService Service
 */
public class GetService extends BaseService {

  private RequestConfig getDataConfig = RequestConfig.builder()
    .environment(Environment.POSTMAN_ECHO)
    .build();

  /**
   * Constructs a new instance of GetService.
   *
   * @param httpClient The HTTP client to use for requests
   * @param config The SDK configuration
   */
  public GetService(@NonNull OkHttpClient httpClient, IconocracyCorpusSdkConfig config) {
    super(httpClient, config);
  }

  /**
   * Sets method-level configuration for {@code getData}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public GetService setGetDataConfig(RequestConfig config) {
    this.getDataConfig = config;
    return this;
  }

  /**
   * This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).
   *
   * A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.
   *
   * @return response of {@code Object}
   */
  public Object getData() throws ApiError {
    return this.getData(null);
  }

  /**
   * This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).
   *
   * A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.
   *
   * @return response of {@code Object}
   */
  public Object getData(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getDataConfig, requestConfig);
    Request request = this.buildGetDataRequest(resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).
   *
   * A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getDataAsync() throws ApiError {
    return this.getDataAsync(null);
  }

  /**
   * This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).
   *
   * A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getDataAsync(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getDataConfig, requestConfig);
    Request request = this.buildGetDataRequest(resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildGetDataRequest(RequestConfig resolvedConfig) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.POSTMAN_ECHO),
      "get"
    ).build();
  }
}
