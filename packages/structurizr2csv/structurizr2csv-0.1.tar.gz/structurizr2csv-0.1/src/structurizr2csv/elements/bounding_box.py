from typing import TYPE_CHECKING, List, Optional

from structurizr2csv.coordinates import Dimensions, Position
from structurizr2csv.elements.base_box import BaseBox

if TYPE_CHECKING:
    from .box import Box  # @UnusedImport


class BoundingBox(BaseBox):
    @classmethod
    def compute_from_boxes(
        cls, boxes: List["Box"], **kwargs
    ) -> Optional["BoundingBox"]:
        if not boxes:
            return None

        position = Position(
            x=min(box.position.x for box in boxes),
            y=min(box.position.y for box in boxes),
        )
        max_coordinates = Position(
            x=max(box.position.x + box.dimensions.x for box in boxes),
            y=max(box.position.y + box.dimensions.y for box in boxes),
        )
        return cls(
            position=position,
            dimensions=Dimensions(
                x=max_coordinates.x - position.x,
                y=max_coordinates.y - position.y,
            ),
            **kwargs,
        )
