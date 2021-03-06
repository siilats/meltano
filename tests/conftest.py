import logging
import os

import pytest
from _pytest.monkeypatch import MonkeyPatch

logging.basicConfig(level=logging.INFO)

PYTEST_BACKEND = os.getenv("PYTEST_BACKEND", "sqlite")

pytest_plugins = [
    "fixtures.db",
    "fixtures.fs",
    "fixtures.core",
    "fixtures.api",
    "fixtures.cli",
]

if PYTEST_BACKEND == "sqlite":
    pytest_plugins.append("fixtures.db.sqlite")
elif PYTEST_BACKEND == "postgresql":
    pytest_plugins.append("fixtures.db.postgresql")
else:
    raise Exception(f"Unsuported backend: {PYTEST_BACKEND}.")

BACKEND = ["sqlite", "postgresql"]


def pytest_runtest_setup(item):
    backend_marker = item.get_closest_marker("backend")

    # currently, there is no distinction between the SYSTEM database
    # and the WAREHOUSE database at the test level.
    # There is only one database used for the tests, and it serves
    # both as SYSTEM and WAREHOUSE.
    if backend_marker and backend_marker.args[0] != PYTEST_BACKEND:
        pytest.skip()


@pytest.fixture(scope="session")
def concurrency():
    return {
        "threads": int(os.getenv("PYTEST_CONCURRENCY_THREADS", 8)),
        "processes": int(os.getenv("PYTEST_CONCURRENCY_PROCESSES", 8)),
        "cases": int(os.getenv("PYTEST_CONCURRENCY_CASES", 64)),
    }


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    monkeypatch = MonkeyPatch()
    monkeypatch.setenv("MELTANO_DISABLE_TRACKING", "True")

    yield

    monkeypatch.undo()
