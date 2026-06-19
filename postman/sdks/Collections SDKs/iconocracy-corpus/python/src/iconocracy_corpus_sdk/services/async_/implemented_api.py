from typing import Awaitable, Optional, Any, List, Union
from .utils.to_async import to_async
from ..implemented_api import ImplementedApiService
from ...net.sdk_config import SdkConfig
from ...models.utils.sentinel import SENTINEL


class ImplementedApiServiceAsync(ImplementedApiService):
    """
    Async Wrapper for ImplementedApiServiceAsync
    """

    def get_diary(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().get_diary)(request_config=request_config)

    def update_diary(
        self,
        request_body: List[Any],
        authorization: Union[str, None],
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Awaitable[Any]:
        return to_async(super().update_diary)(
            request_body, authorization, request_config=request_config
        )

    def get_scout_data(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().get_scout_data)(request_config=request_config)

    def get_corpus_stats(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().get_corpus_stats)(request_config=request_config)

    def get_corpus_countries(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().get_corpus_countries)(request_config=request_config)

    def search_corpus_analysis(
        self,
        attr: Union[str, None] = SENTINEL,
        figure: Union[str, None] = SENTINEL,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Awaitable[Any]:
        return to_async(super().search_corpus_analysis)(
            attr, figure, request_config=request_config
        )

    def list_corpus_analysis(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().list_corpus_analysis)(request_config=request_config)

    def list_corpus_items(
        self,
        country: Union[str, None] = SENTINEL,
        regime: Union[str, None] = SENTINEL,
        q: Union[str, None] = SENTINEL,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Awaitable[Any]:
        return to_async(super().list_corpus_items)(
            country, regime, q, request_config=request_config
        )

    def get_corpus_item(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().get_corpus_item)(request_config=request_config)
