from typing import List, Type

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from . import ssh_connection
from .base import Base
from .ssh_connection import SSHConnection


class DBConnection:
    connection = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls.connection is None:
            cls.connection = super(DBConnection, cls).__new__(cls)
        return cls.connection

    def __init__(self, connector: str, echo: bool = False, **kwargs):
        if not self._initialized:
            self.engine = create_engine(connector, echo=echo, **kwargs)
            Base.metadata.create_all(self.engine)
            DBConnection._initialized = True

    def add_ssh_connection(self, server: str, port: int, user: str) -> None:
        with Session(self.engine) as session:
            session.add(SSHConnection(server=server, port=port, username=user))
            session.commit()

    def delete_ssh_connection(self, id: int) -> None:
        with Session(self.engine) as session:
            stmt = delete(SSHConnection).where(SSHConnection.id == id)
            session.execute(stmt)
            session.commit()

    def get_all_ssh_connections(self) -> List[Type[SSHConnection]]:
        with Session(self.engine) as session:
            ssh_connections = session.query(SSHConnection).all()
        return ssh_connections
