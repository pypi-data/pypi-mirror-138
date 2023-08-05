from typing import Iterator, Set

from pydantic.class_validators import root_validator

from structurizr2csv.coordinates import Dimensions, Position
from structurizr2csv.elements.base_box import BaseBox
from structurizr2csv.enums import Terminology
from structurizr2csv.settings import FILL_COLORS, STROKE_COLORS


class LegendRow(BaseBox):

    box_type: str
    _height: int = 30

    @root_validator(pre=True)
    def init_base_box_attrs(cls, values):  # @NoSelf
        """Initialize `position` and `dimensions`"""
        values.update({"dimensions": Dimensions(x=180, y=cls._height)})
        return values

    @property
    def style(self) -> str:
        return "legend_row"

    @property
    def label(self) -> str:
        match self.box_type.split("-"):
            case c4_name, tag:
                return "{} {}".format(
                    tag.title(), getattr(Terminology, c4_name).value  # noqa
                )
            case [c4_name]:  # noqa
                return getattr(Terminology, c4_name).value  # noqa
            case _:
                raise NotImplementedError

    @property
    def csv_data(self):
        data = super().csv_data
        data.update(
            {
                "c4Name": self.label,
                "id": f"id_{self.box_type}",
                "parent": Legend._id,
                "styleKey": self.style,
                "labelKey": self.style,
                "left": self.position.x,
                "top": self.position.y,
                "width": self.dimensions.x,
                "height": self.dimensions.y,
                "fill": FILL_COLORS.get(self.box_type, ""),
                "stroke": STROKE_COLORS.get(self.box_type, ""),
            }
        )
        return data


class LegendHeader(LegendRow):
    box_type: str = "legend"

    @property
    def style(self) -> str:
        return "legend_header"


class Legend(BaseBox):
    box_types: Set[str]
    _id: str = "id_legend_container"

    @root_validator(pre=True)
    def init_base_box_attrs(cls, values):  # @NoSelf
        """Initialize `dimensions`"""
        values.update(
            {
                "dimensions": Dimensions(
                    x=180, y=LegendRow._height * (1 + len(values["box_types"]))
                )
            }
        )
        return values

    @property
    def csv_data(self):
        data = super().csv_data
        data.update(
            {
                "id": self._id,
                "styleKey": '"strokeColor=none;"',  # don't display the border
                "left": self.position.x,
                "top": self.position.y,
                "width": self.dimensions.x,
                "height": self.dimensions.y,
            }  # pyright: reportGeneralTypeIssues=false
        )
        return data

    def to_csv(self) -> Iterator[str]:
        yield super().to_csv()
        yield LegendHeader(position=Position(x=0, y=0)).to_csv()
        for index, box_type in enumerate(
            sorted(
                # sort by color first, then by label
                self.box_types,
                key=lambda box_type: (FILL_COLORS[box_type], box_type),
            ),
            1,
        ):
            yield LegendRow(
                position=Position(x=0, y=index * LegendRow._height), box_type=box_type
            ).to_csv()
