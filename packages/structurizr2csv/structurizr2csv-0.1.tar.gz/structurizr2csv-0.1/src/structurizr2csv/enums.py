from enum import Enum


class ParameterEnum(Enum):
    def __str__(self) -> str:
        return (
            f"{self.config.param}={self.value}" if self.value else ""
        )  # pyright: reportGeneralTypeIssues=false


class EdgeStyle(ParameterEnum):
    class Config:
        param = "edgeStyle"

    # this is not defined in jgraph API, but there are apparently no constant to
    # display the edge as a direct segment between the two linked elements
    # (even "segmentEdgeStyle" is not doing that).
    DIRECT = None

    # Redefine for our purpose some constants from
    # https://jgraph.github.io/mxgraph/docs/js-api/files/util/mxConstants-js.html
    ELBOW = "elbowEdgeStyle"
    ENTITY_RELATION = "entityRelationEdgeStyle"
    LOOP = "loopEdgeStyle"
    SIDE_TO_SIDE = "sideToSideEdgeStyle"
    TOP_TO_BOTTOM = "topToBottomEdgeStyle"
    ORTHOGONAL = "orthogonalEdgeStyle"
    SEGMENT = "segmentEdgeStyle"


class Tag(Enum):
    # tag that we use to display boxes in grey
    EXISTING_SYSTEM = "Existing System"

    # tags for which a dedicated style is defined
    HEXAGON = "Hexagon"
    CYLINDER = "Cylinder"
    PIPE = "Pipe"
    WEB_BROWSER = "Web Browser"

    # tag aliases
    DATABASE = "Database"
    MOBILE_APP = "Mobile App"


class Terminology(Enum):
    legend = "Legend"
    person = "Person"
    persons = "Persons"
    enterprise = "Enterprise"
    systemLandscape = "System Landscape"
    systemContext = "System Context"
    softwareSystem = "Software System"
    container = "Container"
    containers = "Containers"
    component = "Component"
    components = "Components"
    dynamic = "Dynamic"
    relationship = "Relationship"
