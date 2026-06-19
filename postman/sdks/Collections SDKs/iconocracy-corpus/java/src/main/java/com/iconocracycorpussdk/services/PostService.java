package com.iconocracycorpussdk.services;

import com.fasterxml.jackson.core.type.TypeReference;
import com.iconocracycorpussdk.config.IconocracyCorpusSdkConfig;
import com.iconocracycorpussdk.config.RequestConfig;
import com.iconocracycorpussdk.exceptions.ApiError;
import com.iconocracycorpussdk.http.Environment;
import com.iconocracycorpussdk.http.HttpMethod;
import com.iconocracycorpussdk.http.ModelConverter;
import com.iconocracycorpussdk.http.util.RequestBuilder;
import com.iconocracycorpussdk.models.PostDataRequest;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import lombok.NonNull;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

/**
 * PostService Service
 */
public class PostService extends BaseService {

  private RequestConfig postDataConfig = RequestConfig.builder()
    .environment(Environment.POSTMAN_ECHO)
    .build();

  /**
   * Constructs a new instance of PostService.
   *
   * @param httpClient The HTTP client to use for requests
   * @param config The SDK configuration
   */
  public PostService(@NonNull OkHttpClient httpClient, IconocracyCorpusSdkConfig config) {
    super(httpClient, config);
  }

  /**
   * Sets method-level configuration for {@code postData}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public PostService setPostDataConfig(RequestConfig config) {
    this.postDataConfig = config;
    return this;
  }

  /**
   * This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.
   *
   * A successful POST request typically returns a `200 OK` or `201 Created` response code.
   *
   * @param postDataRequest {@link PostDataRequest} Request Body
   * @return response of {@code Object}
   */
  public Object postData(@NonNull PostDataRequest postDataRequest) throws ApiError {
    return this.postData(postDataRequest, null);
  }

  /**
   * This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.
   *
   * A successful POST request typically returns a `200 OK` or `201 Created` response code.
   *
   * @param postDataRequest {@link PostDataRequest} Request Body
   * @return response of {@code Object}
   */
  public Object postData(@NonNull PostDataRequest postDataRequest, RequestConfig requestConfig)
    throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.postDataConfig, requestConfig);
    Request request = this.buildPostDataRequest(postDataRequest, resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.
   *
   * A successful POST request typically returns a `200 OK` or `201 Created` response code.
   *
   * @param postDataRequest {@link PostDataRequest} Request Body
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> postDataAsync(@NonNull PostDataRequest postDataRequest)
    throws ApiError {
    return this.postDataAsync(postDataRequest, null);
  }

  /**
   * This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.
   *
   * A successful POST request typically returns a `200 OK` or `201 Created` response code.
   *
   * @param postDataRequest {@link PostDataRequest} Request Body
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> postDataAsync(
    @NonNull PostDataRequest postDataRequest,
    RequestConfig requestConfig
  ) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.postDataConfig, requestConfig);
    Request request = this.buildPostDataRequest(postDataRequest, resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildPostDataRequest(
    @NonNull PostDataRequest postDataRequest,
    RequestConfig resolvedConfig
  ) {
    return new RequestBuilder(
      HttpMethod.POST,
      resolveBaseUrl(resolvedConfig, Environment.POSTMAN_ECHO),
      "post"
    )
      .setJsonContent(postDataRequest)
      .build();
  }
}
