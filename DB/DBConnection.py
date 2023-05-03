import sqlite3


def connect():
    return sqlite3.connect("./databases/epood_kjugapuu.db")
