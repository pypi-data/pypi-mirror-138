import os

import pytest
from click.testing import CliRunner

from kaze.kaze_cli import kaze, Envs

Envs.DATA_DIR = os.path.expandvars('$HOME/kaze_debug')


@pytest.fixture
def remove_data():
    try:
        os.remove(Envs.DATA_DIR)
    except Exception as e:
        pass
    os.makedirs(Envs.DATA_DIR, exist_ok=True)


@pytest.fixture
def remove_yml():
    try:
        os.remove(".kaze.yml")
    except Exception as e:
        pass


@pytest.fixture
def remove_lock():
    try:
        os.remove(".kaze-lock.yml")
    except Exception as e:
        pass


def test_kaze_add(remove_data, remove_yml, remove_lock):
    runner = CliRunner()
    # os.remove(Envs.DATA_DIR + "/mnist")
    result = runner.invoke(
        kaze, "add https://data.deepai.org/mnist.zip".split(" "),
        input="y\ny\n")
    print(result.output)
    assert result.exit_code == 0
    assert "Download the file to" in result.output


def test_kaze_add_quiet(remove_data, remove_yml, remove_lock):
    runner = CliRunner()
    result = runner.invoke(
        kaze, "add -q https://data.deepai.org/mnist.zip".split(" "), input="y\n"
    )
    print(result.output)
    assert result.exit_code == 0
    assert "Downloading mnist to" in result.output


def test_kaze(remove_data):
    runner = CliRunner()
    result = runner.invoke(
        kaze, input="y\n"
    )
    print()
    print(result.output)
    assert result.exit_code == 0
    assert "Found 1 dataset" in result.output
