from __future__ import annotations
from paramiko.client import SSHClient

from typing import Any

from textual.message import Message


class CronJobDeleted(Message):
    """Dispatched after a cron job was removed from the crontab so listeners can clean up (e.g. log files)."""

    def __init__(
        self,
        identificator: str,
        *,
        ssh_client: Any = None,
    ) -> None:
        self.identificator: str = identificator
        self.ssh_client: SSHClient = ssh_client
        super().__init__()
