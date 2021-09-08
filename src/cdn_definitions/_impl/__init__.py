import json
import os
import warnings

import requests
import yaml

# Requests module historically (>=0.8.0) bundled its own urllib3,
# however it may depend on how the module is installed, as some
# distributions (e.g. RHEL-7) ship the same version of requests
# module without bundled urllib3 and add a compat layer aliasing
# requests.packages.urllib3 to non-bundled urllib3.
# New versions (>=2.16) of the requests module stopped bundling
# urllib3 and added a different backwards-compat layer to retain
# requests.packages.* imports, however that layer is nontransparent
# to static analyzers such as pylint, hence the disable=import-error
# annotation even though the actual import still works.
from requests.packages.urllib3.util.retry import Retry  # pylint: disable=import-error

# It is preferred to return the data as immutable when possible
try:
    from frozendict import frozendict
except ImportError:  # pragma: no cover
    # If frozendict is not available, fall back to builtin dict
    frozendict = dict  # pylint: disable=invalid-name
try:
    from frozenlist2 import frozenlist
except ImportError:  # pragma: no cover
    # If frozenlist is not available, fall back to builtin list
    frozenlist = list  # pylint: disable=invalid-name


def freeze(node):
    """
    Converts dict to frozendict and list to frozenlist.
    """
    if isinstance(node, list):
        # Iterating using index instead of enumeration
        # so we can replace the list items in place
        for index in range(len(node)):  # pylint: disable=consider-using-enumerate
            node[index] = freeze(node[index])
        return frozenlist(node)
    if isinstance(node, dict):
        for key, value in node.items():
            node[key] = freeze(value)
        return frozendict(node)
    return node


def parsed(data, ext):
    """
    Parses a JSON or YAML string or a requests.Response object.
    """
    is_response = isinstance(data, requests.Response)
    if ext.lower() == ".json":
        parsed_data = data.json() if is_response else json.loads(data)
    else:
        parsed_data = yaml.safe_load(data.text if is_response else data)
    return freeze(parsed_data)


def get_remote_data(url, session=None):
    """
    Creates a requests session with retries. If the request was successful, returns the response.
    """
    retry_strategy = Retry(
        status_forcelist=[429, 500, 502, 503, 504],
    )

    if not session:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
        session.mount(url, adapter)

    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response


def get_local_data(data_path):
    """
    Given a valid path to a file, returns the contents of the file.
    """
    with open(data_path, "rb") as data_file:
        return data_file.read()


def get_data(data_paths, session=None):
    """
    Returns the parsed data at a URL or local file path.
    If data cannot be loaded, raises a RuntimeError.
    """
    for path in data_paths:
        _, ext = os.path.splitext(path)

        if path.startswith("http"):
            return parsed(get_remote_data(path, session), ext)

        if os.path.exists(path):
            return parsed(get_local_data(path), ext)
    raise RuntimeError("Could not load data")


def load_data(source=None, session=None):
    """Loads data from a YAML or JSON file into a Python object. If a requests.Session is provided
    in the "session" parameter, any HTTP request issued while loading data will use the given
    session.

    Args:
        source (str, optional): A local path or URL to a JSON or YAML data file.
        session (requests.Session, optional): A session to provide to HTTP requests.

    Returns:
        The data from the local path or URL, coerced into a Python object.

    Raises:
        RuntimeError: If all attempted data sources are invalid, a RuntimeError will be raised.

    """
    if source is None:
        # Load data from first existing of these
        candidate_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.yaml"),
            "/usr/share/cdn-definitions/data.yaml",
        ]

        # If env var is set, it takes highest precedence
        if "CDN_DEFINITIONS_PATH" in os.environ:
            candidate_paths.insert(0, os.environ["CDN_DEFINITIONS_PATH"])

        return get_data(candidate_paths, session)
    return get_data([source], session)


def load_schema():
    """
    Loads the `schema.json` file provided with the cdn-definitions package into a Python object.

    Returns:
        The cdn-definitions schema, coerced into a Python object.
    """
    schema_filename = os.path.join(os.path.dirname(__file__), "../schema.json")
    with open(schema_filename) as schema:  # pylint: disable=unspecified-encoding
        return json.load(schema)


DATA = load_data()


class PathAlias(object):
    """Represents an alias between one CDN path and another, generally
    used to make two directory trees on CDN serve identical content."""

    def __init__(self, **kwargs):
        warnings.warn(
            "PathAlias is deprecated - please use load_data instead",
            DeprecationWarning,
        )
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
    warnings.warn(
        "rhui_aliases is deprecated - please use load_data instead",
        DeprecationWarning,
    )
    return [PathAlias(**elem) for elem in DATA["rhui_alias"]]


def origin_aliases():
    """Returns:
    list[:class:`~PathAlias`]
        A list of aliases relating to origin paths.
    """
    warnings.warn(
        "origin_aliases is deprecated - please use load_data instead",
        DeprecationWarning,
    )
    return [PathAlias(**elem) for elem in DATA["origin_alias"]]
