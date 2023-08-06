import pytest
from ckan.plugins import plugin_loaded


@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugin_loaded("thumbnailer")
