from typing import Union

from _pytest.config import ExitCode
from _pytest.main import Session


def pytest_squadcast_create_payload(
    session: Session, exitstatus: Union[int, ExitCode]
) -> dict:
    """Called to create content"""
