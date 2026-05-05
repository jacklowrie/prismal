import argparse

import pytest

from prismal.cli import add_common_arguments


def test_add_common_arguments():
    parser = argparse.ArgumentParser()
    add_common_arguments(parser)

    # Test required config argument
    with pytest.raises(SystemExit):
        parser.parse_args([])

    # Test providing only config
    args = parser.parse_args(["-c", "config.yaml"])
    assert args.config == "config.yaml"
    assert args.input is None
    assert args.output is None
    assert args.model is None

    # Test providing all arguments
    args = parser.parse_args(
        ["-c", "config.yaml", "-i", "input.txt", "-o", "output.txt", "-m", "gpt-4"]
    )
    assert args.config == "config.yaml"
    assert args.input == "input.txt"
    assert args.output == "output.txt"
    assert args.model == "gpt-4"


def test_add_common_arguments_long_names():
    parser = argparse.ArgumentParser()
    add_common_arguments(parser)

    args = parser.parse_args(
        [
            "--config",
            "config.yaml",
            "--input",
            "input.txt",
            "--output",
            "output.txt",
            "--model",
            "gpt-4",
        ]
    )
    assert args.config == "config.yaml"
    assert args.input == "input.txt"
    assert args.output == "output.txt"
    assert args.model == "gpt-4"
