"""
Tests pour le module de validation
"""

import pytest
from datetime import datetime
from pathlib import Path

from iso27001_toolkit.validators import (
    validate_email,
    validate_date,
    validate_risk_score,
    validate_choice,
    validate_non_empty,
    validate_integer_range,
    validate_url,
    validate_file_path,
    validate_control_id,
    validate_percentage,
    sanitize_filename,
)
from iso27001_toolkit.exceptions import ValidationError


class TestValidateEmail:
    """Tests pour validate_email"""

    def test_valid_email(self):
        assert validate_email("test@example.com") == "test@example.com"
        assert validate_email(" test@example.com ") == "test@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            validate_email("invalid-email")
        with pytest.raises(ValidationError):
            validate_email("@example.com")
        with pytest.raises(ValidationError):
            validate_email("test@")
        with pytest.raises(ValidationError):
            validate_email("")


class TestValidateDate:
    """Tests pour validate_date"""

    def test_valid_date(self):
        result = validate_date("2025-11-17")
        assert isinstance(result, datetime)
        assert result.year == 2025
        assert result.month == 11
        assert result.day == 17

    def test_invalid_date(self):
        with pytest.raises(ValidationError):
            validate_date("invalid-date")
        with pytest.raises(ValidationError):
            validate_date("2025-13-01")  # Mois invalide
        with pytest.raises(ValidationError):
            validate_date("")


class TestValidateRiskScore:
    """Tests pour validate_risk_score"""

    def test_valid_score(self):
        assert validate_risk_score(1) == 1
        assert validate_risk_score(3) == 3
        assert validate_risk_score(5) == 5
        assert validate_risk_score("3") == 3

    def test_invalid_score(self):
        with pytest.raises(ValidationError):
            validate_risk_score(0)  # Trop bas
        with pytest.raises(ValidationError):
            validate_risk_score(6)  # Trop haut
        with pytest.raises(ValidationError):
            validate_risk_score("not a number")


class TestValidateChoice:
    """Tests pour validate_choice"""

    def test_valid_choice(self):
        choices = ["high", "medium", "low"]
        assert validate_choice("high", choices) == "high"

    def test_invalid_choice(self):
        choices = ["high", "medium", "low"]
        with pytest.raises(ValidationError):
            validate_choice("invalid", choices)
        with pytest.raises(ValidationError):
            validate_choice("", choices)


class TestValidateNonEmpty:
    """Tests pour validate_non_empty"""

    def test_valid_string(self):
        assert validate_non_empty("test") == "test"
        assert validate_non_empty(" test ") == "test"

    def test_invalid_string(self):
        with pytest.raises(ValidationError):
            validate_non_empty("")
        with pytest.raises(ValidationError):
            validate_non_empty("   ")


class TestValidateIntegerRange:
    """Tests pour validate_integer_range"""

    def test_valid_integer(self):
        assert validate_integer_range(5, min_val=1, max_val=10) == 5
        assert validate_integer_range("5", min_val=1, max_val=10) == 5

    def test_out_of_range(self):
        with pytest.raises(ValidationError):
            validate_integer_range(0, min_val=1, max_val=10)
        with pytest.raises(ValidationError):
            validate_integer_range(11, min_val=1, max_val=10)

    def test_invalid_type(self):
        with pytest.raises(ValidationError):
            validate_integer_range("not a number", min_val=1, max_val=10)


class TestValidateUrl:
    """Tests pour validate_url"""

    def test_valid_url(self):
        assert validate_url("https://example.com") == "https://example.com"
        assert validate_url("http://example.com/path") == "http://example.com/path"

    def test_invalid_url(self):
        with pytest.raises(ValidationError):
            validate_url("not-a-url")
        with pytest.raises(ValidationError):
            validate_url("ftp://example.com")  # Protocole non supporté
        with pytest.raises(ValidationError):
            validate_url("")


class TestValidateFilePath:
    """Tests pour validate_file_path"""

    def test_valid_path(self, temp_dir):
        # Créer un fichier temporaire
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")

        result = validate_file_path(str(test_file), must_exist=True)
        assert isinstance(result, Path)
        assert result.exists()

    def test_nonexistent_path(self, temp_dir):
        test_file = temp_dir / "nonexistent.txt"

        # Sans must_exist, devrait fonctionner
        result = validate_file_path(str(test_file), must_exist=False)
        assert isinstance(result, Path)

        # Avec must_exist, devrait échouer
        with pytest.raises(ValidationError):
            validate_file_path(str(test_file), must_exist=True)


class TestValidateControlId:
    """Tests pour validate_control_id"""

    def test_valid_control_id(self):
        assert validate_control_id("A.5.1") == "A.5.1"
        assert validate_control_id("A.8.23") == "A.8.23"

    def test_invalid_control_id(self):
        with pytest.raises(ValidationError):
            validate_control_id("A.9.1")  # Catégorie invalide (doit être 5-8)
        with pytest.raises(ValidationError):
            validate_control_id("B.5.1")  # Préfixe invalide
        with pytest.raises(ValidationError):
            validate_control_id("A.5")  # Format incomplet
        with pytest.raises(ValidationError):
            validate_control_id("")


class TestValidatePercentage:
    """Tests pour validate_percentage"""

    def test_valid_percentage(self):
        assert validate_percentage(0) == 0.0
        assert validate_percentage(50) == 50.0
        assert validate_percentage(100) == 100.0
        assert validate_percentage(50.5) == 50.5

    def test_invalid_percentage(self):
        with pytest.raises(ValidationError):
            validate_percentage(-1)
        with pytest.raises(ValidationError):
            validate_percentage(101)
        with pytest.raises(ValidationError):
            validate_percentage("not a number")


class TestSanitizeFilename:
    """Tests pour sanitize_filename"""

    def test_valid_filename(self):
        assert sanitize_filename("document.pdf") == "document.pdf"
        assert sanitize_filename("my file.txt") == "my file.txt"

    def test_sanitize_dangerous_characters(self):
        assert sanitize_filename("file<>:name.txt") == "file___name.txt"
        assert sanitize_filename("path/to/file.txt") == "path_to_file.txt"
        assert sanitize_filename("file|name.txt") == "file_name.txt"

    def test_empty_after_sanitization(self):
        with pytest.raises(ValidationError):
            sanitize_filename("<<<>>>")
        with pytest.raises(ValidationError):
            sanitize_filename("")
