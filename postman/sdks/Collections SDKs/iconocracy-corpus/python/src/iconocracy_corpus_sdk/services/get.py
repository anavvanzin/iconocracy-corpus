from typing import Any, Optional
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models


class GetService(BaseService):
    """
    Service class for GetService operations.
    Provides methods to interact with GetService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._get_data_config: SdkConfig = {"environment": Environment.POSTMAN_ECHO}

    def set_get_data_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_data.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_data_config = config
        return self

    @cast_models
    def get_data(self, *, request_config: Optional[SdkConfig] = None) -> Any:
        """This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`). A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._get_data_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.POSTMAN_ECHO.url or Environment.DEFAULT.url}/get",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response
