from cdn_definitions._impl import load_data
from mock import patch
import pytest
import requests


def test_can_load_custom_data(monkeypatch, tmpdir):
    json_file = tmpdir.join("myfile.json")
    json_file.write('{"hello": "world"}')

    # If we set an env var pointing at the above JSON file, the library
    # should load it instead of the bundled data
    monkeypatch.setenv("CDN_DEFINITIONS_PATH", str(json_file))
    data = load_data()

    assert data == {"hello": "world"}


def test_can_load_custom_data_from_source(monkeypatch, tmpdir):
    json_file = tmpdir.join("myfile.json")
    json_file.write('{"hello": "world"}')

    # If we set an env var pointing at the above JSON file, the library
    # should load it instead of the bundled data
    data = load_data(source=str(json_file))

    assert data == {"hello": "world"}


def test_can_load_url_from_env_var(monkeypatch):
    with patch("cdn_definitions._impl.requests.get") as r:
        r.return_value = {"hello": "world"}
        monkeypatch.setenv("CDN_DEFINITIONS_PATH", "https://example")
        data = load_data()
    assert data == {"hello": "world"}


def test_can_load_url_from_source_arg(monkeypatch):
    with patch("cdn_definitions._impl.requests.get") as r:
        r.return_value = {"hello": "world"}
        data = load_data("https://example.com")

    assert data == {"hello": "world"}


def test_invalid_source(monkeypatch, tmpdir):
    with pytest.raises(RuntimeError, match="Could not load data"):
        data = load_data(source="test")
