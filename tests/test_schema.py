import pytest
import yaml
import jsonschema

from jsonschema import Draft7Validator, ValidationError

from . import ROOT_PATH

DATA_PATH = ROOT_PATH / "src/cdn_definitions/data.yaml"
SCHEMA_PATH = ROOT_PATH / "src/cdn_definitions/schema.yaml"
HISTORICAL_DATA_DIR = ROOT_PATH / "tests/historical-data"


def validate(instance):
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    jsonschema.validate(instance, schema, format_checker=Draft7Validator.FORMAT_CHECKER)


@pytest.fixture(name="data")
def fixture_data():
    with DATA_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def historical_data():
    for f in HISTORICAL_DATA_DIR.iterdir():
        with f.open(encoding="utf-8") as d:
            yield f.name, yaml.safe_load(d)


def test_data_matches_schema(data):
    """Verify that the content of data.yaml matches the declared schema."""

    validate(data)


@pytest.mark.parametrize("name, historical_data", historical_data())
def test_historical_data_matches_schema(name, historical_data):
    """Verify that all the historical data.yaml files that were compatible preceding
    the schema changes matches the currently declared schema i.e. current schema is
    backward compatible."""

    validate(historical_data)


def test_bogus_data_not_match_schema():
    """Verify that a completely bogus object does NOT match the schema.

    This is a sanity check to ensure that the schema is doing something."""

    with pytest.raises(ValidationError):
        validate({"bad": "data"})


def test_relative_path_not_match_schema(data):
    """Verify that data using a relative path does NOT match the schema."""

    data["rhui_alias"][0]["dest"] = "dest-path"
    with pytest.raises(ValidationError):
        validate(data)


def test_invalid_signing_key(data):
    """Verify that data using an invalid signing key does NOT match the schema."""

    data["signing_keys_mappings"]["platform"]["example_platform"]["ga_keys"] = "INVALID"
    with pytest.raises(ValidationError):
        validate(data)


@pytest.mark.parametrize(
    "platform_full_version, platform_version",
    [("7", "7"), ("5.2", "5.3"), ("7", "5.2"), ("5.2", "7")],
)
def test_major_or_minor_regex(data, platform_full_version, platform_version):
    """Validate the major_or_minor_version regex."""

    # cfme_version_mappings are a major_or_minor_version to major_or_minor_version mapping.
    data["cfme_version_mappings"][platform_full_version] = platform_version
    validate(data)


@pytest.mark.parametrize(
    "test_data", ["latest_rhel_6_dist", "latest_rhel6_ga", "current_rhel_dist"]
)
def test_current_latest_rhel_string(data, test_data):
    """Verify that data using invalid env_to_rhel_version_mappings strings do NOT
    match the schema."""

    data["env_to_releasever_mappings"]["prod"] = {test_data: "3.1"}
    data["env_to_releasever_mappings"]["stage"] = {test_data: "3.1"}
    data["env_to_releasever_mappings"]["qa"] = {test_data: "3.1"}
    with pytest.raises(ValidationError):
        validate(data)


def test_repo_override_not_match_schema(data):
    """Verify that a repo override without if_* condition does NOT match the schema."""

    del data["repo_overrides"]["stage"][0]["if_match_id"]
    with pytest.raises(ValidationError):
        validate(data)
