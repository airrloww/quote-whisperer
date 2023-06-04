"""
This module was created to list all the users currently in the database
"""

import sqlite3
from sqlite3 import Error
from prettytable import PrettyTable


def create_connection():
    """
    Creates a connection to a SQLite database.

    Returns:
        conn: The database connection object if successful, None otherwise.
    """
    conn = None
    try:
        conn = sqlite3.connect("whisperer_app.db")
        print(f"[-] this app uses sqlite version {sqlite3.version}")
    except Error as error:
        print(error)
    return conn


def list_all_tables(conn):
    """
    Lists all tables in the database.

    Args:
        conn: The database connection object.

    Returns:
        bool: True if tables were listed successfully, False otherwise.
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        if len(tables) == 0:
            print("[+] No tables in the database.")
            return False
        table = PrettyTable(["Tables in Database"])
        for table_entry in tables:
            table.add_row([table_entry[0]])
        print(table)
        return True
    except Error as error:
        print(error)
        return False


def list_all_users(conn):
    """
    Lists all users in the 'users' table.

    Args:
        conn: The database connection object.

    Returns:
        list of all users in the database
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        user_table = PrettyTable(["ID", "Username"])
        for user in users:
            user_table.add_row([user[0], user[1]])
        print(user_table)
    except Error as error:
        print(error)


def main():
    """
    Main function to display tables and users information.
    """
    conn = create_connection()
    if conn is not None:
        if list_all_tables(conn):
            list_all_users(conn)
    else:
        print("[+] Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
