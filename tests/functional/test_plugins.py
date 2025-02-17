import pytest

from ape.plugins import _get_name_from_install
from ape_plugins.utils import PluginInstallRequest

EXPECTED_PLUGIN_NAME = "plugin_name"


@pytest.mark.parametrize(
    "name",
    (
        f"{EXPECTED_PLUGIN_NAME}_0_4_1_dev1_g048574f",
        f"{EXPECTED_PLUGIN_NAME}_0_4_1_dev1_g791b83a_d20220817",
        f"{EXPECTED_PLUGIN_NAME}_0_4_0",
    ),
)
def test_get_name_from_install_editable_examples(name):
    editable_name = f"__editable___ape_{name}_finder"
    actual = _get_name_from_install(editable_name)
    assert actual == f"ape_{EXPECTED_PLUGIN_NAME}"


class TestPluginInstallRequest:
    @pytest.mark.parametrize(
        "name", ("ape-foo-bar", "ape-foo-bar", "ape_foo_bar", "foo-bar", "foo_bar")
    )
    def test_names(self, name):
        request = PluginInstallRequest(name=name)
        assert request.name == "foo-bar"
        assert request.package_name == "ape-foo-bar"
        assert request.module_name == "ape_foo_bar"

    def test_parse_obj_when_version_included_with_name(self):
        # This allows parsing requirements files easier
        request = PluginInstallRequest(name="ape-foo-bar==0.5.0")
        assert request.name == "foo-bar"
        assert request.version == "0.5.0"

    @pytest.mark.parametrize("version", ("0.5.0", "v0.5.0", "0.5.0a123"))
    def test_version(self, version):
        request = PluginInstallRequest(name="foo", version=version)
        assert request.version == version

    def test_install_str_without_version(self):
        request = PluginInstallRequest(name="foo-bar")
        actual = request.install_str
        assert actual == "ape-foo-bar"

    def test_install_str_with_version(self):
        request = PluginInstallRequest(name="foo-bar", version="0.5.0")
        actual = request.install_str
        assert actual == "ape-foo-bar==0.5.0"
