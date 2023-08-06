#!/usr/bin/env python

"""Tests for `signalboard` package."""

import pytest
from click.testing import CliRunner

from signalboard import cli


@pytest.fixture
def help_options():
    return ['--help']


def test_command_line_interface(help_options):
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, help_options)
    assert help_result.exit_code == 0
    assert '--port' in help_result.output
