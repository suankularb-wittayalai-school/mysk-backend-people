import sys
import os

from src.db.database import engine, metadata


def pytest_configure(config):
    sys._called_from_test = True


def pytest_unconfigure(config):
    del sys._called_from_test


# make sure test.db dont exit before test session
def pytest_sessionstart(session):
    if os.path.exists("test.db"):
        os.remove("test.db")


# create everything in test database before each test
def pytest_runtest_setup(item):
    metadata.create_all(engine)
    # pass


# delete test database after end of test session
def pytest_runtest_teardown(item):
    metadata.drop_all(engine)


# delete test database after end of test session
def pytest_sessionfinish(session, exitstatus):
    os.remove("test.db")
