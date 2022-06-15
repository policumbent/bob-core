import pytest

from core.database import Database, SqliteType
from core.exceptions import DatabaseError, DatabaseInfoError


class TestDatabase:
    def setup(
        self,
    ) -> None:
        self.db = Database(table="test", path=":memory:", max_pending=1)

        self.data = ("ciao", 1, 1.0)
        self.wrong_data = ("ciao", "ciao", 1, 1.0)

        # create a test table
        self.db._db.execute(
            "CREATE TABLE test(str_field TEXT, int_field INTEGER, float_field REAL)"
        )

    def test_table_info(self):
        info = self.db._table_info()

        assert info["names"] == ["str_field", "int_field", "float_field"]
        assert info["types"] == [
            SqliteType("text"),
            SqliteType("integer"),
            SqliteType("real"),
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
        keys = ["str_field", "int_field", "float_field"]
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

        # wrong type of `str_filed`, must be `str` is `int`
        wrong_type_data = {"str_field": 12, "int_field": 1, "float_field": 1.0}
        assert self.db._check_insert_data("test", wrong_type_data) == False

        # wrong type of `float_filed`, must be `float` is `int`
        wrong_type_data = {"str_field": 12, "int_field": 1, "float_field": 1}
        assert self.db._check_insert_data("test", wrong_type_data) == False

    def test_insert(self):
        d = self.data

        for _ in range(5):
            self.db.insert("test", data=d)

        data = self.db.select()

        assert len(data) == 5
        assert data == [d, d, d, d, d]

    def test_insert_fail(self):
        with pytest.raises(DatabaseError):
            self.db.insert("test", data=self.wrong_data)
