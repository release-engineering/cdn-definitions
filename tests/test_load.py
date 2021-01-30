import os
import json

import pytest
import requests
import requests_mock

from cdn_definitions import load_data, load_schema


def test_can_load_custom_json_data(monkeypatch, tmpdir):
    json_file = tmpdir.join("myfile.json")
    json_file.write('{"hello": "json"}')

    # If we set an env var pointing at the above JSON file, the library
    # should load it instead of the bundled data
    monkeypatch.setenv("CDN_DEFINITIONS_PATH", str(json_file))
    data = load_data()

    assert data == {"hello": "json"}


def test_can_load_custom_yaml_data(monkeypatch, tmpdir):
    yaml_file = tmpdir.join("myfile.yaml")
    yaml_file.write("hello: yaml")

    # If we set an env var pointing at the above YAML file, the library
    # should load it instead of the bundled data
    monkeypatch.setenv("CDN_DEFINITIONS_PATH", str(yaml_file))
    data = load_data()

    assert data == {"hello": "yaml"}


@pytest.mark.parametrize(
    "file_name, file_contents, expected",
    [
        ("myfile.json", '{"french": "toast"}', {"french": "toast"}),
        ("myfile.yaml", "french: fries", {"french": "fries"}),
    ],
)
def test_can_load_local_data_from_source(tmpdir, file_name, file_contents, expected):
    json_file = tmpdir.join(file_name)
    json_file.write(file_contents)

    data = load_data(source=str(json_file))

    assert data == expected


def test_can_load_yaml_url_from_env_var(monkeypatch):
    with requests_mock.Mocker() as m:
        m.get("https://test.com/data.yaml", text='{"water": "melon"}')
        monkeypatch.setenv("CDN_DEFINITIONS_PATH", "https://test.com/data.yaml")
        data = load_data()

    assert data == {"water": "melon"}


def test_can_load_json_url_from_env_var(monkeypatch):
    with requests_mock.Mocker() as m:
        m.get("https://test.com/data.json", json={"green": "bean"})
        monkeypatch.setenv("CDN_DEFINITIONS_PATH", "https://test.com/data.json")
        data = load_data()

    assert data == {"green": "bean"}


def test_can_load_yaml_url_from_source_arg(monkeypatch):
    with requests_mock.Mocker() as m:
        m.get("http://test.com/data.yaml", text='{"grape": "fruit"}')
        data = load_data("http://test.com/data.yaml")

    assert data == {"grape": "fruit"}


def test_can_load_json_url_from_source_arg(monkeypatch):
    with requests_mock.Mocker() as m:
        m.get("http://test.com/data.json", json={"green": "pepper"})
        data = load_data("http://test.com/data.json")

    assert data == {"green": "pepper"}


def test_invalid_data_source():
    with pytest.raises(RuntimeError, match="Could not load data"):
        data = load_data(source="test")


def test_load_schema():
    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "cdn_definitions",
            "schema.json",
        )
    ) as f:
        local_schema = json.load(f)

    assert load_schema() == local_schema
