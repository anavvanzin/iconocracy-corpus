from typing import Union
from .net.environment import Environment
from .sdk import IconocracyCorpusSdk
from .services.async_.get import GetServiceAsync
from .services.async_.implemented_api import ImplementedApiServiceAsync
from .services.async_.post import PostServiceAsync


class IconocracyCorpusSdkAsync(IconocracyCorpusSdk):
    """
    IconocracyCorpusSdkAsync is the asynchronous version of the IconocracyCorpusSdk SDK Client.
    """

    def __init__(
        self, base_url: Union[Environment, str, None] = None, timeout: int = 60000
    ):
        super().__init__(base_url=base_url, timeout=timeout)

        self.get = GetServiceAsync(base_url=self._base_url)
        self.implemented_api = ImplementedApiServiceAsync(base_url=self._base_url)
        self.post = PostServiceAsync(base_url=self._base_url)
