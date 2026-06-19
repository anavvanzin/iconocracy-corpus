import { z } from 'zod';
import { BaseService } from '../base-service';
import { ContentType, HttpResponse, SdkConfig } from '../../http/types';
import { RequestBuilder } from '../../http/transport/request-builder';
import { SerializationStyle } from '../../http/serialization/base-serializer';
import { ThrowableError } from '../../http/errors/throwable-error';
import { Environment } from '../../http/environment';
import {
  ListCorpusItemsParams,
  SearchCorpusAnalysisParams,
  UpdateDiaryParams,
} from './request-params';

/**
 * Service class for ImplementedApiService operations.
 * Provides methods to interact with ImplementedApiService-related API endpoints.
 * All methods return promises and handle request/response serialization automatically.
 */
export class ImplementedApiService extends BaseService {
  protected getDiaryConfig: Partial<SdkConfig> = { environment: Environment.LOCALHOST8787 };

  protected updateDiaryConfig: Partial<SdkConfig> = { environment: Environment.LOCALHOST8787 };

  protected getScoutDataConfig: Partial<SdkConfig> = { environment: Environment.LOCALHOST8787 };

  protected getCorpusStatsConfig: Partial<SdkConfig> = { environment: Environment.LOCALHOST8787 };

  protected getCorpusCountriesConfig: Partial<SdkConfig> = {
    environment: Environment.LOCALHOST8787,
  };

  protected searchCorpusAnalysisConfig: Partial<SdkConfig> = {
    environment: Environment.LOCALHOST8787,
  };

  protected listCorpusAnalysisConfig: Partial<SdkConfig> = {
    environment: Environment.LOCALHOST8787,
  };

  protected listCorpusItemsConfig: Partial<SdkConfig> = { environment: Environment.LOCALHOST8787 };

  protected getCorpusItemConfig: Partial<SdkConfig> = { environment: Environment.LOCALHOST8787 };

  /**
   * Sets method-level configuration for getDiary.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setGetDiaryConfig(config: Partial<SdkConfig>): this {
    this.getDiaryConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for updateDiary.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setUpdateDiaryConfig(config: Partial<SdkConfig>): this {
    this.updateDiaryConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for getScoutData.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setGetScoutDataConfig(config: Partial<SdkConfig>): this {
    this.getScoutDataConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for getCorpusStats.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setGetCorpusStatsConfig(config: Partial<SdkConfig>): this {
    this.getCorpusStatsConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for getCorpusCountries.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setGetCorpusCountriesConfig(config: Partial<SdkConfig>): this {
    this.getCorpusCountriesConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for searchCorpusAnalysis.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setSearchCorpusAnalysisConfig(config: Partial<SdkConfig>): this {
    this.searchCorpusAnalysisConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for listCorpusAnalysis.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setListCorpusAnalysisConfig(config: Partial<SdkConfig>): this {
    this.listCorpusAnalysisConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for listCorpusItems.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setListCorpusItemsConfig(config: Partial<SdkConfig>): this {
    this.listCorpusItemsConfig = config;
    return this;
  }

  /**
   * Sets method-level configuration for getCorpusItem.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setGetCorpusItemConfig(config: Partial<SdkConfig>): this {
    this.getCorpusItemConfig = config;
    return this;
  }

  /**
   *
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async getDiary(requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.getDiaryConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/diary')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {string} params.authorization -
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async updateDiary(
    body: any[],
    params: UpdateDiaryParams,
    requestConfig?: Partial<SdkConfig>,
  ): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.updateDiaryConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('PUT')
      .setPath('/api/diary')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .addHeaderParam({
        key: 'Authorization',
        value: params?.authorization,
      })
      .addHeaderParam({ key: 'Content-Type', value: 'application/json' })
      .addBody(body)
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async getScoutData(requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.getScoutDataConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/scout')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async getCorpusStats(requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.getCorpusStatsConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/corpus/stats')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async getCorpusCountries(requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.getCorpusCountriesConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/corpus/countries')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {string} [params.attr] -
   * @param {string} [params.figure] -
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async searchCorpusAnalysis(
    params?: SearchCorpusAnalysisParams,
    requestConfig?: Partial<SdkConfig>,
  ): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.searchCorpusAnalysisConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/corpus/analysis/search')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .addQueryParam({
        key: 'attr',
        value: params?.attr,
      })
      .addQueryParam({
        key: 'figure',
        value: params?.figure,
      })
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async listCorpusAnalysis(requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.listCorpusAnalysisConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/corpus/analysis')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {string} [params.country] -
   * @param {string} [params.regime] -
   * @param {string} [params.q] -
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async listCorpusItems(
    params?: ListCorpusItemsParams,
    requestConfig?: Partial<SdkConfig>,
  ): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.listCorpusItemsConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/corpus')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .addQueryParam({
        key: 'country',
        value: params?.country,
      })
      .addQueryParam({
        key: 'regime',
        value: params?.regime,
      })
      .addQueryParam({
        key: 'q',
        value: params?.q,
      })
      .build();
    return this.client.callDirect<any>(request);
  }

  /**
   *
   * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
   * @returns {Promise<HttpResponse<any>>} - OK
   */
  async getCorpusItem(requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.getCorpusItemConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/api/corpus/{itemId}')
      .setRequestSchema(z.any())
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .build();
    return this.client.callDirect<any>(request);
  }
}
