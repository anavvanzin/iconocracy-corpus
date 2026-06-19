from pydantic import Field
from typing import Optional
from typing import Union
from .utils.base_model import BaseModel


class PostDataRequest(BaseModel):
    """PostDataRequest

    :param name: name, defaults to None
    :type name: str, optional
    """

    name: Optional[str] = Field(default=None)
