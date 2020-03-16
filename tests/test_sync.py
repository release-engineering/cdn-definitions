import os

import pytest
import json
import yaml

from . import ROOT_PATH


@pytest.fixture(params=["data", "schema"])
def any_basename(request):
    yield request.param


def test_data_sync(any_basename):
    """Verify that .json files are up-to-date with .yaml files."""
    yaml_path = os.path.join(ROOT_PATH, "cdn_definitions", "%s.yaml" % any_basename)
    json_path = os.path.join(ROOT_PATH, "cdn_definitions", "%s.json" % any_basename)

    with open(yaml_path) as f:
        yaml_data = yaml.load(f, yaml.SafeLoader)

    with open(json_path) as f:
        json_data = json.load(f)

    message = "%s and %s differ! Consider running `scripts/make-json'." % (
        yaml_path,
        json_path,
    )
    assert yaml_data == json_data, message
