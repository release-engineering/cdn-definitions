from cdn_definitions._impl import load_data


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
