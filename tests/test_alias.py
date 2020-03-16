import pytest

from cdn_definitions import PathAlias, origin_aliases, rhui_aliases


def test_rhui_sanity():
    """rhui_aliases must exist with expected properties"""
    paths = rhui_aliases()

    # There should be some items
    assert paths

    # Paths should have src/dest the correct way around
    for path in paths:
        assert "/rhui" in path.src
        assert "/rhui" not in path.dest


def test_origin_sanity():
    """origin_aliases must exist with expected properties"""
    paths = origin_aliases()

    # There should be some items
    assert paths

    # Paths should relate to origin
    for path in paths:
        assert "/origin" in path.src
        assert "/origin" in path.dest


def test_enforced_absolute():
    """PathAlias raises if given relative paths"""
    with pytest.raises(ValueError) as exc_info:
        PathAlias(src="/src", dest="dest")
    assert "relative path" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        PathAlias(src="src", dest="/dest")
    assert "relative path" in str(exc_info.value)


def test_enforced_nonequal():
    """PathAlias raises if given equal paths"""
    with pytest.raises(ValueError) as exc_info:
        PathAlias(src="/src", dest="/src")
    assert "/src cannot alias itself" in str(exc_info.value)
