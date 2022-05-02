import os
import shutil
from core import CommonSettings

VALUES = {
    "pippo": 3,
    "pluto": "ciao",
    "paperino": True,
    "minni": False,
    "luigi": "ciao ciao",
    "mario": -1,
    "yoshi": 0,
}

CHANGE_1 = {"pippo": 18}

NEW_VALUES_1 = {
    "pippo": 18,
    "pluto": "ciao",
    "paperino": True,
    "minni": False,
    "luigi": "ciao ciao",
    "mario": -1,
    "yoshi": 0,
}

CHANGE_2 = {"minni": True}

NEW_VALUES_2 = {
    "pippo": 18,
    "pluto": "ciao",
    "paperino": True,
    "minni": True,
    "luigi": "ciao ciao",
    "mario": -1,
    "yoshi": 0,
}

CHANGE_3 = {"pluto": "miao", "paperino": False, "minni": True}

NEW_VALUES_3 = {
    "pippo": 18,
    "pluto": "miao",
    "paperino": False,
    "minni": True,
    "luigi": "ciao ciao",
    "mario": -1,
    "yoshi": 0,
}


def delete_module_folder(module_name="test", path="tests"):
    # elimino le possibili tracce di file salvati precedentemente
    file_dir = f"{path}/BOB_CONFIG/{module_name}/"
    if os.path.exists(f"{file_dir}/config.json"):
        os.remove(f"{file_dir}/config.json")
        os.removedirs(file_dir)


def delete_config_folder(path="tests"):
    folder = f"{path}/BOB_CONFIG"

    if os.path.exists(folder):
        shutil.rmtree(folder)


class TestCommonSettings:
    def setup(self):
        delete_config_folder()

    def test_create_dict(self):
        settings = CommonSettings(VALUES, "test")
        assert settings.values == VALUES

        delete_config_folder()

    def test_create_common_settings(self):
        settings1 = CommonSettings(VALUES, "test1")
        settings2 = CommonSettings(settings1, "test2")
        assert settings2.values == VALUES

        delete_config_folder()

    def test_save_and_restore(self):
        # testo il salvataggio e vedo se il file riaperto è uguale
        settings1 = CommonSettings(VALUES, "test")
        settings1.save("tests")
        settings2 = CommonSettings({}, "test")
        settings2.load("tests")
        assert settings1.values == settings2.values

        delete_config_folder()

    def test_new_settings(self):
        settings = CommonSettings(VALUES, "test")

        settings.new_settings(CHANGE_1, "tests")
        assert NEW_VALUES_1 == settings.values

        settings.new_settings(CHANGE_2, "tests")
        assert NEW_VALUES_2 == settings.values

        settings.new_settings(CHANGE_3, "tests")
        assert NEW_VALUES_3 == settings.values

        delete_config_folder()
