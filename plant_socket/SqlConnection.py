import sqlite3
import time

""" This is a helper class that handles all connection to the database. Each daemon has its own, and theyre not necessarily the same. It depends on what that daemon has to do with the database. """

class SqlConnection():
    def __init__(self, database_name = "../database.sqlite3"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        if database_name == ":memory:":
            print("Initalizing db from memory. (db_name = %s)" % database_name)
            self.init_from_file("db_def.sql")


    def add_plant(self, name):
        command = """INSERT INTO plants (name) VALUES (?);"""
        self.execute(command, (name,))
        pass

    def add_data_point(self, name, dryness):
        command = """INSERT INTO dryness_data (timestamp, dryness, plant) VALUES (?, ?, ?);"""
        self.execute(command, (int(time.time()), dryness, name))
        pass

    def add_watering_point(self, name, amount):
        command = """INSERT INTO watering_stats (timestamp, duration, plant) VALUES (?, ?, ?);"""
        self.execute(command, (int(time.time()), amount, name))
        pass

    def get_plants(self):
        command = """SELECT * FROM plants;"""
        return [{"plant_id": data[0], "name": data[1]} for data in self.get(command)]

    def get_data_for_plant(self, name):
        command = """SELECT * FROM dryness_data WHERE plant = ?;"""
        return [{"data_id": x[0], "timestamp": x[1], "dryness": x[2], "plant": x[3]} for x in self.get(command, (name,))]

    def get_watering_points_for_plant(self, name):
        command = """SELECT * FROM watering_stats WHERE plant = ?;"""
        return [{"data_id": x[0], "timestamp": x[1], "duration": x[2], "plant": x[3]} for x in self.get(command, (name,))]

    def get_data_from_last_days(self, name, days):
        command = """SELECT * FROM dryness_data WHERE plant = ? AND timestamp > ?;"""
        time = time.time() - (days * 24 * 3600)
        return [{"data_id": x[0], "timestamp": x[1], "dryness": x[2], "plant": x[3]} for x in self.get(command, (name, time))]


    def execute(self, command, args):
        self.cursor.execute(command, args)
        self.conn.commit()
        return

    def get(self, command, args=()):
        return list(self.cursor.execute(command, args))

    def init_from_file(self, filename):
        f = open(filename)
        lines = f.read()
        f.close()

        for statement in lines.split(";"):
            self.cursor.execute(statement + ";")
        self.conn.commit()
