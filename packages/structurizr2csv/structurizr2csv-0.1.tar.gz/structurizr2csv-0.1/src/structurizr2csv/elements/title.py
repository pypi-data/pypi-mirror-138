from datetime import datetime

from pydantic.class_validators import root_validator

from structurizr2csv.coordinates import Dimensions, Position
from structurizr2csv.elements.base_box import BaseBox
from structurizr2csv.enums import Terminology
from structurizr2csv.settings import POSITION_FACTOR
from structurizr2csv.utils import camel_case
from structurizr2csv.workspace_extension import View


class Title(BaseBox):

    view: View
    title: str

    @root_validator(pre=True)
    def init_base_box_attrs(cls, values):  # @NoSelf
        """Initialize `position` and `dimensions`"""
        values.update(
            {
                "position": Position(
                    x=0,
                    y=values["view"].dimensions.height * POSITION_FACTOR
                    if values["view"].dimensions
                    else 0,
                ),
                "dimensions": Dimensions(x=600, y=40),
            }
        )
        return values

    @property
    def key(self) -> str:
        return self.view.key

    @property
    def description(self) -> str:
        return '"{}"'.format(datetime.today().strftime("%A %d. %B %Y, %H:%M:%S"))

    @property
    def style(self) -> str:
        return "title"

    @property
    def name(self) -> str:
        classname = self.view.__class__.__name__
        diagram_type = getattr(
            Terminology, camel_case(classname).replace("View", "")
        ).value
        return f"[{diagram_type}] {self.title}"

    @property
    def csv_data(self):
        data = super().csv_data
        data.update(
            {
                "c4Name": self.name,
                "c4Description": self.description,
                "id": "title",
                "styleKey": self.style,
                "labelKey": self.style,
                "left": self.position.x,
                "top": self.position.y,
                "width": self.dimensions.x,
                "height": self.dimensions.y,
            }  # pyright: reportGeneralTypeIssues=false
        )
        return data
