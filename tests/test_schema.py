import os

import pytest
import yaml
import jsonschema

from jsonschema import ValidationError

from . import ROOT_PATH

DATA_PATH = os.path.join(ROOT_PATH, "cdn_definitions", "data.yaml")
SCHEMA_PATH = os.path.join(ROOT_PATH, "cdn_definitions", "schema.yaml")


@pytest.fixture
def schema():
    with open(SCHEMA_PATH) as f:
        return yaml.load(f, yaml.SafeLoader)


@pytest.fixture
def data():
    with open(DATA_PATH) as f:
        return yaml.load(f, yaml.SafeLoader)


def test_data_matches_schema(data, schema):
    """Verify that the content of data.yaml matches the declared schema."""

    jsonschema.validate(data, schema)


def test_bogus_data_not_match_schema(schema):
    """Verify that a completely bogus object does NOT match the schema.

    This is a sanity check to ensure that the schema is doing something."""

    with pytest.raises(ValidationError):
        jsonschema.validate({"bad": "data"}, schema)


def test_relative_path_not_match_schema(data, schema):
    """Verify that data using a relative path does NOT match the schema."""

    data["rhui_alias"][0]["dest"] = "dest-path"
    with pytest.raises(ValidationError):
        jsonschema.validate(data, schema)
