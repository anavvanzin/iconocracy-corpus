import { Environment } from './http/environment';
import { SdkConfig } from './http/types';
import { Get_Service } from './services/get_';
import { ImplementedApiService } from './services/implemented-api';
import { PostService } from './services/post';

export * from './services/get_';
export * from './services/implemented-api';
export * from './services/post';

export * from './http';
export { Environment } from './http/environment';

export class IconocracyCorpusSdk {
  public readonly get_: Get_Service;

  public readonly implementedApi: ImplementedApiService;

  public readonly post: PostService;

  constructor(public config: SdkConfig) {
    this.get_ = new Get_Service(this.config);

    this.implementedApi = new ImplementedApiService(this.config);

    this.post = new PostService(this.config);
  }

  set baseUrl(baseUrl: string) {
    this.get_.baseUrl = baseUrl;
    this.implementedApi.baseUrl = baseUrl;
    this.post.baseUrl = baseUrl;
  }

  set environment(environment: Environment) {
    this.get_.baseUrl = environment;
    this.implementedApi.baseUrl = environment;
    this.post.baseUrl = environment;
  }

  set timeoutMs(timeoutMs: number) {
    this.get_.timeoutMs = timeoutMs;
    this.implementedApi.timeoutMs = timeoutMs;
    this.post.timeoutMs = timeoutMs;
  }
}

// c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
