from functools import cached_property
from typing import Dict, List

from pydantic.class_validators import root_validator

from structurizr2csv.coordinates import Dimensions, Position
from structurizr2csv.elements.base_box import BaseBox
from structurizr2csv.enums import Tag, Terminology
from structurizr2csv.settings import FILL_COLORS, POSITION_FACTOR, STROKE_COLORS
from structurizr2csv.workspace import Component, Container, ElementView
from structurizr2csv.workspace_extension import Element


class Box(BaseBox):
    """Convert a basic element in structurizr to a box in diagrams.net"""

    class Config:
        keep_untouched = (cached_property,)

    element: ElementView

    @root_validator(pre=True)
    def init_base_box_attrs(cls, values):  # type: ignore
        """Initialize `position` and `dimensions` based on `element`"""
        element = values["element"]
        values["position"] = Position(
            x=element.x * POSITION_FACTOR,
            y=element.y * POSITION_FACTOR,
        )
        values["dimensions"] = Dimensions(x=cls.width(element), y=cls.height(element))
        return values

    @classmethod
    def width(cls, element):
        """Box's width in diagrams.net"""
        match element.c4_type:
            case Terminology.person:
                return 200
            case _:
                return 240

        raise NotImplementedError

    @classmethod
    def height(cls, element):
        """Box's height in diagrams.net"""
        match element.c4_type:
            case Terminology.person:
                return 180
            case _:
                return 120

        raise NotImplementedError

    @property
    def style(self) -> str:
        """Returns the style in diagrams.net"""
        style = self.definition.c4_type.name  # type: ignore
        for tag in (
            Tag.HEXAGON,
            Tag.CYLINDER,
            Tag.PIPE,
            Tag.WEB_BROWSER,
            Tag.DATABASE,
            Tag.MOBILE_APP,
        ):
            if tag.value in self.tags:
                match tag:  # handle aliases
                    case Tag.DATABASE:
                        tag = Tag.CYLINDER
                    case Tag.MOBILE_APP:
                        tag = Tag.WEB_BROWSER
                return tag.value.lower().replace("_", "-").replace(" ", "-")

        return style

    @property
    def box_type(self) -> str:
        """Returns the shape's type"""
        c4_type = self.definition.c4_type  # pyright: reportGeneralTypeIssues=false
        if Tag.EXISTING_SYSTEM.value in self.tags:
            return f"{c4_type.name}-existing"
        elif self.is_internal or c4_type == Terminology.person:
            return c4_type.name
        else:
            return f"{c4_type.name}-external"

    def get_color(self, colors: Dict[str, str]) -> str:
        return colors[self.box_type]

    @property
    def definition(self) -> Element:
        """Returns the model element for this view element"""
        return self.element.definition  # type: ignore

    @property
    def is_internal(self) -> bool:
        """Tells if the box is internal to the company or not"""
        return (
            isinstance(self.definition, (Component, Container))
            or self.definition.is_internal
        )

    @property
    def tags(self) -> List[str]:
        return self.definition.tags.split(",") if self.definition.tags else []

    @property
    def c4_type(self) -> Terminology:
        return self.definition.c4_type

    @property
    def csv_data(self) -> Dict[str, str]:
        type_ = self.c4_type.value
        if getattr(self.definition, "technology", None):
            type_ += f": {self.definition.technology}"

        return {
            "c4Name": self.definition.name,
            "c4Type": type_,
            "c4Description": self.definition.safe_description,
            "id": self.element.id,
            "parent": self.parent_id,
            "styleKey": self.style,
            "labelKey": "box",
            "left": self.relative_position.x,
            "top": self.relative_position.y,
            "width": self.dimensions.x,
            "height": self.dimensions.y,
            "fill": self.get_color(FILL_COLORS),
            "stroke": self.get_color(STROKE_COLORS),
        }
