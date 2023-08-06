import os
import shutil
from time import sleep

import pytest

from click.testing import CliRunner

from kaze.kaze_cli import kaze, Envs

Envs.DATA_DIR = os.path.expandvars('$HOME/kaze_debug')


@pytest.fixture
def setup():
    try:
        os.remove(Envs.DATA_DIR)
        os.remove('.kaze.yml')
        os.remove('.kaze-lock.yml')
        sleep(0.1)
    except Exception as e:
        pass
    os.makedirs(Envs.DATA_DIR, exist_ok=True)


def test_kaze_add(setup):
    runner = CliRunner()
    # os.remove(Envs.DATA_DIR + "/mnist")
    result = runner.invoke(
        kaze, "add https://data.deepai.org/mnist.zip".split(" "),
        input="y\ny\n")
    print(result.output)
    assert result.exit_code == 0
    assert "Download the file to" in result.output


def test_kaze_add_quiet(setup):
    runner = CliRunner()
    result = runner.invoke(
        kaze, "add -q https://data.deepai.org/mnist.zip".split(" "), input="y\n"
    )
    print(result.output)
    assert result.exit_code == 0
    assert "Downloading mnist to" in result.output
