from typing import Any, Optional, List, Union
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.sentinel import SENTINEL
from ..models.utils.cast_models import cast_models


class ImplementedApiService(BaseService):
    """
    Service class for ImplementedApiService operations.
    Provides methods to interact with ImplementedApiService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._get_diary_config: SdkConfig = {"environment": Environment.LOCALHOST8787}
        self._update_diary_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }
        self._get_scout_data_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }
        self._get_corpus_stats_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }
        self._get_corpus_countries_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }
        self._search_corpus_analysis_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }
        self._list_corpus_analysis_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }
        self._list_corpus_items_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }
        self._get_corpus_item_config: SdkConfig = {
            "environment": Environment.LOCALHOST8787
        }

    def set_get_diary_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_diary.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_diary_config = config
        return self

    def set_update_diary_config(self, config: SdkConfig):
        """
        Sets method-level configuration for update_diary.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._update_diary_config = config
        return self

    def set_get_scout_data_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_scout_data.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_scout_data_config = config
        return self

    def set_get_corpus_stats_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_corpus_stats.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_corpus_stats_config = config
        return self

    def set_get_corpus_countries_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_corpus_countries.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_corpus_countries_config = config
        return self

    def set_search_corpus_analysis_config(self, config: SdkConfig):
        """
        Sets method-level configuration for search_corpus_analysis.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._search_corpus_analysis_config = config
        return self

    def set_list_corpus_analysis_config(self, config: SdkConfig):
        """
        Sets method-level configuration for list_corpus_analysis.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._list_corpus_analysis_config = config
        return self

    def set_list_corpus_items_config(self, config: SdkConfig):
        """
        Sets method-level configuration for list_corpus_items.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._list_corpus_items_config = config
        return self

    def set_get_corpus_item_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_corpus_item.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_corpus_item_config = config
        return self

    @cast_models
    def get_diary(self, *, request_config: Optional[SdkConfig] = None) -> Any:
        """get_diary

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._get_diary_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/diary",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def update_diary(
        self,
        request_body: List[Any],
        authorization: Union[str, None],
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Any:
        """update_diary

        :param request_body: The request body.
        :type request_body: List[Any]
        :param authorization: authorization
        :type authorization: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        Validator(Any).is_array().is_nullable().validate(request_body)
        Validator(str).is_nullable().validate(authorization)

        resolved_config = self._get_resolved_config(
            self._update_diary_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/diary",
                [],
                resolved_config,
            )
            .add_header("Authorization", authorization)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def get_scout_data(self, *, request_config: Optional[SdkConfig] = None) -> Any:
        """get_scout_data

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._get_scout_data_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/scout",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def get_corpus_stats(self, *, request_config: Optional[SdkConfig] = None) -> Any:
        """get_corpus_stats

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._get_corpus_stats_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/corpus/stats",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def get_corpus_countries(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Any:
        """get_corpus_countries

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._get_corpus_countries_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/corpus/countries",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def search_corpus_analysis(
        self,
        attr: Union[str, None] = SENTINEL,
        figure: Union[str, None] = SENTINEL,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Any:
        """search_corpus_analysis

        :param attr: attr, defaults to None
        :type attr: str, optional
        :param figure: figure, defaults to None
        :type figure: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        Validator(str).is_optional().is_nullable().validate(attr)
        Validator(str).is_optional().is_nullable().validate(figure)

        resolved_config = self._get_resolved_config(
            self._search_corpus_analysis_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/corpus/analysis/search",
                [],
                resolved_config,
            )
            .add_query("attr", attr, nullable=True)
            .add_query("figure", figure, nullable=True)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def list_corpus_analysis(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Any:
        """list_corpus_analysis

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._list_corpus_analysis_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/corpus/analysis",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def list_corpus_items(
        self,
        country: Union[str, None] = SENTINEL,
        regime: Union[str, None] = SENTINEL,
        q: Union[str, None] = SENTINEL,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Any:
        """list_corpus_items

        :param country: country, defaults to None
        :type country: str, optional
        :param regime: regime, defaults to None
        :type regime: str, optional
        :param q: q, defaults to None
        :type q: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        Validator(str).is_optional().is_nullable().validate(country)
        Validator(str).is_optional().is_nullable().validate(regime)
        Validator(str).is_optional().is_nullable().validate(q)

        resolved_config = self._get_resolved_config(
            self._list_corpus_items_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/corpus",
                [],
                resolved_config,
            )
            .add_query("country", country, nullable=True)
            .add_query("regime", regime, nullable=True)
            .add_query("q", q, nullable=True)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def get_corpus_item(self, *, request_config: Optional[SdkConfig] = None) -> Any:
        """get_corpus_item

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._get_corpus_item_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.LOCALHOST8787.url or Environment.DEFAULT.url}/api/corpus/{{itemId}}",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response
