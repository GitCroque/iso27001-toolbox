"""
Tests pour le CLI principal
"""

import pytest
from click.testing import CliRunner

from iso27001_toolkit.cli import main, info
from iso27001_toolkit import __version__


class TestMainCLI:
    """Tests pour le CLI principal"""

    def test_main_help(self):
        """Test l'affichage de l'aide"""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])

        assert result.exit_code == 0
        assert 'ISO 27001 Toolkit' in result.output
        assert 'policies' in result.output
        assert 'controls' in result.output
        assert 'risks' in result.output
        assert 'audit' in result.output

    def test_main_version(self):
        """Test l'affichage de la version"""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])

        assert result.exit_code == 0
        assert __version__ in result.output

    def test_info_command(self):
        """Test la commande info"""
        runner = CliRunner()
        result = runner.invoke(info)

        assert result.exit_code == 0
        assert 'ISO 27001 Toolkit' in result.output
