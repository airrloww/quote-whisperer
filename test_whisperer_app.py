"""
This module contains unit tests for the database operations of the Whisperer application.
"""

import unittest
import sqlite3
import os
from whisperer_app import create_connection, create_table, add_user, check_user


class TestDatabaseOperations(unittest.TestCase):
    """
    Test case for testing the database operations of the Whisperer application.
    """

    def setUp(self):
        """
        Set up the test case by creating a connection to the test database
        and creating the necessary table.
        """
        self.conn = create_connection("test_database.db")
        create_table(self.conn)

    def test_create_connection(self):
        """
        Test the create_connection() function.

        Ensure that the function returns a valid connection object.
        """
        conn = create_connection("test_database.db")
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()

    def test_add_user(self):
        """
        Test the add_user() function.

        Ensure that a user can be added successfully,
        and verify that adding the same user again returns False.
        """
        result = add_user(self.conn, "TestUser")
        self.assertEqual(result, True)

        # Test trying to add the same user again
        result = add_user(self.conn, "TestUser")
        self.assertEqual(result, False)

    def test_check_user(self):
        """
        Test the check_user() function.

        Ensure that the function correctly identifies existing and non-existing users.
        """
        # Check if the user exists
        add_user(self.conn, "TestUser")
        result = check_user(self.conn, "TestUser")
        self.assertEqual(result, True)

        # Check non-existing user
        result = check_user(self.conn, "NonExistingUser")
        self.assertEqual(result, False)

    def tearDown(self):
        """
        Tear down the test case by closing the database connection
        and deleting the test database file.
        """
        # Close the database connection
        self.conn.close()

        # Delete the test database file
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")


if __name__ == "__main__":
    unittest.main()
