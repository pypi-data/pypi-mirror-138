from pydantic import BaseModel


class Coordinates(BaseModel):
    x: int
    y: int


class Position(Coordinates):
    pass


class Dimensions(Coordinates):
    pass
