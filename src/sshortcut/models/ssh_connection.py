from .base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SSHConnection(Base):
    __tablename__ = "ssh_connection"

    id: Mapped[int] = mapped_column(primary_key=True)
    server: Mapped[str] = mapped_column(String(256))
    port: Mapped[int] = mapped_column(default=22)
    username: Mapped[str] = mapped_column(String(256))
