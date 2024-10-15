import unittest
from typing import List

from sshortcut.models.database_connection import DBConnection
from sshortcut.models.ssh_connection import SSHConnection


class TestModels(unittest.TestCase):
    def setUp(self):
        self.connection = DBConnection("sqlite+pysqlite:///:memory:")

    def test_add_ssh_connection(self):
        self.connection.add_ssh_connection(server="127.0.0.1", port=22, user="Test")
        result = self.connection.get_all_ssh_connections()

        assert len(result) == 1
        assert result[0].server == "127.0.0.1"
        assert result[0].port == 22
        assert result[0].username == "Test"

    def test_delete_ssh_connection(self):
        self.connection.add_ssh_connection(server="127.0.0.1", port=22, user="Test")
        self.connection.delete_ssh_connection(1)
        result = self.connection.get_all_ssh_connections()
        assert len(result) == 0


if __name__ == "__main__":
    unittest.main()
