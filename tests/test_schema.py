import os

import pytest
import yaml
import jsonschema

from jsonschema import ValidationError

from . import ROOT_PATH

DATA_PATH = os.path.join(ROOT_PATH, "src", "cdn_definitions", "data.yaml")
SCHEMA_PATH = os.path.join(ROOT_PATH, "src", "cdn_definitions", "schema.yaml")


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


def test_invalid_signing_key(data, schema):
    """Verify that data using an invalid signing key does NOT match the schema."""

    data["signing_keys_mappings"]["platform"]["example_platform"]["ga_keys"] = "INVALID"
    with pytest.raises(ValidationError):
        jsonschema.validate(data, schema)


@pytest.mark.parametrize(
    "platform_full_version, platform_version",
    [("7", "7"), ("5.2", "5.3"), ("7", "5.2"), ("5.2", "7")],
)
def test_major_or_minor_regex(data, schema, platform_full_version, platform_version):
    """Validate the major_or_minor_version regex."""

    # cfme_version_mappings are a major_or_minor_version to major_or_minor_version mapping.
    data["cfme_version_mappings"][platform_full_version] = platform_version
    jsonschema.validate(data, schema)


@pytest.mark.parametrize(
    "test_data", ["latest_rhel_6_dist", "latest_rhel6_ga", "current_rhel_dist"]
)
def test_current_latest_rhel_string(data, schema, test_data):
    """Verify that data using invalid env_to_rhel_version_mappings strings do NOT
    match the schema."""

    data["env_to_releasever_mappings"]["prod"] = {test_data: "3.1"}
    data["env_to_releasever_mappings"]["stage"] = {test_data: "3.1"}
    data["env_to_releasever_mappings"]["qa"] = {test_data: "3.1"}
    with pytest.raises(ValidationError):
        jsonschema.validate(data, schema)
