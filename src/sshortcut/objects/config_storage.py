from typing import List

from pydantic import BaseModel, Field


class SSHConfig(BaseModel):
    server: str
    port: int
    username: str

    @property
    def ssh_connection(self):
        if not self.port == 22:
            return f"ssh -p {self.port} {self.username}@{self.server}"
        return f"ssh {self.username}@{self.server}"


class ConfigStorage(BaseModel):
    options: List[SSHConfig] = Field(default_factory=list)
