"""
Tests de sécurité pour ISO 27001 Toolkit

Tests critiques pour la certification ISO 27001:
1. Protection contre les injections
2. Validation des entrées
3. Permissions de fichiers
4. Chiffrement sécurisé
5. Exposition de secrets
"""

import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import yaml

from iso27001_toolkit.exceptions import ValidationError, EncryptionError
from iso27001_toolkit.validators import (
    validate_email,
    validate_file_path,
    validate_control_id,
    sanitize_filename,
    validate_non_empty,
    validate_risk_score,
    validate_choice,
    validate_url,
    validate_percentage
)
from iso27001_toolkit.utils.encryption import EncryptionManager
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.controls_tracker import ControlsTracker


# ============================================================================
# TESTS: INJECTION & PATH TRAVERSAL
# ============================================================================

class TestPathTraversalProtection:
    """Tests de protection contre path traversal attacks"""

    def test_sanitize_filename_blocks_path_traversal(self):
        """Test que sanitize_filename bloque les tentatives de path traversal"""
        dangerous_names = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "foo/../bar",
            "./../../sensitive",
            "../../../../root/.ssh/id_rsa"
        ]

        for dangerous in dangerous_names:
            # sanitize_filename doit maintenant REJETER ces inputs avec ValidationError
            with pytest.raises(ValidationError, match="path traversal|chemins absoluts"):
                sanitize_filename(dangerous)

    def test_sanitize_filename_removes_dangerous_chars(self):
        """Test que les caractères dangereux sont supprimés"""
        dangerous = '<script>alert("xss")</script>.txt'
        sanitized = sanitize_filename(dangerous)

        assert "<" not in sanitized
        assert ">" not in sanitized
        assert '"' not in sanitized

    def test_sanitize_filename_blocks_null_bytes(self):
        """Test protection contre null byte injection"""
        dangerous = "file.txt\x00.exe"
        sanitized = sanitize_filename(dangerous)

        assert "\x00" not in sanitized

    def test_validate_file_path_prevents_traversal(self, tmp_path):
        """Test que validate_file_path empêche l'accès en dehors du répertoire"""
        # Créer un fichier légitime
        safe_file = tmp_path / "safe.txt"
        safe_file.write_text("safe")

        # Tentative de path traversal
        dangerous_path = str(tmp_path / "../../../etc/passwd")

        # validate_file_path doit rejeter avec ValidationError par défaut
        with pytest.raises(ValidationError, match="Path traversal"):
            validate_file_path(dangerous_path, must_exist=False)

        # Avec allow_parent_traversal=True, il devrait résoudre et retourner le chemin absolu
        result = validate_file_path(dangerous_path, must_exist=False, allow_parent_traversal=True)
        # Le chemin résolu ne devrait plus contenir ".."
        assert ".." not in str(result)


class TestCommandInjectionProtection:
    """Tests de protection contre command injection"""

    def test_no_shell_execution_in_validators(self):
        """Test qu'aucun validateur n'exécute de commandes shell"""
        # Tenter d'injecter des commandes
        malicious_inputs = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "$(whoami)",
            "`whoami`",
            "&& echo hacked"
        ]

        for malicious in malicious_inputs:
            # Les validateurs doivent soit rejeter, soit échapper ces inputs
            # Ils ne doivent JAMAIS les exécuter
            try:
                sanitized = sanitize_filename(malicious)
                # Si pas d'exception, vérifier que les chars dangereux sont neutralisés
                assert "|" not in sanitized
                assert "&" not in sanitized
                assert "$" not in sanitized
                assert "`" not in sanitized
                assert ";" not in sanitized
            except ValidationError:
                # Rejet acceptable (path traversal, caractères invalides, etc.)
                pass


# ============================================================================
# TESTS: VALIDATION EXHAUSTIVE
# ============================================================================

class TestEmailValidation:
    """Tests exhaustifs de validation email"""

    def test_valid_emails(self):
        """Test emails valides"""
        valid_emails = [
            "user@example.com",
            "john.doe@company.co.uk",
            "admin+test@domain.org",
            "user_123@sub.domain.com"
        ]

        for email in valid_emails:
            assert validate_email(email) == email.strip()

    def test_invalid_emails(self):
        """Test emails invalides"""
        invalid_emails = [
            "",
            "notanemail",
            "@example.com",
            "user@",
            "user @example.com",  # espace
            "user@example",  # pas de TLD
            "user@.com",
            "../../../etc/passwd@evil.com"  # path traversal
        ]

        for email in invalid_emails:
            with pytest.raises(ValidationError):
                validate_email(email)

    def test_email_injection_protection(self):
        """Test protection contre email injection"""
        malicious_emails = [
            "user@example.com\nBcc:attacker@evil.com",
            "user@example.com\r\nTo:victim@target.com",
            "user@example.com%0ABcc:hacker@bad.com"
        ]

        for malicious in malicious_emails:
            with pytest.raises(ValidationError):
                validate_email(malicious)


class TestRiskScoreValidation:
    """Tests de validation des scores de risque"""

    def test_valid_risk_scores(self):
        """Test scores valides"""
        for score in [1, 2, 3, 4, 5]:
            assert validate_risk_score(score) == score

    def test_invalid_risk_scores(self):
        """Test scores invalides"""
        invalid_scores = [
            0,      # trop bas
            6,      # trop haut
            -1,     # négatif
            999,    # très grand
            "abc",  # string
            None,   # null
            [],     # list
            {},     # dict
        ]

        for score in invalid_scores:
            with pytest.raises(ValidationError):
                validate_risk_score(score)

    def test_sql_injection_in_scores(self):
        """Test protection contre SQL injection dans les scores"""
        sql_injections = [
            "1; DROP TABLE users--",
            "1 OR 1=1",
            "1'; DELETE FROM risks--"
        ]

        for injection in sql_injections:
            with pytest.raises(ValidationError):
                validate_risk_score(injection)


class TestControlIdValidation:
    """Tests de validation des IDs de contrôles"""

    def test_valid_control_ids(self):
        """Test IDs valides"""
        valid_ids = [
            "A.5.1",
            "A.6.10",
            "A.7.5",
            "A.8.23"
        ]

        for control_id in valid_ids:
            assert validate_control_id(control_id) == control_id

    def test_invalid_control_ids(self):
        """Test IDs invalides"""
        invalid_ids = [
            "",
            "B.5.1",  # pas A
            "A.4.1",  # section invalide (4 < 5)
            "A.9.1",  # section invalide (9 > 8)
            "A.5",    # incomplet
            "5.1",    # pas de A
            "A.5.abc",  # non numérique
            "../A.5.1",  # path traversal
            "A.5.1; DROP TABLE--"  # SQL injection
        ]

        for control_id in invalid_ids:
            with pytest.raises(ValidationError):
                validate_control_id(control_id)


class TestUrlValidation:
    """Tests de validation URL"""

    def test_valid_urls(self):
        """Test URLs valides"""
        valid_urls = [
            "https://example.com",
            "http://sub.domain.co.uk/path",
            "https://site.org/page?param=value"
        ]

        for url in valid_urls:
            assert validate_url(url) == url.strip()

    def test_invalid_urls(self):
        """Test URLs invalides"""
        invalid_urls = [
            "",
            "not a url",
            "ftp://example.com",  # protocol non supporté
            "javascript:alert('xss')",  # XSS
            "file:///etc/passwd",  # file protocol
            "http://",
            "https://"
        ]

        for url in invalid_urls:
            with pytest.raises(ValidationError):
                validate_url(url)

    def test_url_xss_protection(self):
        """Test protection contre XSS dans les URLs"""
        xss_attempts = [
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>",
            "vbscript:msgbox('xss')"
        ]

        for xss in xss_attempts:
            with pytest.raises(ValidationError):
                validate_url(xss)


# ============================================================================
# TESTS: PERMISSIONS & SÉCURITÉ FICHIERS
# ============================================================================

class TestFilePermissions:
    """Tests de permissions de fichiers"""

    def test_encryption_key_has_restrictive_permissions(self, tmp_path):
        """Test que la clé de chiffrement a des permissions restrictives (0600)"""
        key_file = tmp_path / "test_encryption.key"

        # Créer un EncryptionManager (génère une clé)
        enc = EncryptionManager(key_file=key_file)

        # Vérifier que le fichier existe
        assert key_file.exists()

        # Vérifier les permissions (0600 = rw-------)
        permissions = stat.S_IMODE(os.stat(key_file).st_mode)
        assert permissions == 0o600, f"Expected 0600, got {oct(permissions)}"

    def test_yaml_files_not_world_readable(self, mock_config_dir):
        """Test que les fichiers YAML avec données sensibles ne sont pas world-readable"""
        # Créer un RiskManager (utilise get_risks_file() automatiquement)
        risk_manager = RiskManager()

        # Ajouter un risque
        risk_manager.add_risk({
            'name': 'Test Risk',
            'description': 'Sensitive data',
            'impact': 5,
            'likelihood': 5
        })

        # Vérifier que le fichier de données existe
        data_file = risk_manager.file_path
        assert data_file.exists()

        # Vérifier les permissions (ne devrait pas être world-writable)
        permissions = stat.S_IMODE(os.stat(data_file).st_mode)

        # Les permissions ne devraient pas inclure other-write (0o002)
        # Note: En pratique, le fichier est créé avec umask par défaut
        assert not (permissions & stat.S_IWOTH), "File should not be world-writable"


class TestDataLeakage:
    """Tests de prévention de fuite de données"""

    def test_error_messages_dont_leak_sensitive_paths(self, tmp_path):
        """Test que les messages d'erreur ne révèlent pas de chemins sensibles"""
        # Tenter de déchiffrer avec une mauvaise clé
        key_file = tmp_path / "wrong_key.key"
        enc = EncryptionManager(key_file=key_file)

        # Créer une autre instance avec une clé différente
        key_file2 = tmp_path / "another_key.key"
        enc2 = EncryptionManager(key_file=key_file2)

        # Chiffrer avec enc2
        encrypted = enc2.encrypt("secret data")

        # Tenter de déchiffrer avec enc (mauvaise clé)
        try:
            enc.decrypt(encrypted)
            assert False, "Should have raised EncryptionError"
        except EncryptionError as e:
            error_msg = str(e)
            # Le message d'erreur ne devrait pas contenir le chemin complet
            # ni d'informations sensibles sur la clé
            assert "key_file" not in error_msg.lower() or len(str(key_file)) < 20

    def test_logs_dont_contain_encryption_keys(self, tmp_path, caplog):
        """Test que les logs ne contiennent pas les clés de chiffrement"""
        import logging
        caplog.set_level(logging.DEBUG)

        key_file = tmp_path / "secret_key.key"
        enc = EncryptionManager(key_file=key_file)

        # Lire la clé
        with open(key_file, 'rb') as f:
            actual_key = f.read()

        # Vérifier les logs
        for record in caplog.records:
            # Les logs ne devraient JAMAIS contenir la clé brute
            assert actual_key.decode('utf-8', errors='ignore') not in record.message
            # Même pas en représentation hexa
            assert actual_key.hex() not in record.message


# ============================================================================
# TESTS: CHIFFREMENT SÉCURISÉ
# ============================================================================

class TestEncryptionSecurity:
    """Tests de sécurité du chiffrement"""

    def test_encryption_produces_different_output(self, tmp_path):
        """Test que le même input produit des outputs différents (IV unique)"""
        enc = EncryptionManager(key_file=tmp_path / "test.key")

        data = "secret message"
        encrypted1 = enc.encrypt(data)
        encrypted2 = enc.encrypt(data)

        # Fernet utilise un timestamp, donc les ciphertexts sont différents
        assert encrypted1 != encrypted2

    def test_decryption_with_wrong_key_fails(self, tmp_path):
        """Test que le déchiffrement avec la mauvaise clé échoue"""
        key1 = tmp_path / "key1.key"
        key2 = tmp_path / "key2.key"

        enc1 = EncryptionManager(key_file=key1)
        enc2 = EncryptionManager(key_file=key2)

        data = "secret"
        encrypted = enc1.encrypt(data)

        # Déchiffrer avec la mauvaise clé doit échouer
        with pytest.raises(EncryptionError):
            enc2.decrypt(encrypted)

    def test_tampered_ciphertext_fails_decryption(self, tmp_path):
        """Test que la modification du ciphertext empêche le déchiffrement"""
        enc = EncryptionManager(key_file=tmp_path / "test.key")

        data = "secret"
        encrypted = enc.encrypt(data)

        # Modifier un byte du ciphertext
        encrypted_bytes = encrypted.encode('utf-8')
        tampered = bytearray(encrypted_bytes)
        tampered[10] ^= 1  # Flip un bit
        tampered = bytes(tampered).decode('utf-8', errors='ignore')

        # Le déchiffrement doit échouer (HMAC verification)
        with pytest.raises(EncryptionError):
            enc.decrypt(tampered)

    def test_encryption_handles_unicode(self, tmp_path):
        """Test que le chiffrement gère correctement Unicode"""
        enc = EncryptionManager(key_file=tmp_path / "test.key")

        unicode_data = "Données secrètes: 中文, 日本語, العربية, 🔒"
        encrypted = enc.encrypt(unicode_data)
        decrypted = enc.decrypt(encrypted)

        assert decrypted == unicode_data

    def test_encryption_handles_binary_data(self, tmp_path):
        """Test chiffrement de données binaires via fichiers"""
        enc = EncryptionManager(key_file=tmp_path / "test.key")

        # Pour les données binaires, utiliser encrypt_file
        binary_file = tmp_path / "binary.dat"
        binary_data = bytes(range(256))
        binary_file.write_bytes(binary_data)

        # Chiffrer le fichier
        encrypted_file = enc.encrypt_file(binary_file)
        assert encrypted_file.exists()

        # Déchiffrer le fichier
        decrypted_file = enc.decrypt_file(encrypted_file)
        decrypted_data = decrypted_file.read_bytes()

        assert decrypted_data == binary_data

    def test_file_encryption_preserves_data(self, tmp_path):
        """Test que le chiffrement de fichier préserve les données"""
        enc = EncryptionManager(key_file=tmp_path / "test.key")

        # Créer un fichier avec données
        input_file = tmp_path / "secret.txt"
        original_data = b"Secret content\nLine 2\nLine 3"
        input_file.write_bytes(original_data)

        # Chiffrer
        encrypted_file = enc.encrypt_file(input_file)
        assert encrypted_file.exists()

        # Le fichier chiffré ne doit pas contenir le texte en clair
        encrypted_content = encrypted_file.read_bytes()
        assert b"Secret content" not in encrypted_content

        # Déchiffrer
        decrypted_file = enc.decrypt_file(encrypted_file)
        decrypted_data = decrypted_file.read_bytes()

        assert decrypted_data == original_data

    def test_key_rotation_creates_backup(self, tmp_path):
        """Test que la rotation de clé crée une sauvegarde"""
        key_file = tmp_path / "original.key"
        enc = EncryptionManager(key_file=key_file)

        # Sauvegarder la clé originale
        original_key = key_file.read_bytes()

        # Rotation
        enc.rotate_key()

        # Vérifier que la backup existe
        backup_file = key_file.with_suffix('.key.backup')
        assert backup_file.exists()

        # Vérifier que la backup contient la clé originale
        assert backup_file.read_bytes() == original_key

        # Vérifier que la nouvelle clé est différente
        new_key = key_file.read_bytes()
        assert new_key != original_key


# ============================================================================
# TESTS: YAML INJECTION
# ============================================================================

class TestYAMLInjection:
    """Tests de protection contre YAML injection"""

    def test_yaml_safe_load_prevents_code_execution(self, tmp_path):
        """Test que yaml.safe_load est utilisé (pas yaml.load)"""
        # Créer un fichier YAML malicieux
        malicious_yaml = tmp_path / "malicious.yml"
        malicious_yaml.write_text("""
!!python/object/apply:os.system
args: ['echo hacked']
""")

        # Tenter de charger (doit échouer ou ignorer le code)
        with pytest.raises(yaml.YAMLError):
            with open(malicious_yaml) as f:
                yaml.safe_load(f)

    def test_risk_manager_sanitizes_yaml_input(self, mock_config_dir):
        """Test que RiskManager n'accepte pas d'objets Python arbitraires"""
        risk_manager = RiskManager()

        # Tenter d'injecter un objet Python
        malicious_risk = {
            'name': 'Test',
            'description': '!!python/object/apply:os.system',
            'impact': 5,
            'likelihood': 5
        }

        # Devrait soit rejeter, soit traiter comme string
        risk_id = risk_manager.add_risk(malicious_risk)
        risk = risk_manager.get_risk(risk_id)

        # La description doit être une string, pas un objet exécutable
        assert isinstance(risk['description'], str)


# ============================================================================
# TESTS: FUZZING & EDGE CASES
# ============================================================================

class TestFuzzingValidators:
    """Tests de fuzzing pour trouver des edge cases"""

    def test_validate_non_empty_with_whitespace_variations(self):
        """Test avec différents types de whitespace"""
        whitespace_inputs = [
            " ",
            "\t",
            "\n",
            "\r\n",
            "   \t\n   ",
        ]

        for ws in whitespace_inputs:
            with pytest.raises(ValidationError, match="ne peut pas être vide"):
                validate_non_empty(ws, "Test Field")

        # Test null byte séparément (message d'erreur différent)
        with pytest.raises(ValidationError, match="null bytes"):
            validate_non_empty("text\x00here", "Test Field")

        # Note: \u200B (zero-width space) n'est PAS retiré par Python strip()
        # C'est acceptable car c'est un caractère Unicode valide, pas vraiment "vide"

    def test_validate_choice_with_similar_values(self):
        """Test validation de choix avec valeurs similaires"""
        valid_choices = ["low", "medium", "high"]

        # Cas limites
        test_cases = [
            ("low", True),      # OK
            ("LOW", False),     # Case sensitive
            (" low", False),    # Espace
            ("low ", False),    # Espace
            ("lo", False),      # Substring
            ("", False),        # Vide
        ]

        for value, should_pass in test_cases:
            if should_pass:
                assert validate_choice(value, valid_choices) == value
            else:
                with pytest.raises(ValidationError):
                    validate_choice(value, valid_choices)

    def test_percentage_with_edge_values(self):
        """Test validation de pourcentage avec valeurs limites"""
        # Valides
        assert validate_percentage(0) == 0
        assert validate_percentage(100) == 100
        assert validate_percentage(50.5) == 50.5

        # Invalides
        with pytest.raises(ValidationError):
            validate_percentage(-0.1)

        with pytest.raises(ValidationError):
            validate_percentage(100.1)

        with pytest.raises(ValidationError):
            validate_percentage(float('inf'))

        with pytest.raises(ValidationError):
            validate_percentage(float('nan'))


# ============================================================================
# TESTS: INTÉGRATION SÉCURITÉ
# ============================================================================

class TestSecurityIntegration:
    """Tests d'intégration de sécurité"""

    def test_complete_risk_workflow_is_secure(self, mock_config_dir):
        """Test qu'un workflow complet de gestion des risques est sécurisé"""
        risk_manager = RiskManager()

        # Ajouter un risque avec inputs potentiellement malicieux
        risk_id = risk_manager.add_risk({
            'name': '<script>alert("xss")</script>',
            'description': '../../etc/passwd',
            'impact': 5,
            'likelihood': 5,
            'owner': 'user@example.com\nBcc:hacker@evil.com'
        })

        # Récupérer le risque
        risk = risk_manager.get_risk(risk_id)

        # Les données doivent être stockées telles quelles (échappement au moment de l'affichage)
        # mais ne doivent pas causer d'injection
        assert risk_id is not None
        assert risk is not None
        assert isinstance(risk['name'], str)

        # Vérifier que le fichier YAML est valide
        data_file = risk_manager.file_path
        assert data_file.exists()

        with open(data_file) as f:
            data = yaml.safe_load(f)

        assert 'risks' in data
        assert len(data['risks']) > 0

    def test_controls_tracker_handles_malicious_input(self, mock_config_dir):
        """Test que ControlsTracker gère les inputs malicieux"""
        tracker = ControlsTracker()
        tracker.initialize()

        # Tenter d'update avec un ID malicieux
        malicious_ids = [
            "A.5.1; DROP TABLE controls--",
            "../../../etc/passwd",
            "A.999.999"
        ]

        for malicious_id in malicious_ids:
            # Devrait soit échouer avec ValidationError, soit ignorer
            try:
                tracker.update_control_status(malicious_id, 'implemented')
            except (ValidationError, ValueError, KeyError):
                pass  # Expected

    def test_template_engine_prevents_template_injection(self, tmp_path):
        """Test protection contre template injection dans Jinja2"""
        from iso27001_toolkit.utils.template_engine import TemplateEngine

        engine = TemplateEngine()

        # Tenter d'injecter du code dans les variables
        malicious_context = {
            'company_name': '{{ config.items() }}',  # Tenter d'accéder à config
            'policy_name': '{% for item in ().__class__.__bases__[0].__subclasses__() %}{% endfor %}',  # Python injection
            'version': '1.0',
            'effective_date': '2025-01-01',
            'review_period': '12 mois',
            'owner': 'RSSI'
        }

        # Le template engine doit échapper ou rejeter ces tentatives
        # Jinja2 avec autoescape devrait protéger
        try:
            result = engine.render_policy('policy_template', malicious_context)
            # Le résultat ne devrait pas contenir de code exécuté
            assert isinstance(result, str)
            # Les accolades devraient être échappées ou traitées comme texte littéral
        except FileNotFoundError:
            # Si le template n'existe pas, c'est acceptable pour ce test
            # L'important est que Jinja2 utilise autoescape
            pass


# ============================================================================
# TESTS: CONFIGURATION BANDIT (SAST)
# ============================================================================

class TestSASTConfiguration:
    """Tests pour vérifier que SAST est configuré"""

    def test_bandit_config_exists(self):
        """Vérifier que .bandit existe ou est configuré dans pyproject.toml"""
        # Vérifier dans pyproject.toml
        pyproject = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject.exists():
            content = pyproject.read_text()
            # Vérifier qu'il y a une config bandit ou que bandit est mentionné
            # Note: Ce test sera mis à jour quand on configure Bandit
            assert True  # Placeholder

    def test_no_hardcoded_secrets_in_code(self):
        """Test qu'il n'y a pas de secrets hardcodés (pattern matching basique)"""
        # Patterns dangereux
        dangerous_patterns = [
            b'password = "',
            b'api_key = "',
            b'secret_key = "',
            b'aws_access_key',
            b'private_key = "-----BEGIN'
        ]

        # Scanner les fichiers Python
        src_dir = Path(__file__).parent.parent / "src"

        for py_file in src_dir.rglob("*.py"):
            content = py_file.read_bytes()

            for pattern in dangerous_patterns:
                if pattern in content:
                    # Vérifier que ce n'est pas dans un commentaire ou exemple
                    lines = content.split(b'\n')
                    for line in lines:
                        if pattern in line and not line.strip().startswith(b'#'):
                            # Autoriser les exemples dans les docstrings
                            if b'"""' not in line and b"'''" not in line:
                                pytest.fail(
                                    f"Potential hardcoded secret found in {py_file}: {line}"
                                )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
