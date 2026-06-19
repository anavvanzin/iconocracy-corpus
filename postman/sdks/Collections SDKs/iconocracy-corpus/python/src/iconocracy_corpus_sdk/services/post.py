from typing import Any, Optional
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models
from ..models import PostDataRequest


class PostService(BaseService):
    """
    Service class for PostService operations.
    Provides methods to interact with PostService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._post_data_config: SdkConfig = {"environment": Environment.POSTMAN_ECHO}

    def set_post_data_config(self, config: SdkConfig):
        """
        Sets method-level configuration for post_data.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._post_data_config = config
        return self

    @cast_models
    def post_data(
        self,
        request_body: PostDataRequest,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Any:
        """This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. A successful POST request typically returns a `200 OK` or `201 Created` response code.

        :param request_body: The request body.
        :type request_body: PostDataRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        Validator(PostDataRequest).is_nullable().validate(request_body)

        resolved_config = self._get_resolved_config(
            self._post_data_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.POSTMAN_ECHO.url or Environment.DEFAULT.url}/post",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return response
