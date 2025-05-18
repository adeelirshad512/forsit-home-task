import json
from datetime import datetime
from typing import Any, Type
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class Page(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

    class Config:
        arbitrary_types_allowed = True

class ResponseModel(BaseModel, Generic[T]):
    result: Optional[T] = None
    error: Optional[dict] = None

class CustomResponse(JSONResponse, Generic[T]):
    def render(self, content: Any) -> bytes:
        def default(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
        return json.dumps(content, default=default).encode("utf-8")

    def __init__(
        self,
        content: Any,
        *args,
        error: Optional[dict] = None,
        **kwargs
    ):
        if error:
            wrapped_content = ResponseModel[T](result=None, error=error)
        else:
            if isinstance(content, list):
                wrapped_content = ResponseModel[T](result={"data": content}, error=None)
            elif isinstance(content, dict) and all(k in content for k in ["items", "total", "page", "size"]):
                wrapped_content = ResponseModel[T](
                    result={
                        "data": content["items"],
                        "total": content["total"],
                        "page": content["page"],
                        "size": content["size"],
                    },
                    error=None,
                )
            elif isinstance(content, Page):
                wrapped_content = ResponseModel[T](
                    result={
                        "data": content.items,
                        "total": content.total,
                        "page": content.page,
                        "size": content.size,
                    },
                    error=None,
                )
            else:
                wrapped_content = ResponseModel[T](result=content, error=None)
        super().__init__(content=wrapped_content.dict(), *args, **kwargs)

def success_response(data: Any, model: Type[BaseModel] = None):
    is_page_model = model and hasattr(model, "__origin__") and model.__origin__ is Page

    if is_page_model and hasattr(data, "items"):
        inner_model = model.__args__[0]
        items = [inner_model.model_validate(item).model_dump() for item in data.items]
        page_data = {
            "items": items,
            "total": data.total,
            "page": data.page,
            "size": data.size,
        }
        return CustomResponse(content=page_data)

    if isinstance(data, BaseModel):
        data = data.model_dump()

    return CustomResponse(content=data)
