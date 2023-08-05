from typing import TYPE_CHECKING, Dict, Iterator, Optional, Tuple

from pydantic import BaseModel

from structurizr2csv.coordinates import Dimensions, Position

if TYPE_CHECKING:
    from structurizr2csv.elements.group import Group  # @UnusedImport


class BaseBox(BaseModel):
    """Base element for any diagrams.net object that is not a connector"""

    position: Position
    dimensions: Dimensions
    parent: Optional["Group"]

    # Attributes that can be edited in diagrams.net via "Edit Data..."
    _data_columns: Tuple[str, ...] = ("c4Name", "c4Type", "c4Description")

    # Other attributes that are not editable
    _meta_columns: Tuple[str, ...] = (
        "id",
        "parent",
        "styleKey",
        "labelKey",
        "left",
        "top",
        "width",
        "height",
        "fill",
        "stroke",
    )

    @classmethod
    def build_placeholders(cls, columns: Tuple[str]) -> str:
        return "{" + "},{".join(columns) + "}"

    @property
    def parent_id(self) -> str:
        return self.parent.id if self.parent else ""

    @property
    def style(self) -> str:
        """Returns the style for displaying the element in diagrams.net"""
        raise NotImplementedError

    @property
    def csv_data(self) -> Dict[str, str]:
        return {key: "" for key in self._data_columns + self._meta_columns}

    @property
    def relative_position(self) -> Position:
        """Returns the position within the element's parent group"""
        if self.parent:
            return Position(
                x=self.position.x - self.parent.position.x,
                y=self.position.y - self.parent.position.y,
            )
        else:
            return self.position

    def to_csv(self) -> str | Iterator[str]:
        return "{},{}".format(
            self.build_placeholders(self._data_columns),
            self.build_placeholders(self._meta_columns),
        ).format(**self.csv_data)
