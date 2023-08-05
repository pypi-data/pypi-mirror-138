#!python3
# avoid absolute path in shebang, so that it also works on windows

import argparse
import glob
from pathlib import Path

from structurizr2csv.dsl2json import DSL2JSON
from structurizr2csv.elements.diagram import Diagram
from structurizr2csv.utils import Directory
from structurizr2csv.workspace import Workspace
from structurizr2csv.workspace_extension import WorkspaceWrapper


class Converter:
    @classmethod
    def parse_args(cls) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description=(
                "Convert structurizr DSL or JSON (for describing C4 models) to "
                "diagrams.net CSV format"
            )
        )
        parser.add_argument(
            "input_path",
            type=Path,
            help=(
                "input workspace file, either *.dsl or *.json. "
                "If you pass a *.json file, it is expected to define the positions "
                "of each elements. If you pass a *.dsl file, it will be "
                "automatically transformed to JSON and GraphViz auto layout will "
                "be applied (this is done with the official Docker image for "
                "structurizr/cli, so you need a running Docker system for this to "
                "work with a *.dsl file). When using the '-a {dsl,json}' option, "
                "this must be the path to a directory."
            ),
        )
        parser.add_argument(
            "-a",
            "--all",
            type=str,
            choices=["dsl", "json"],
            dest="process_all",
            help="process all the files in 'input_path' that are of the given type",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=Path,
            dest="output_path",
            help=(
                "output base directory for the CSV files "
                "(workspace basename will be appended)"
            ),
            default="output",
        )
        return parser.parse_args()

    @classmethod
    def get_workspace(cls, filepath: Path) -> Workspace:
        with open(filepath, "r") as fp:
            return Workspace.parse_raw(fp.read())

    @classmethod
    def ensure_directory_exists(cls, directory: Path):
        Path(directory).mkdir(parents=True, exist_ok=True)

    def process_views(self, workspace: Workspace, output_path: Path):
        Directory.create_or_clean(output_path)

        for view in WorkspaceWrapper(workspace).iterate_views():
            Diagram(view=view, model=workspace.model, output_path=output_path).process()

    def process_workspace(self, input_path: Path, output_path: Path):
        workspace_suffix = input_path.suffix.lower()
        if workspace_suffix not in (".dsl", ".json"):
            raise RuntimeError("The workspace file suffix must be either .dsl or .json")

        if workspace_suffix == ".dsl":
            input_path = DSL2JSON(input_path).convert()

        self.ensure_directory_exists(output_path)
        workspace = self.get_workspace(input_path)

        self.process_views(workspace, output_path / input_path.stem)

    def run(self):
        args = self.parse_args()

        if not args.input_path.exists():
            raise FileNotFoundError(f"{args.input_path} does not exist")

        if args.process_all:
            for filename in glob.glob(f"{args.input_path}/*.{args.process_all}"):
                print(f"Converting {filename}")
                self.process_workspace(Path(filename), args.output_path)
        else:
            self.process_workspace(args.input_path, args.output_path)


def main():
    Converter().run()


if __name__ == "__main__":
    main()
