import pytest
import json
import yaml

from . import ROOT_PATH


@pytest.mark.parametrize("basename", ["data", "schema"])
def test_data_sync(basename):
    """Verify that .json files are up-to-date with .yaml files."""
    yaml_path = ROOT_PATH / f"src/cdn_definitions/{basename}.yaml"
    json_path = ROOT_PATH / f"src/cdn_definitions/{basename}.json"

    with yaml_path.open(encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    with json_path.open(encoding="utf-8") as f:
        json_data = json.load(f)

    message = (
        f"{yaml_path} and {json_path} differ! Consider running `scripts/make-json'."
    )
    assert yaml_data == json_data, message
