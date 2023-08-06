from typing import Optional

import pydantic


class RegisterUserInput(pydantic.BaseModel):
    size: pydantic.PositiveInt
    name: Optional[str] = None
    is_signed: bool = False
    fraction_places: pydantic.NonNegativeInt = 0

    def is_boolean_register(self) -> bool:
        return (not self.is_signed) and (self.size == 1) and (self.fraction_places == 0)

    class Config:
        extra = "forbid"
