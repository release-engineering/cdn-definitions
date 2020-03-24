import json
import os

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json")
DATA = json.load(open(JSON_PATH))


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
