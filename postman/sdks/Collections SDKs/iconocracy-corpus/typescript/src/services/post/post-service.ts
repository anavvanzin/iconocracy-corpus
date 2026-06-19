import { z } from 'zod';
import { BaseService } from '../base-service';
import { ContentType, HttpResponse, SdkConfig } from '../../http/types';
import { RequestBuilder } from '../../http/transport/request-builder';
import { SerializationStyle } from '../../http/serialization/base-serializer';
import { ThrowableError } from '../../http/errors/throwable-error';
import { Environment } from '../../http/environment';
import { PostDataRequest, postDataRequestRequest } from './models/post-data-request';

/**
 * Service class for PostService operations.
 * Provides methods to interact with PostService-related API endpoints.
 * All methods return promises and handle request/response serialization automatically.
 */
export class PostService extends BaseService {
  protected postDataConfig: Partial<SdkConfig> = { environment: Environment.POSTMAN_ECHO };

  /**
   * Sets method-level configuration for postData.
   * @param config - Partial configuration to override service-level defaults
   * @returns This service instance for method chaining
   */
  setPostDataConfig(config: Partial<SdkConfig>): this {
    this.postDataConfig = config;
    return this;
  }

  /**
 * This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.
A successful POST request typically returns a `200 OK` or `201 Created` response code.
 * @param {Partial<SdkConfig>} [requestConfig] - The request configuration for retry and validation.
 * @returns {Promise<HttpResponse<any>>} - OK
 */
  async postData(body: PostDataRequest, requestConfig?: Partial<SdkConfig>): Promise<any> {
    const resolvedConfig = this.getResolvedConfig(this.postDataConfig, requestConfig);
    const request = new RequestBuilder()
      .setConfig(resolvedConfig)
      .setBaseUrl(resolvedConfig)
      .setMethod('POST')
      .setPath('/post')
      .setRequestSchema(postDataRequestRequest)
      .setRequestContentType(ContentType.Json)
      .addResponse({
        schema: z.any(),
        contentType: ContentType.Json,
        status: 200,
      })
      .addHeaderParam({ key: 'Content-Type', value: 'application/json' })
      .addBody(body)
      .build();
    return this.client.callDirect<any>(request);
  }
}
