import sqlite3
import time


class Database:
    def __init__(self, path: str = "database.db", max_pending=10_000) -> None:
        self._db = sqlite3.connect(path, detect_types=1)

        self._pending = 0
        self._max_pending = max_pending

        # todo: remove
        try:
            self._db.execute("PRAGMA journal_mode=wal")
            self._db.execute(
                "CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)"
            )
        except:
            pass

    def __del__(self):
        """Close the db on exit"""

        # check if there are uncommitted changes
        if self._db.in_transaction:
            self._db.commit()

        self._db.close()

    def _commit(self) -> None:
        self._pending += 1

        if self._pending > self._max_pending:
            try:
                self._db.commit()
                self._pending = 0
            except sqlite3.DatabaseError:
                # if database is locked pass and try to
                # commit on the next change
                pass

    def insert(self, table: str = None, data: list = None) -> None:
        """Insert a new row into the db table

        :param table: name of the table to write
        :param data: ordered list with the data to write
        """

        if table is None or data is None:
            return

        # fill the query with the qmark
        values = ",".join(["?"] * len(data))

        self._db.execute(f"INSERT INTO {table} VALUES ({values})", data)

        # evaluate commit if there are enough pending changes
        self._commit()

    def select(self, table: str = None, range_: tuple = None) -> list:
        """Read a range of row of the table, if a range is not provided return the entire table

        :param table: name of the table to read
        :param range: inclusive range of value to read in the form `(start, end)`[default=None]
        """

        if range_ is None:
            return self._db.execute(f"SELECT * FROM {table}").fetchall()
        elif isinstance(range_, tuple) and len(range_) == 2:
            start, end = range_

            return self._db.execute(
                f"SELECT * FROM {table} WHERE id >= {start} AND id <= {end}"
            ).fetchall()


def main():
    db = Database(max_pending=10)

    # db.insert("fish", ["ciao", "ciao", 1])

    print(db.select("fish"))

    # start = time.time()

    # ins_num = 10_000_000

    # for _ in range(ins_num):
    #     db.insert()

    # try:
    #     ins_num = 0
    #     while True:
    #         db.insert("fish", ["ciao", "ciao", 1])
    #         ins_num += 1
    # except Exception as e:
    #     pass
    # finally:
    #     exec_time = time.time() - start

    #     print(
    #         f"Proc: 1\nExec time: {exec_time} sec\nInset: {ins_num} ins\nInsert per sec: {ins_num/exec_time:.3f} ins/sec"
    #     )


if __name__ == "__main__":
    main()
