"""
TBD
"""

import sqlite3
from sqlite3 import Error
import requests


def create_connection(db_file):
    """
    Creates a connection to a SQLite database file.

    Args:
        db_file: the database file.

    Returns:
        conn: The database connection object if successful, None otherwise.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as error:
        print(error)
    return conn


def create_table(conn):
    """
    Creates the 'users' table in the database if it does not exist.

    Args:
        conn: The database connection object.
    """
    try:
        sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    username varchar(32) NOT NULL UNIQUE);"""
        connection = conn.cursor()
        connection.execute(sql_create_users_table)
    except Error as error:
        print(error)


def add_user(conn, username):
    """
    Adds a user to the 'users' table.

    Args:
        conn: The database connection object.
        username: The username to add.

    Returns:
        bool: True if the user was added successfully, False if the username is already taken.
    """
    sql = """ INSERT INTO users(username) VALUES(?) """
    cur = conn.cursor()
    try:
        cur.execute(sql, (username.lower(),))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def check_user(conn, username):
    """
    Checks if a user with the given username exists in the 'users' table.

    Args:
        conn: The database connection object.
        username: The username to check.

    Returns:
        bool: True if a user with the given username exists, False otherwise.
    """
    sql = """ SELECT * FROM users WHERE username=? """
    cur = conn.cursor()
    cur.execute(sql, (username.lower(),))
    records = cur.fetchall()
    return bool(records)


def get_random_quote():
    """
    Retrieves a random quote from the API and prints the quote, author, and category.
    """
    api_url = "https://api.api-ninjas.com/v1/quotes"
    headers = {"X-Api-Key": "kjZcL1NmyMgOnwYh6KFzxw==S7NbVhlPY0i86NPi"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == requests.codes.ok:
        quote_data = response.json()
        for quote in quote_data:
            formatted_quote = f"""
                [-] Quote: {quote['quote']}
                [-] Author: {quote['author']}
                [-] Category: {quote['category']}
            """
            return formatted_quote
    else:
        return f"Error: {response.status_code} {response.text}"


def get_quote_by_category(category):
    """
    Retrieves quotes from the API for a specific category
    and prints the quotes, authors, and categories.

    Args:
        category: The category of quotes to retrieve.
    """
    api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"
    response = requests.get(
        api_url, headers={"X-Api-Key": "kjZcL1NmyMgOnwYh6KFzxw==S7NbVhlPY0i86NPi"}
    )
    if response.status_code == requests.codes.ok:
        quote_data = response.json()
        for quote in quote_data:
            formatted_quote = f"""
                [-] Quote: {quote['quote']}
                [-] Author: {quote['author']}
                [-] Category: {quote['category']}
            """
            return formatted_quote
    else:
        return f"Error: {response.status_code} {response.text}"


def main():
    """
    Main function starts the cli application for users to register/login
    and proceed to choose between getting a random quote and picking a category to get a quote from
    """
    conn = create_connection("whisperer_app.db")
    if conn is None:
        return

    create_table(conn)

    while True:
        user_input = input("[+] Do you want to 'register' or 'login': ").lower()
        if user_input not in ["register", "login"]:
            print("[+] Invalid option. Please choose 'register' or 'login'.")
            continue

        username = input("[+] Enter your username: ").lower()

        if user_input == "register":
            if add_user(conn, username):
                print(f"[+] User {username} registered successfully.")
            else:
                print(
                    f"[+] Username {username} is already taken. Please choose a different username."
                )
        elif user_input == "login":
            if not check_user(conn, username):
                print(f"[+] No user found with username: {username}")
                continue

            while True:
                action_input = input(
                    "[+] Do you want to get a 'random' quote or choose by 'category': "
                ).lower()
                if action_input == "random":
                    print(get_random_quote())
                    break
                elif action_input == "category":
                    category_input = input("[+] Enter the category of the quote: ")
                    print(get_quote_by_category(category_input))
                    break
                else:
                    print("[+] Invalid option. Please choose 'random' or 'category'.")


if __name__ == "__main__":
    main()
