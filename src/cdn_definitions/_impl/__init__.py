import json
import os
import requests


def load_data(source=None):
    if source is None:
        # Load data from first existing of these
        candidate_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json"),
            "/usr/share/cdn-definitions/data.json",
        ]

        # If env var is set, it takes highest precedence
        if "CDN_DEFINITIONS_PATH" in os.environ:
            cdn_definitions_path = os.environ["CDN_DEFINITIONS_PATH"]
            candidate_paths.insert(0, cdn_definitions_path)
            if cdn_definitions_path.startswith("http"):
                return requests.get(cdn_definitions_path)
        existing_paths = [p for p in candidate_paths if os.path.exists(p)]
        return json.load(open(existing_paths[0]))
    if os.path.exists(source):
        return json.load(open(source))
    if source.startswith("http"):
        return requests.get(source)
    raise RuntimeError("Could not load data")


DATA = load_data()


class PathAlias(object):
    """Represents an alias between one CDN path and another, generally
    used to make two directory trees on CDN serve identical content."""

    def __init__(self, **kwargs):
        self.src = kwargs["src"]
        """Source path of mapping (e.g. "/content/rhel/dist/rhui")."""

        self.dest = kwargs["dest"]
        """Destination path of mapping (e.g. "/content/rhel/dist")."""

        # Enforce a few invariants:
        # absolute paths only
        if not self.src.startswith("/") or not self.dest.startswith("/"):
            raise ValueError("Attempted to construct PathAlias with relative path")

        # Equal src/dest is nonsensical
        if self.src == self.dest:
            raise ValueError("%s cannot alias itself!" % self.src)


def rhui_aliases():
    """Returns:
    list[:class:`~PathAlias`]
        A list of aliases relating to RHUI paths.
    """
    return [PathAlias(**elem) for elem in DATA["rhui_alias"]]


def origin_aliases():
    """Returns:
    list[:class:`~PathAlias`]
        A list of aliases relating to origin paths.
    """
    return [PathAlias(**elem) for elem in DATA["origin_alias"]]
