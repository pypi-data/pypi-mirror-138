from typing import Union

import pytest
import requests
from _pytest.config import ExitCode, Config
from _pytest.main import Session
from _pytest.terminal import TerminalReporter


class Squadcast:
    def __init__(self, config: Config):
        self.config = config

    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]):
        self.send_incident(session, exitstatus)

    @pytest.hookimpl(trylast=True)
    def pytest_terminal_summary(
        self,
        terminalreporter: TerminalReporter,
        exitstatus: Union[int, ExitCode],
        config: Config,
    ):
        terminalreporter.write_sep("-", "incident reported on Squadcast")

    def send_incident(self, session: Session, exitstatus: Union[int, ExitCode]):
        # https://support.squadcast.com/docs/apiv2
        payload = session.config.hook.pytest_squadcast_create_payload(
            session=session, exitstatus=exitstatus
        )
        if not payload:
            raise Exception("you must implement the hook to create payload")
        requests.post(
            url=f"https://api.squadcast.com/v2/incidents/api/{payload[0]['service']}",
            json=payload[0]["data"],
        )
