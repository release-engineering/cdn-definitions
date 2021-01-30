import json
import os

from cdn_definitions import api


def test_load_schema_api():
    schema = api.schema()
    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "cdn_definitions",
            "schema.json",
        )
    ) as f:
        local_schema = json.load(f)
    assert schema == local_schema


def test_load_data_api(tmpdir):
    json_file = tmpdir.join("myfile.json")
    json_file.write('{"hello": "world"}')
    data = api.data(source=str(json_file))
    assert data == {"hello": "world"}
