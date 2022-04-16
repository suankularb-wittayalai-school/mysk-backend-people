import sys
import os

from src.db.database import engine, metadata


def pytest_configure(config):
    sys._called_from_test = True


def pytest_unconfigure(config):
    del sys._called_from_test


# delete everything in test database before each test
def pytest_runtest_setup(item):
    if "test_" in item.name:
        metadata.drop_all(engine)
        metadata.create_all(engine)
    # pass


# delete test database after end of test session
def pytest_sessionfinish(session, exitstatus):
    os.remove("test.db")
