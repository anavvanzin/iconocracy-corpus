import { z } from 'zod';
import { BaseService } from '../base-service';
import { ContentType, HttpResponse, SdkConfig } from '../../http/types';
import { RequestBuilder } from '../../http/transport/request-builder';
import { SerializationStyle } from '../../http/serialization/base-serializer';
import { ThrowableError } from '../../http/errors/throwable-error';
import { Environment } from '../../http/environment';

/**
 * Service class for Get_Service operations.
 * Provides methods to interact with Get_Service-related API endpoints.
 * All methods return promises and handle request/response serialization automatically.
 */
export class Get_Service extends BaseService {
  protected getDataConfig: Partial<SdkConfig> = { environment: Environment.POSTMAN_ECHO };

  /**
   * Sets method-level configuration for getData.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setGetDataConfig(config: Partial<SdkConfig>): this {
    this.getDataConfig = config;
    return this;
  }

  /**
 * This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).
A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.
 * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
 * @returns {Promise<HttpResponse<any>>} - OK
 */
  async getData(requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.getDataConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('GET')
      .setPath('/get')
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
