from collections import defaultdict
from typing import Dict, Optional, Set

from pydantic import BaseModel, Field

from structurizr2csv.style import Style
from structurizr2csv.utils import auto_index
from structurizr2csv.workspace_extension import Element


class Connector(BaseModel):
    """Convert a relationship in structurizr to a connector in diagrams.net"""

    id: str = Field(default_factory=lambda: auto_index("c", Connector))

    description: str
    technology: Optional[str]

    # Map structurizr destination element to the source elements
    instances: Dict[Element, Set[Element]] = Field(
        default_factory=lambda: defaultdict(set)
    )

    @property
    def label(self):
        return (
            f"{self.description}<br>[{self.technology}]"
            if self.technology
            else self.description
        )

    def __str__(self):
        return (
            f'# connect: {{"from": "{self.id}","to": "id",'
            f'"invert": "true","label": "{self.label}",'
            f'"style": "{Style.connector}"}}\n'
        )
