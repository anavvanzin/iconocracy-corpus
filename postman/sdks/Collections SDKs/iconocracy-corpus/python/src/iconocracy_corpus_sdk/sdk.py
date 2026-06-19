from typing import Union
from .services.get import GetService
from .services.implemented_api import ImplementedApiService
from .services.post import PostService
from .net.environment import Environment


class IconocracyCorpusSdk:
    """
    Main SDK client class for IconocracyCorpusSdk.
    Provides centralized configuration and access to all service endpoints.
    Supports authentication, environment management, and global timeout settings.
    """

    def __init__(
        self, base_url: Union[Environment, str, None] = None, timeout: int = 60000
    ):
        """
        Initializes IconocracyCorpusSdk the SDK class.
        """

        self._base_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )
        self.get = GetService(base_url=self._base_url)
        self.implemented_api = ImplementedApiService(base_url=self._base_url)
        self.post = PostService(base_url=self._base_url)
        self.set_timeout(timeout)

    def set_base_url(self, base_url: Union[Environment, str]):
        """
        Sets the base URL for the entire SDK.

        :param Union[Environment, str] base_url: The base URL to be set.
        :return: The SDK instance.
        """
        self._base_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )

        self.get.set_base_url(self._base_url)
        self.implemented_api.set_base_url(self._base_url)
        self.post.set_base_url(self._base_url)

        return self

    def set_timeout(self, timeout: int):
        """
        Sets the timeout for the entire SDK.

        :param int timeout: The timeout (ms) to be set.
        :return: The SDK instance.
        """
        self.get.set_timeout(timeout)
        self.implemented_api.set_timeout(timeout)
        self.post.set_timeout(timeout)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
