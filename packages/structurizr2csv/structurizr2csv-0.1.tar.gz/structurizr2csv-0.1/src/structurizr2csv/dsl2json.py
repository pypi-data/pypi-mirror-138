import json
import os
import socket
import textwrap
import warnings
from pathlib import Path
from typing import Optional

from structurizr2csv.settings import (
    DOCKER_MOUNT_TARGET,
    DOCKER_STRUCTURIZR_MOUNT_TARGET,
)

# c.f. https://github.com/docker/docker-py/issues/2928
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import docker


class DSL2JSON:
    """Convert structurizr DSL to JSON and apply GraphViz autolayout."""

    def __init__(self, input_path: Path):
        self.input_path = input_path

    @property
    def output_path(self) -> Path:
        return self.input_path.with_suffix(".json")  # i.e. *.json

    @property
    def tmp_dsl_path(self) -> Path:
        return self.input_path.with_suffix(".autolayout.dsl")  # i.e. *.autolayout.dsl

    @property
    def tmp_output_path(self) -> Path:
        return self.tmp_dsl_path.with_suffix(".json")  # i.e. *.autolayout.json

    @property
    def autolayout_dsl_content(self):
        """Extend the workspace to add GraphViz autolayout."""
        # c.f. https://github.com/structurizr/cli/issues/62#issuecomment-999623728
        return textwrap.dedent(
            f"""
workspace extends {self.input_path.name} {{
    !script groovy {{
        new com.structurizr.graphviz.GraphvizAutomaticLayout().apply(workspace);
    }}
}}"""
        )

    def clean_temporary_artifacts(self):
        """Remove all temporary files that have been created during the conversion."""
        if self.tmp_output_path.exists():
            with open(self.tmp_output_path, "r") as fp:
                for key, values in json.load(fp)["views"].items():
                    if key != "configuration":
                        for view in values:
                            view_key = view["key"]
                            for suffix in (".dot", ".dot.svg"):
                                (self.input_path.parent / f"{view_key}{suffix}").unlink(
                                    missing_ok=True
                                )

        self.tmp_dsl_path.unlink(missing_ok=True)

    def get_docker_host_working_directory(
        self, client: docker.client.DockerClient
    ) -> Optional[str]:
        """Returns the host's working directory if we are running in docker, else None.

        If we are currently running in docker, the host's working directory must be the
        source path of the mounted /structurizr2csv volume.
        """
        # In Makefile, we fake "docker in docker" (dind) using the socket solution.
        # So here, we assume to be inside a docker container and we will run another
        # container using the existing docker server that is running on the host.
        # So the mount source path that we will pass to structurizr's docker must
        # be the host's source path, and not the target in structurizr2csv's container.
        # c.f. https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/
        try:
            container_info = client.api.inspect_container(socket.gethostname())
        except docker.errors.NotFound:  # pyright: reportGeneralTypeIssues=false
            # we are running in docker
            return None
        else:
            path = [
                mount
                for mount in container_info["Mounts"]
                if mount["Destination"] == DOCKER_MOUNT_TARGET
            ][0]["Source"]

            print(f"The mounted volume host path is {path}")  # e.g. /d/structurizr2csv
            return path

    def get_docker_host_workspace_directory(
        self, client: docker.client.DockerClient
    ) -> str:
        """Returns the host's workspace directory (that contains the DSL/JSON files)."""
        new_volume_source_path = os.path.realpath(self.input_path.parent)

        mounted_volume_host_path = self.get_docker_host_working_directory(client)
        if mounted_volume_host_path:  # we are currently in docker
            new_volume_source_path = new_volume_source_path.replace(
                DOCKER_MOUNT_TARGET, mounted_volume_host_path
            )

        # e.g. /d/structurizr2csv/examples
        print(f"The new volume source path will be {new_volume_source_path}")
        return new_volume_source_path

    def convert(self):
        with open(self.tmp_dsl_path, "w") as fp:
            fp.write(self.autolayout_dsl_content)

        # c.f. https://github.com/docker/docker-py/issues/2928
        # TODO: remove this catch when docker package has been updated
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            client = docker.from_env()
            try:
                client.containers.run(
                    image="souliane/structurizr-cli-with-graphviz",
                    command=(f'export -w "{self.tmp_dsl_path.name}" -f json'),
                    volumes={
                        self.get_docker_host_workspace_directory(client): {
                            "bind": DOCKER_STRUCTURIZR_MOUNT_TARGET,
                            "mode": "rw",
                        }
                    },
                    auto_remove=True,
                )
            finally:
                self.clean_temporary_artifacts()
                client.close()

        self.output_path.unlink(missing_ok=True)
        self.tmp_output_path.rename(self.output_path)

        return self.output_path
