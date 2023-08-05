import glob
import os
from pathlib import Path
from typing import List, Tuple

from structurizr2csv.settings import EDGE_STYLE

ASSETS_PATH = Path(__file__).parent


class Style:
    """Build static styles for diagrams.net"""

    @classmethod
    def get(cls, style: str) -> str:
        with open(ASSETS_PATH / f"styles/{style}.txt", "r") as fp:
            return fp.read().strip()

    @classmethod
    @property
    def connector(cls) -> str:
        return cls.get("connector") + str(EDGE_STYLE)

    @classmethod
    def get_definitions(cls, path: str, ignored: Tuple[str, ...] = None) -> List[str]:
        """Returns all definitions for the styles contained in `path` directory."""
        defs = []
        if ignored is None:
            ignored = tuple()

        for file in sorted(glob.glob(str(ASSETS_PATH / path / "*.txt"))):
            key = os.path.basename(file)[:-4]
            if key not in ignored:
                with open(file, "r") as fp:
                    content = fp.read().strip().replace('"', "'")
                    defs.append(f'"{key}": "{content}"')

        return defs

    @classmethod
    def build_headers(cls) -> str:
        """Build all the styling headers for diagrams.net CSV format."""
        element_styles = cls.get_definitions(
            "styles", ignored=("styles", "connector", "group")
        )
        labels = cls.get_definitions("labels")

        with open(ASSETS_PATH / "styles/styles.txt", "r") as fp:
            styles = fp.read().strip()

        return styles.format(
            element_styles=",\\\n#  ".join(element_styles),
            labels=",\\\n#  ".join(labels),
        )
