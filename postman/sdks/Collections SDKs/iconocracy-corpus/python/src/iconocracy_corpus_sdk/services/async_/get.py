from typing import Awaitable, Optional, Any
from .utils.to_async import to_async
from ..get import GetService
from ...net.sdk_config import SdkConfig


class GetServiceAsync(GetService):
    """
    Async Wrapper for GetServiceAsync
    """

    def get_data(self, *, request_config: Optional[SdkConfig] = None) -> Awaitable[Any]:
        return to_async(super().get_data)(request_config=request_config)
