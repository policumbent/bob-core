import pytest


from core import Database, SqliteType, time
from core.exceptions import *


class TestDatabase:
    def setup(
        self,
    ) -> None:
        self.db = Database(table="test", path=":memory:", max_pending=1)

        self.data = (time.human_timestamp(), "ciao", 1, 1.0)
        self.wrong_data = (time.human_timestamp(), "ciao", "ciao", 1, 1.0)

        # create a test table
        self.db._db.execute(
            "CREATE TABLE test(timestamp DATETIME, str_field TEXT, int_field INTEGER, float_field REAL)"
        )

    def test_table_info(self):
        info = self.db._table_info()

        assert info["names"] == ["timestamp", "str_field", "int_field", "float_field"]
        assert info["types"] == [
            SqliteType("datetime"),
            SqliteType("text"),
            SqliteType("integer"),
            SqliteType("real"),
        ]
        assert info["types"] == [
            str(),
            str(),
            int(),
            float(),
        ]

    def test_table_info_fail(self):
        wrong_table = "fake"

        with pytest.raises(
            DatabaseInfoError,
            match=f"Unable to retrive information from table `{wrong_table}`",
        ):
            self.db._table_info(wrong_table)

    def test_check_insert_data(self):
        # tuple
        assert self.db._check_insert_data("test", self.data) == True
        assert self.db._check_insert_data("test", self.wrong_data) == False
        assert self.db._check_insert_data("test", (1, 1, 1)) == False

        # list
        assert self.db._check_insert_data("test", list(self.data)) == True
        assert self.db._check_insert_data("test", list(self.wrong_data)) == False
        assert self.db._check_insert_data("test", [1, 1, 1]) == False

    def test_check_insert_data_dict(self):
        keys = ["timestamp", "str_field", "int_field", "float_field"]
        data = dict()
        for i, k in enumerate(keys):
            data.update({k: self.data[i]})

        assert self.db._check_insert_data("test", data) == True

        # wrong number of fields
        keys = ["str_field", "str_field2", "int_field", "float_field"]
        wrong_data = dict()
        for i, k in enumerate(keys):
            wrong_data.update({k: self.wrong_data[i]})

        assert self.db._check_insert_data("test", wrong_data) == False

        # wrong type of `str_field`, must be `str` is `int`
        wrong_type_data = {
            "timestamp": "1.001",
            "str_field": 12,
            "int_field": 1,
            "float_field": 1.0,
        }
        assert self.db._check_insert_data("test", wrong_type_data) == False

        # wrong type of `int_field`, must be `int` is `float`
        wrong_type_data = {
            "timestamp": "1.001",
            "str_field": "ciao",
            "int_field": 1.0,
            "float_field": 1,
        }
        assert self.db._check_insert_data("test", wrong_type_data) == False

        # a `float_field` can have a int value
        data = {
            "timestamp": "1.001",
            "str_field": "ciao",
            "int_field": 1,
            "float_field": 1,
        }
        assert self.db._check_insert_data("test", data) == True

    def test_insert_data(self):
        first = self.data

        self.db.insert_data(first)

        assert self.db.select() == [first]

        second = [time.human_timestamp(), "ciao", 1, 1.0]
        self.db.insert_data(second)

        assert self.db.select() == [first, tuple(second)]

        third = {
            "timestamp": time.human_timestamp(),
            "str_field": "ciao",
            "int_field": 1,
            "float_field": 1.0,
        }
        self.db.insert_data(third)
        assert self.db.select() == [first, tuple(second), tuple(third.values())]

    def test_insert_data_fail(self):
        # generic exception due error table parameter
        with pytest.raises(DatabaseError):
            self.db.insert_data()

        # data format is wrong
        with pytest.raises(DatabaseDataError):
            self.db.insert_data(self.wrong_data)

    def test_insert(self):
        d = self.data

        for _ in range(5):
            self.db.insert("test", data=d)

        data = self.db.select()

        assert len(data) == 5
        assert data == [d, d, d, d, d]

    def test_insert_fail(self):
        # generic exception due error table parameter
        with pytest.raises(DatabaseError):
            self.db.insert(data=self.wrong_data)

        # data format is wrong
        with pytest.raises(DatabaseDataError):
            self.db.insert("test", data=self.wrong_data)

    def test_range_select(self):
        self.db._db.execute("CREATE TABLE range(id INTEGER, value REAL)")

        for i in range(15):
            self.db.insert("range", data=(i, 12.22))

        read = self.db.select(table="range", range_=(1, 3))
        assert len(read) == 3

        read = self.db.select(table="range", range_=(10, 13))
        assert len(read) == 4

        read = self.db.select(table="range", range_=(2, 13))
        assert len(read) == 12

    def test_config(self):
        g_conf = {"name": "phoenix", "circunference": 1450}
        v_conf = {"grid": False, "zoom": 0, "track_len": 8000}

        self.db._db.execute("CREATE TABLE configuration(module STR, value BLOB)")
        self.db._db.execute(
            "INSERT INTO configuration VALUES (?, ?)",
            ["global", str(g_conf)],
        )
        self.db._db.execute(
            "INSERT INTO configuration VALUES (?, ?)",
            ["video", str(v_conf)],
        )

        conf = self.db.config()
        video = self.db.config("video")

        assert conf == g_conf
        assert video == {**g_conf, **v_conf}

    def test_nested_config(self):
        g_conf = {"name": "phoenix", "circunference": 1450}
        a_conf = {
            "taurusx": {"hall_id": 49, "hall_type": 120, "hr_id": 444},
            "phoenix": {"hall_id": 50, "hall_type": 120, "hr_id": 670},
            "cerberus": {"hall_id": 51, "hall_type": 120, "hr_id": 760},
        }

        self.db._db.execute("CREATE TABLE configuration(module STR, value BLOB)")
        self.db._db.execute(
            "INSERT INTO configuration VALUES (?, ?)",
            ["global", str(g_conf)],
        )
        self.db._db.execute(
            "INSERT INTO configuration VALUES (?, ?)",
            ["ant", str(a_conf)],
        )

        conf = self.db.config("ant")

        assert conf == {**g_conf, **a_conf}
        assert conf.get("phoenix") == a_conf.get("phoenix")
        assert conf.get("kerberos") is None
