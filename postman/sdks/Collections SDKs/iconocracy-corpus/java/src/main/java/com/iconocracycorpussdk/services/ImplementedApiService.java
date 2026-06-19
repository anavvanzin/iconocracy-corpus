package com.iconocracycorpussdk.services;

import com.fasterxml.jackson.core.type.TypeReference;
import com.iconocracycorpussdk.config.IconocracyCorpusSdkConfig;
import com.iconocracycorpussdk.config.RequestConfig;
import com.iconocracycorpussdk.exceptions.ApiError;
import com.iconocracycorpussdk.http.Environment;
import com.iconocracycorpussdk.http.HttpMethod;
import com.iconocracycorpussdk.http.ModelConverter;
import com.iconocracycorpussdk.http.util.RequestBuilder;
import com.iconocracycorpussdk.models.ListCorpusItemsParameters;
import com.iconocracycorpussdk.models.SearchCorpusAnalysisParameters;
import com.iconocracycorpussdk.models.UpdateDiaryParameters;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import lombok.NonNull;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

/**
 * ImplementedApiService Service
 */
public class ImplementedApiService extends BaseService {

  private RequestConfig getDiaryConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig updateDiaryConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig getScoutDataConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig getCorpusStatsConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig getCorpusCountriesConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig searchCorpusAnalysisConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig listCorpusAnalysisConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig listCorpusItemsConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();
  private RequestConfig getCorpusItemConfig = RequestConfig.builder()
    .environment(Environment.LOCALHOST8787)
    .build();

  /**
   * Constructs a new instance of ImplementedApiService.
   *
   * @param httpClient The HTTP client to use for requests
   * @param config The SDK configuration
   */
  public ImplementedApiService(@NonNull OkHttpClient httpClient, IconocracyCorpusSdkConfig config) {
    super(httpClient, config);
  }

  /**
   * Sets method-level configuration for {@code getDiary}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setGetDiaryConfig(RequestConfig config) {
    this.getDiaryConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code updateDiary}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setUpdateDiaryConfig(RequestConfig config) {
    this.updateDiaryConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code getScoutData}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setGetScoutDataConfig(RequestConfig config) {
    this.getScoutDataConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code getCorpusStats}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setGetCorpusStatsConfig(RequestConfig config) {
    this.getCorpusStatsConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code getCorpusCountries}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setGetCorpusCountriesConfig(RequestConfig config) {
    this.getCorpusCountriesConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code searchCorpusAnalysis}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setSearchCorpusAnalysisConfig(RequestConfig config) {
    this.searchCorpusAnalysisConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code listCorpusAnalysis}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setListCorpusAnalysisConfig(RequestConfig config) {
    this.listCorpusAnalysisConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code listCorpusItems}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setListCorpusItemsConfig(RequestConfig config) {
    this.listCorpusItemsConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for {@code getCorpusItem}.
   * Method-level overrides take precedence over service-level configuration but are
   * overridden by request-level configurations.
   *
   * @param config The configuration overrides to apply at the method level
   * @return This service instance for method chaining
   */
  public ImplementedApiService setGetCorpusItemConfig(RequestConfig config) {
    this.getCorpusItemConfig = config;
    return this;
  }

  /**
   * Method getDiary
   * GET /api/diary
   *
   * @return response of {@code Object}
   */
  public Object getDiary() throws ApiError {
    return this.getDiary(null);
  }

  /**
   * Method getDiary
   * GET /api/diary
   *
   * @return response of {@code Object}
   */
  public Object getDiary(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getDiaryConfig, requestConfig);
    Request request = this.buildGetDiaryRequest(resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method getDiary
   * GET /api/diary
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getDiaryAsync() throws ApiError {
    return this.getDiaryAsync(null);
  }

  /**
   * Method getDiary
   * GET /api/diary
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getDiaryAsync(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getDiaryConfig, requestConfig);
    Request request = this.buildGetDiaryRequest(resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildGetDiaryRequest(RequestConfig resolvedConfig) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/diary"
    ).build();
  }

  /**
   * Method updateDiary
   * PUT /api/diary
   *
   * @param requestParameters {@link UpdateDiaryParameters} Request Parameters Object
   * @return response of {@code Object}
   */
  public Object updateDiary(@NonNull UpdateDiaryParameters requestParameters) throws ApiError {
    return this.updateDiary(requestParameters, null);
  }

  /**
   * Method updateDiary
   * PUT /api/diary
   *
   * @param requestParameters {@link UpdateDiaryParameters} Request Parameters Object
   * @return response of {@code Object}
   */
  public Object updateDiary(
    @NonNull UpdateDiaryParameters requestParameters,
    RequestConfig requestConfig
  ) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.updateDiaryConfig, requestConfig);
    Request request = this.buildUpdateDiaryRequest(requestParameters, resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method updateDiary
   * PUT /api/diary
   *
   * @param requestParameters {@link UpdateDiaryParameters} Request Parameters Object
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> updateDiaryAsync(
    @NonNull UpdateDiaryParameters requestParameters
  ) throws ApiError {
    return this.updateDiaryAsync(requestParameters, null);
  }

  /**
   * Method updateDiary
   * PUT /api/diary
   *
   * @param requestParameters {@link UpdateDiaryParameters} Request Parameters Object
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> updateDiaryAsync(
    @NonNull UpdateDiaryParameters requestParameters,
    RequestConfig requestConfig
  ) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.updateDiaryConfig, requestConfig);
    Request request = this.buildUpdateDiaryRequest(requestParameters, resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildUpdateDiaryRequest(
    @NonNull UpdateDiaryParameters requestParameters,
    RequestConfig resolvedConfig
  ) {
    return new RequestBuilder(
      HttpMethod.PUT,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/diary"
    )
      .setHeader("Authorization", requestParameters.getAuthorization())
      .setJsonContent(requestParameters.getRequestBody())
      .build();
  }

  /**
   * Method getScoutData
   * GET /api/scout
   *
   * @return response of {@code Object}
   */
  public Object getScoutData() throws ApiError {
    return this.getScoutData(null);
  }

  /**
   * Method getScoutData
   * GET /api/scout
   *
   * @return response of {@code Object}
   */
  public Object getScoutData(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getScoutDataConfig, requestConfig);
    Request request = this.buildGetScoutDataRequest(resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method getScoutData
   * GET /api/scout
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getScoutDataAsync() throws ApiError {
    return this.getScoutDataAsync(null);
  }

  /**
   * Method getScoutData
   * GET /api/scout
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getScoutDataAsync(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getScoutDataConfig, requestConfig);
    Request request = this.buildGetScoutDataRequest(resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildGetScoutDataRequest(RequestConfig resolvedConfig) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/scout"
    ).build();
  }

  /**
   * Method getCorpusStats
   * GET /api/corpus/stats
   *
   * @return response of {@code Object}
   */
  public Object getCorpusStats() throws ApiError {
    return this.getCorpusStats(null);
  }

  /**
   * Method getCorpusStats
   * GET /api/corpus/stats
   *
   * @return response of {@code Object}
   */
  public Object getCorpusStats(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getCorpusStatsConfig, requestConfig);
    Request request = this.buildGetCorpusStatsRequest(resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method getCorpusStats
   * GET /api/corpus/stats
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getCorpusStatsAsync() throws ApiError {
    return this.getCorpusStatsAsync(null);
  }

  /**
   * Method getCorpusStats
   * GET /api/corpus/stats
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getCorpusStatsAsync(RequestConfig requestConfig)
    throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getCorpusStatsConfig, requestConfig);
    Request request = this.buildGetCorpusStatsRequest(resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildGetCorpusStatsRequest(RequestConfig resolvedConfig) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/corpus/stats"
    ).build();
  }

  /**
   * Method getCorpusCountries
   * GET /api/corpus/countries
   *
   * @return response of {@code Object}
   */
  public Object getCorpusCountries() throws ApiError {
    return this.getCorpusCountries(null);
  }

  /**
   * Method getCorpusCountries
   * GET /api/corpus/countries
   *
   * @return response of {@code Object}
   */
  public Object getCorpusCountries(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.getCorpusCountriesConfig, requestConfig);
    Request request = this.buildGetCorpusCountriesRequest(resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method getCorpusCountries
   * GET /api/corpus/countries
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getCorpusCountriesAsync() throws ApiError {
    return this.getCorpusCountriesAsync(null);
  }

  /**
   * Method getCorpusCountries
   * GET /api/corpus/countries
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getCorpusCountriesAsync(RequestConfig requestConfig)
    throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.getCorpusCountriesConfig, requestConfig);
    Request request = this.buildGetCorpusCountriesRequest(resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildGetCorpusCountriesRequest(RequestConfig resolvedConfig) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/corpus/countries"
    ).build();
  }

  /**
   * Method searchCorpusAnalysis
   * GET /api/corpus/analysis/search
   *
   * @return response of {@code Object}
   */
  public Object searchCorpusAnalysis() throws ApiError {
    return this.searchCorpusAnalysis(SearchCorpusAnalysisParameters.builder().build());
  }

  /**
   * Method searchCorpusAnalysis
   * GET /api/corpus/analysis/search
   *
   * @param requestParameters {@link SearchCorpusAnalysisParameters} Request Parameters Object
   * @return response of {@code Object}
   */
  public Object searchCorpusAnalysis(@NonNull SearchCorpusAnalysisParameters requestParameters)
    throws ApiError {
    return this.searchCorpusAnalysis(requestParameters, null);
  }

  /**
   * Method searchCorpusAnalysis
   * GET /api/corpus/analysis/search
   *
   * @param requestParameters {@link SearchCorpusAnalysisParameters} Request Parameters Object
   * @return response of {@code Object}
   */
  public Object searchCorpusAnalysis(
    @NonNull SearchCorpusAnalysisParameters requestParameters,
    RequestConfig requestConfig
  ) throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.searchCorpusAnalysisConfig, requestConfig);
    Request request = this.buildSearchCorpusAnalysisRequest(requestParameters, resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method searchCorpusAnalysis
   * GET /api/corpus/analysis/search
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> searchCorpusAnalysisAsync() throws ApiError {
    return this.searchCorpusAnalysisAsync(SearchCorpusAnalysisParameters.builder().build());
  }

  /**
   * Method searchCorpusAnalysis
   * GET /api/corpus/analysis/search
   *
   * @param requestParameters {@link SearchCorpusAnalysisParameters} Request Parameters Object
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> searchCorpusAnalysisAsync(
    @NonNull SearchCorpusAnalysisParameters requestParameters
  ) throws ApiError {
    return this.searchCorpusAnalysisAsync(requestParameters, null);
  }

  /**
   * Method searchCorpusAnalysis
   * GET /api/corpus/analysis/search
   *
   * @param requestParameters {@link SearchCorpusAnalysisParameters} Request Parameters Object
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> searchCorpusAnalysisAsync(
    @NonNull SearchCorpusAnalysisParameters requestParameters,
    RequestConfig requestConfig
  ) throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.searchCorpusAnalysisConfig, requestConfig);
    Request request = this.buildSearchCorpusAnalysisRequest(requestParameters, resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildSearchCorpusAnalysisRequest(
    @NonNull SearchCorpusAnalysisParameters requestParameters,
    RequestConfig resolvedConfig
  ) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/corpus/analysis/search"
    )
      .setOptionalQueryParameter("attr", requestParameters.getAttr())
      .setOptionalQueryParameter("figure", requestParameters.getFigure())
      .build();
  }

  /**
   * Method listCorpusAnalysis
   * GET /api/corpus/analysis
   *
   * @return response of {@code Object}
   */
  public Object listCorpusAnalysis() throws ApiError {
    return this.listCorpusAnalysis(null);
  }

  /**
   * Method listCorpusAnalysis
   * GET /api/corpus/analysis
   *
   * @return response of {@code Object}
   */
  public Object listCorpusAnalysis(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.listCorpusAnalysisConfig, requestConfig);
    Request request = this.buildListCorpusAnalysisRequest(resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method listCorpusAnalysis
   * GET /api/corpus/analysis
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> listCorpusAnalysisAsync() throws ApiError {
    return this.listCorpusAnalysisAsync(null);
  }

  /**
   * Method listCorpusAnalysis
   * GET /api/corpus/analysis
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> listCorpusAnalysisAsync(RequestConfig requestConfig)
    throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.listCorpusAnalysisConfig, requestConfig);
    Request request = this.buildListCorpusAnalysisRequest(resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildListCorpusAnalysisRequest(RequestConfig resolvedConfig) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/corpus/analysis"
    ).build();
  }

  /**
   * Method listCorpusItems
   * GET /api/corpus
   *
   * @return response of {@code Object}
   */
  public Object listCorpusItems() throws ApiError {
    return this.listCorpusItems(ListCorpusItemsParameters.builder().build());
  }

  /**
   * Method listCorpusItems
   * GET /api/corpus
   *
   * @param requestParameters {@link ListCorpusItemsParameters} Request Parameters Object
   * @return response of {@code Object}
   */
  public Object listCorpusItems(@NonNull ListCorpusItemsParameters requestParameters)
    throws ApiError {
    return this.listCorpusItems(requestParameters, null);
  }

  /**
   * Method listCorpusItems
   * GET /api/corpus
   *
   * @param requestParameters {@link ListCorpusItemsParameters} Request Parameters Object
   * @return response of {@code Object}
   */
  public Object listCorpusItems(
    @NonNull ListCorpusItemsParameters requestParameters,
    RequestConfig requestConfig
  ) throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.listCorpusItemsConfig, requestConfig);
    Request request = this.buildListCorpusItemsRequest(requestParameters, resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method listCorpusItems
   * GET /api/corpus
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> listCorpusItemsAsync() throws ApiError {
    return this.listCorpusItemsAsync(ListCorpusItemsParameters.builder().build());
  }

  /**
   * Method listCorpusItems
   * GET /api/corpus
   *
   * @param requestParameters {@link ListCorpusItemsParameters} Request Parameters Object
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> listCorpusItemsAsync(
    @NonNull ListCorpusItemsParameters requestParameters
  ) throws ApiError {
    return this.listCorpusItemsAsync(requestParameters, null);
  }

  /**
   * Method listCorpusItems
   * GET /api/corpus
   *
   * @param requestParameters {@link ListCorpusItemsParameters} Request Parameters Object
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> listCorpusItemsAsync(
    @NonNull ListCorpusItemsParameters requestParameters,
    RequestConfig requestConfig
  ) throws ApiError {
    RequestConfig resolvedConfig =
      this.getResolvedConfig(this.listCorpusItemsConfig, requestConfig);
    Request request = this.buildListCorpusItemsRequest(requestParameters, resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildListCorpusItemsRequest(
    @NonNull ListCorpusItemsParameters requestParameters,
    RequestConfig resolvedConfig
  ) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/corpus"
    )
      .setOptionalQueryParameter("country", requestParameters.getCountry())
      .setOptionalQueryParameter("regime", requestParameters.getRegime())
      .setOptionalQueryParameter("q", requestParameters.getQ())
      .build();
  }

  /**
   * Method getCorpusItem
   * GET /api/corpus/{itemId}
   *
   * @return response of {@code Object}
   */
  public Object getCorpusItem() throws ApiError {
    return this.getCorpusItem(null);
  }

  /**
   * Method getCorpusItem
   * GET /api/corpus/{itemId}
   *
   * @return response of {@code Object}
   */
  public Object getCorpusItem(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getCorpusItemConfig, requestConfig);
    Request request = this.buildGetCorpusItemRequest(resolvedConfig);
    Response response = this.execute(request, resolvedConfig);
    byte[] bodyBytes = ModelConverter.readBytes(response);
    return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
  }

  /**
   * Method getCorpusItem
   * GET /api/corpus/{itemId}
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getCorpusItemAsync() throws ApiError {
    return this.getCorpusItemAsync(null);
  }

  /**
   * Method getCorpusItem
   * GET /api/corpus/{itemId}
   *
   * @return response of {@code CompletableFuture<Object>}
   */
  public CompletableFuture<Object> getCorpusItemAsync(RequestConfig requestConfig) throws ApiError {
    RequestConfig resolvedConfig = this.getResolvedConfig(this.getCorpusItemConfig, requestConfig);
    Request request = this.buildGetCorpusItemRequest(resolvedConfig);
    CompletableFuture<Response> futureResponse = this.executeAsync(request, resolvedConfig);
    return futureResponse.thenApplyAsync(response -> {
      byte[] bodyBytes = ModelConverter.readBytes(response);
      return ModelConverter.convert(bodyBytes, new TypeReference<Object>() {});
    });
  }

  private Request buildGetCorpusItemRequest(RequestConfig resolvedConfig) {
    return new RequestBuilder(
      HttpMethod.GET,
      resolveBaseUrl(resolvedConfig, Environment.LOCALHOST8787),
      "api/corpus/{itemId}"
    ).build();
  }
}
