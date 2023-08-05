from typing import TYPE_CHECKING, Optional

from pydantic.fields import Field

from structurizr2csv.coordinates import Dimensions, Position
from structurizr2csv.elements.bounding_box import BoundingBox
from structurizr2csv.enums import Terminology
from structurizr2csv.settings import (
    PRIMARY_GROUP_BOTTOM_PADDING,
    PRIMARY_GROUP_PADDING,
    SECONDARY_GROUP_BOTTOM_PADDING,
    SECONDARY_GROUP_PADDING,
)
from structurizr2csv.style import Style
from structurizr2csv.utils import auto_index

if TYPE_CHECKING:
    from structurizr2csv.elements.box import Box  # noqa: F401


class Group(BoundingBox):
    """Convert a group/enterprise in structurizr to a parent box in diagrams.net"""

    id: str = Field(default_factory=lambda: auto_index("g", Group))

    name: str
    c4_type: Optional[Terminology]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.position = Position(
            x=self.position.x - self.padding,
            y=self.position.y - self.padding,
        )
        self.dimensions = Dimensions(
            x=self.dimensions.x + 2 * self.padding,
            y=self.dimensions.y + self.padding + self.bottom_padding,
        )

    @property
    def style(self) -> str:
        return "group_1" if self.is_primary else "group_2"

    @property
    def is_primary(self) -> bool:
        return self.c4_type is not None

    @property
    def padding(self) -> int:
        return PRIMARY_GROUP_PADDING if self.is_primary else SECONDARY_GROUP_PADDING

    @property
    def bottom_padding(self) -> int:
        return (
            PRIMARY_GROUP_BOTTOM_PADDING
            if self.is_primary
            else SECONDARY_GROUP_BOTTOM_PADDING
        )

    @property
    def csv_data(self):
        style = Style.get(self.style)

        return {
            "c4Name": self.name,
            "c4Type": self.c4_type.value if self.c4_type else "",
            "c4Description": "",
            "id": self.id,
            "parent": self.parent_id,
            "styleKey": f'"{style}"',
            "labelKey": self.style,
            "left": self.relative_position.x,
            "top": self.relative_position.y,
            "width": self.dimensions.x,
            "height": self.dimensions.y,
            "fill": "",
            "stroke": "",
        }
