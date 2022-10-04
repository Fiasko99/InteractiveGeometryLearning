from typing import Any, Dict

import pydantic

__all__ = ["BaseClientModel"]


class BaseClientModel(pydantic.BaseModel):
    def to_dict(self) -> Dict[str, Any]:
        """Make transfer model to Dict object."""
        return self.dict()

    class Config:
        use_enum_values = True
