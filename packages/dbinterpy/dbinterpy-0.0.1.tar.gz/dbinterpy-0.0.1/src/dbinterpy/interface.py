import sqlite3


class DatabaseInterface():

    def __init__(self, db_name: str, keys_types: dict = None) -> None:
        """
        Creates a DatabaseInterface object connected to a SQLite database
        named 'db_name', creates the database with one table headed
        according to the headings and types given in 'keys_types'. If
        'keys_types' is not provided then the connection is made to an
        existing database named 'db_name'.
        """
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.db_name = db_name
        if keys_types is None:
            self.get_table()
            return
        self.keys_types = keys_types
        self.create_table()
        self.conn.commit()

    def __del__(self) -> None:
        """
        Closes connection immediately on destruction
        """
        self.conn.close()

    def __str__(self) -> str:
        rep = "DatabaseInterface connected to: {}\nItem\t".format(self.db_name)
        for key in self.keys_types:
            rep += str(key)+"\t"
        rep = rep[:-1]+'\n'
        rep += '-' * len(rep.split('\n')[0]) + '\n'
        self.cur.execute("SELECT rowid, * FROM {0}".format(self.db_name[:-3]))
        for item in self.cur.fetchall():
            for entry in item:
                rep += str(entry) + '\t'
            rep += '\n'
        self.conn.commit()
        return rep

    def __repr__(self) -> str:
        rep = "<DatabaseInterface('{}') at {}>".format(
                self.db_name, hex(id(self)))
        return rep

    def get_table(self) -> None:
        """
        Returns the table from the database, currently compatibility only
        extends to one table per database
        """
        keys_types = {}
        self.cur.execute("PRAGMA table_info({})".format(self.db_name[:-3]))
        for item in self.cur.fetchall():
            keys_types[item[1]] = item[2]
        self.keys_types = keys_types
        self.conn.commit()

    def create_table(self) -> None:
        """
        Creates table in the database with the same name as the database
        (called automatically when creating a new database)
        """
        command = "CREATE TABLE IF NOT EXISTS {} (".format(self.db_name[:-3])
        for item in self.keys_types:
            command += "{} {}, ".format(item, self.keys_types[item])
        command = command[:-2]+")"
        self.cur.execute(command)
        self.conn.commit()

    def add_one(self, record: dict) -> None:
        """
        Adds a record to the database, 'record' must be given as a dictionary
        with the table headings as the keys and the data as values.
        """
        command = "("
        for key in record:
            if isinstance(record[key], int) or isinstance(record[key], float):
                command += str(record[key])+","
            elif isinstance(record[key], str):
                command += "'"+record[key]+"',"
        command = command[:-1] + ")"
        self.cur.execute("INSERT INTO {0} VALUES {1}"
                         .format(self.db_name[:-3], command))
        self.conn.commit()

    def add_many(self, records: list) -> None:
        """
        Adds many records to the database, input must be a list of dictionaries
        sith the table headings as the keys and the data as values.
        """
        for record in records:
            self.add_one(record)

    def update(self, r_id: int, key: str, value) -> None:
        """
        Updates the database entry at 'r_id' for the desired setting the data
        for heading 'key' as 'value'.
        """
        self.cur.execute("UPDATE {0} SET {1} = {2} WHERE rowid = {3}"
                         .format(self.db_name[:-3], key, value, r_id))
        self.conn.commit()

    def delete(self, r_id: int) -> None:
        """
        Deletes the database entry at 'r_id'
        """
        self.cur.execute("DELETE from {0} WHERE rowid = {1}"
                         .format(self.db_name[:-3], r_id))
        self.conn.commit()

    def execute(self, command: str) -> None:
        """
        Executes a user-input SQLite command which must be given as a string.
        """
        if not isinstance(command, str):
            raise ValueError("Command must be a string")
        self.cur.execute(command)

    def lookup(self, criteria=None) -> list:
        """
        Looks up all entries in the database according to user-input criteria
        which can take the form of a tuple or a list of tuples. If no criteria
        are provided all elements in the table are returned.
        """
        if criteria is None:
            self.execute("SELECT rowid, * from {0}".format(self.db_name[:-3]))
            items = self.cur.fetchall()
            self.conn.commit()
            return items

        comm = "SELECT rowid, * from {0} WHERE ".format(self.db_name[:-3])

        if isinstance(criteria, tuple):
            criteria = [criteria]

        for idx, crit in enumerate(criteria):

            if (not isinstance(crit, tuple)) or len(crit) != 2:
                raise ValueError(
                        "Criteria provided not tuple or list of length 2")

            if isinstance(crit[1], str):
                comm += "{0}='{1}'".format(crit[0], crit[1])
            elif isinstance(crit[1], int) or isinstance(crit[1], float):
                comm += "{0}={1}".format(crit[0], crit[1])
            if idx != len(criteria)-1:
                comm += " AND "

        self.cur.execute(comm)
        items = self.cur.fetchall()
        self.conn.commit()
        return items
