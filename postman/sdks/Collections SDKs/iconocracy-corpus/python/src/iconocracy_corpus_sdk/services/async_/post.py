from typing import Awaitable, Optional, Any
from .utils.to_async import to_async
from ..post import PostService
from ...net.sdk_config import SdkConfig
from ...models import PostDataRequest


class PostServiceAsync(PostService):
    """
    Async Wrapper for PostServiceAsync
    """

    def post_data(
        self,
        request_body: PostDataRequest,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Awaitable[Any]:
        return to_async(super().post_data)(request_body, request_config=request_config)
