# pytest-zulip

Pytest report plugin for [Squadcast](https://www.squadcast.com/)

Allow to send incident on Squadcast product.

## installation

    pip install pytest-squadcast

## Add option to send message

    pytest --squadcast

## Create payload via hook

    def pytest_squadcast_create_payload(session: Session, exitstatus: Union[int, ExitCode]) -> dict:
        reporter = session.config.pluginmanager.get_plugin('terminalreporter')
        return {"data": {
                            "message": "This will be the incident message",
                            "description": "This will be the incident description",
                            "tags": {
                                "passed": str(reporter.stats.get('passed', [])),
                                "tagname2": "Tag value#2",
                            },
                            "status": "trigger",
                        },
                "service": "0d2a4409625e05adbc1d81b3540ag89826bfa7cc",
                }


## Dev

### Change version

edit

    pytest_squadcast/__init__.py

commit

    git commit -m "v0.1.0"

tag

    git tag v0.1.0

### Build package

    python -m build
    twine upload dist/*
