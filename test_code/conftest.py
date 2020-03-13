assert __name__ != "__main__", "This module should NOT be executed."

import os
import sys

# Include the path to the parent directory
sys.path.insert(0, os.path.dirname(__file__))

def pytest_addoption(parser):
    parser.addoption("--image", action="store", default="default name")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.image
    if 'image' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("image", [option_value])