__author__ = "Vanessa Sochat, Alec Scott"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat and Alec Scott"
__license__ = "Apache-2.0"

from paks.logger import logger
import paks.utils
from .base import ContainerTechnology, ContainerName

from datetime import datetime
from glob import glob
import re
import os
import shutil


class SingularityContainer(ContainerTechnology):
    """
    A Singularity container controller.

    All container controllers should have the same general interface.
    """

    def __init__(self):
        try:
            from spython.main import Client

            self.client = Client
        except:
            logger.exit("singularity python (spython) is required to use singularity.")
        super(SingularityContainer, self).__init__()

    def registry_pull(self, module_dir, container_dir, config, tag):
        """
        Given a module directory, container config, and tag, pull the container
        """
        pull_type = config.get_pull_type()

        # Preserve name and version of container if it's ever moved
        container_path = os.path.join(
            container_dir, "%s-%s-%s.sif" % (config.flatname, tag.name, tag.digest)
        )

        # We pull by the digest
        if pull_type in ["docker", "oras"]:
            container_uri = "%s://%s@%s" % (
                pull_type,
                config.docker or config.oras,
                tag.digest,
            )
        elif pull_type == "gh":
            container_uri = "gh://%s/%s:%s" % (config.gh, tag.digest, tag.name)

        # Pull new containers
        if not os.path.exists(container_path):
            self.pull(container_uri, container_path)

        # Exit early if there is an issue
        if not os.path.exists(container_path):
            container_path = None
        return container_path

    def shell(self, image):
        """
        Interactive shell into a container image.
        """
        self.client.shell(image)

    def pull(self, uri, dest):
        """
        Pull a container to a destination
        """
        if re.search("^(docker|shub|https|oras)", uri):
            return self._pull_regular(uri, dest)
        elif uri.startswith("gh://"):
            return self._pull_github(uri, dest)

    def _pull_regular(self, uri, dest):
        """
        Pull a URI that Singularity recognizes
        """
        pull_folder = os.path.dirname(dest)
        name = os.path.basename(dest)
        return self.client.pull(uri, name=name, pull_folder=pull_folder)

    def inspect(self, image):
        """
        Inspect an image and return metadata.
        """
        return self.client.inspect(image)

    def _pull_github(self, uri, dest=None):
        """
        Pull a singularity-deploy container to a destination
        """
        # Assemble the url based on the container uri
        uri = uri.replace("gh://", "", 1)

        # repository name and image prefix
        repo = "/".join(uri.split("/")[0:2])
        prefix = repo.replace("/", "-")

        # The tag includes release and contianer tag (e.g., 0.0.1:latest)
        tag = uri.replace(repo, "", 1).strip("/")
        github_tag, container_tag = tag.split(":", 1)

        # Assemble the artifact url
        url = "https://github.com/%s/releases/download/%s/%s.%s.sif" % (
            repo,
            github_tag,
            prefix,
            container_tag,
        )

        # If no destination, default to present working directory
        if not dest:
            dest = os.path.basename(url)
        name = os.path.basename(dest)
        return self.client.pull(url, name=name, pull_folder=os.path.dirname(dest))

    def test_script(self, image, test_script):
        """
        Given a test file, run it and respond accordingly.
        """
        command = ["singularity", "exec", image, "/bin/bash", test_script]
        result = shpc.utils.run_command(command)

        # We can't run on incompatible hosts
        if (
            "the image's architecture" in result["message"]
            and result["return_code"] != 0
        ):
            logger.warning(
                "Cannot run test for incompatible architecture: %s" % result["message"]
            )
            return 0

        # Return code
        return result["return_code"]
