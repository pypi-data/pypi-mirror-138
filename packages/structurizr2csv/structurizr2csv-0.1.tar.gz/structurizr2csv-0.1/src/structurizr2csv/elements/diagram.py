from collections import OrderedDict
from functools import cached_property
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

from pydantic import BaseModel, Field

from structurizr2csv.coordinates import Position
from structurizr2csv.elements.base_box import BaseBox
from structurizr2csv.elements.box import Box
from structurizr2csv.elements.connector import Connector
from structurizr2csv.elements.group import Group
from structurizr2csv.elements.legend import Legend
from structurizr2csv.elements.title import Title
from structurizr2csv.enums import Terminology
from structurizr2csv.settings import LEGEND_OFFSET_FROM_TITLE
from structurizr2csv.style import Style
from structurizr2csv.workspace import Component, Container, Model, Person
from structurizr2csv.workspace_extension import View


class Diagram(BaseModel):
    """Convert a view in structurizr to a diagram in diagrams.net"""

    class Config:
        keep_untouched = (cached_property,)

    view: View
    model: Model
    output_path: Path

    # Map relationship's description to diagram.net connectors, so we can
    # create a single object for all connectors sharing the same description
    connectors: Dict[Tuple[str], Connector] = Field(default_factory=dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # I miss a better solution... c.f. structurizr2csv.utils.auto_index
        try:
            Connector.reset_counter()
        except AttributeError:  # Connector has never been instantiated yet
            pass
        try:
            Group.reset_counter()
        except AttributeError:  # Group has never been instantiated yet
            pass

    @property
    def connector_columns(self) -> str:
        """Return the list of comma-separated connectors' IDs"""
        return ",".join(connector.id for connector in self.connectors.values())

    @cached_property
    def boxes(self) -> List[Box]:
        """Return all boxes for this structurizr view"""
        return [
            Box(element=element)
            for element in sorted(
                self.view.elements,
                key=lambda element: int(
                    element.id
                ),  # pyright: reportGeneralTypeIssues=false
            )
        ]

    @cached_property
    def primary_children(self) -> List[Box]:
        """Return all children of the primary group for this view.

        Depending on the view's scope, this could be all boxes that are internal
        to the company, or all containers of a given software system...
        """
        key = None
        match self.view.__class__.__name__:
            case "SystemLandscapeView" | "SystemContextView":
                if self.view.enterpriseBoundaryVisible:
                    key = attrgetter("is_internal")
            case "ContainerView":
                key = lambda box: isinstance(box.definition, Container)  # noqa: E731
            case "ComponentView":
                key = lambda box: isinstance(box.definition, Component)  # noqa: E731

        return list(filter(key, self.boxes)) if key else []

    @cached_property
    def primary_group(self) -> Optional[Group]:
        """Return the primary group for this view.

        Depending on the view's scope, this could be the company,
        or a given software system, or a given container...
        """
        match self.view.__class__.__name__:
            case "SystemLandscapeView" | "SystemContextView":
                if self.view.enterpriseBoundaryVisible:
                    try:
                        name = self.model.enterprise.name  # type:ignore
                    except AttributeError:
                        assert self.model.enterprise is None
                        return None
                    else:
                        c4_type = Terminology.enterprise
                else:
                    return None
            case "ContainerView":
                name = self.model.object_ids[self.view.softwareSystemId].name
                c4_type = Terminology.softwareSystem
            case "ComponentView":
                name = self.model.object_ids[self.view.containerId].name
                c4_type = Terminology.container
            case _:
                return None

        children = self.primary_children + self.secondary_groups
        group = Group.compute_from_boxes(children, name=name, c4_type=c4_type)
        for child in children:
            if child.parent is None:  # leave the boxes that are in secondary groups
                child.parent = group
        return group

    @cached_property
    def secondary_groups(self) -> List[Group]:
        """Returns the secondary groups.

        Those are necessarily user defined groups that have no particular
        meaning to structurizr.
        """
        groups = []
        for name, boxes in groupby(self.boxes, attrgetter("definition.group")):
            children = [
                box
                for box in boxes
                if box in self.primary_children or isinstance(box.definition, Person)
            ]
            if children and name:
                group = Group.compute_from_boxes(
                    children,
                    name=name,
                )
                groups.append(group)
                for box in children:
                    box.parent = group
        return groups

    def connectors_to_csv(self) -> Iterator[str]:
        """Yield the CSV rows for all connectors."""
        for relationship in self.view.relationships or []:
            definition = relationship.definition
            keys = OrderedDict(
                (
                    ("description", definition.description),
                    ("technology", definition.technology),
                )
            )

            try:
                connector = self.connectors[keys.values()]
            except KeyError:
                connector = self.connectors.setdefault(keys.values, Connector(**keys))
                yield str(connector)  # str representation for diagrams.net CSV

            connector.instances[definition.destinationId].add(definition.sourceId)

    def boxes_to_csv(self) -> Iterator[str]:
        """Yield the CSV rows for all boxes."""
        for box in self.boxes:
            yield box.to_csv()
            for connector in self.connectors.values():  # append connectors data
                yield ","
                if box.element.id in connector.instances.keys():
                    yield (
                        '"{}"'.format(
                            ",".join(sorted(connector.instances[box.element.id]))
                        )
                    )
            yield "\n"

    def make_title(self) -> Title:
        """Create the diagram's title instance."""
        title = self.view.title
        if not title:
            match self.view.__class__.__name__:
                case "SystemLandscapeView":
                    try:
                        title = (
                            self.model.enterprise.name
                        )  # pyright: reportOptionalMemberAccess=false
                    except AttributeError:
                        assert self.model.enterprise is None
                        title = ""
                case "SystemContextView" | "ContainerView":
                    title = self.model.object_ids[self.view.softwareSystemId].name
                case "ComponentView":
                    title = self.model.object_ids[self.view.containerId].name
        return Title(view=self.view, title=title or "")

    def write_headers(self, fp):
        """Write diagrams.net CSV headers.

        This is more or less where we tell diagrams.net which CSV columns exist,
        and if they are used to hold meta data, editable data or connections.
        """
        data_columns = ",".join(BaseBox._data_columns)
        meta_columns = ",".join(BaseBox._meta_columns)

        columns = f"{meta_columns},{self.connector_columns}"

        fp.write(f"# ignore: {columns}\n")
        fp.write(f"{data_columns},{columns}\n")

    def write_group(self, fp, group: Group):
        """Write a group to CSV format."""
        fp.write("{}{}\n".format(group.to_csv(), "," * len(self.connectors)))

    def write_title(self, title: Title, fp):
        """Write the diagram's title to CSV format."""
        fp.write("{}{}\n".format(title.to_csv(), "," * len(self.connectors)))

    def write_legend(self, title: Title, fp):
        """Write the diagram's legend to CSV format."""
        for row in Legend(
            view=self.view,
            position=Position(
                x=title.position.x,
                y=title.position.y + title.dimensions.y + LEGEND_OFFSET_FROM_TITLE,
            ),
            box_types=set(box.box_type for box in self.boxes),
        ).to_csv():
            fp.write("{}{}\n".format(row, "," * len(self.connectors)))

    def process(self):
        """Export the structurizr view to diagrams.net CSV format."""
        styles = Style.build_headers()

        output_filepath = self.output_path / f"{self.view.key}.csv"

        with open(output_filepath, "w") as fp:
            fp.write(f"## {self.view.key}\n{styles}\n")

            for output in self.connectors_to_csv():
                fp.write(output)

            self.write_headers(fp)

            if self.primary_group:
                self.write_group(fp, self.primary_group)

            for group in self.secondary_groups:
                group.parent = self.primary_group
                self.write_group(fp, group)

            for output in self.boxes_to_csv():
                fp.write(output)

            title = self.make_title()
            self.write_title(title, fp)
            self.write_legend(title, fp)

        print(f"Created/updated {output_filepath}")
