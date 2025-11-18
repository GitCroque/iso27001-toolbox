# Security Policy

## 🔒 Security Statement

ISO 27001 Toolkit is designed to help organizations achieve ISO 27001 certification. Security is at the core of our mission, and we take the security of this project seriously.

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## 🛡️ Security Features

### Data Protection

- **Encryption**: Fernet symmetric encryption (AES-128-CBC + HMAC) for sensitive data
- **Key Management**: Encryption keys stored with restrictive permissions (0o600)
- **Validation**: Comprehensive input validation (13 validators) to prevent injections
- **Sanitization**: File path sanitization to prevent path traversal attacks
- **Exception Handling**: Secure error handling without sensitive information disclosure

### Data Storage

```
~/.iso27001/
├── config.yml              # Organization configuration
├── data/
│   ├── controls.yml        # Controls tracking
│   ├── risks.yml          # Risk register
│   └── audit.yml          # Audit data
├── logs/
│   └── iso27001_toolkit.log  # Application logs (rotated)
└── encryption.key          # Fernet key (0o600 permissions)
```

**Important Notes:**
- YAML files may contain sensitive organizational data
- Enable encryption for sensitive data using `EncryptionManager`
- Backup encryption key in a secure location
- Logs contain DEBUG information - review before sharing

### Secure Coding Practices

✅ **Implemented:**
- Input validation on all user inputs
- Path traversal protection (`sanitize_filename`)
- SQL injection prevention (YAML storage, no SQL)
- Command injection prevention (no `subprocess` with user input)
- Secure random generation (cryptography library)
- Exception chaining without sensitive data exposure
- Type hints for type safety

## 🚨 Reporting a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please send an email to:
- **Email**: [SECURITY_EMAIL_TO_BE_CONFIGURED]
- **Subject**: `[SECURITY] ISO27001 Toolkit - <Brief Description>`

### What to Include

Please include the following information:
1. **Type of vulnerability** (e.g., injection, XSS, path traversal)
2. **Affected component(s)** (file path, function name)
3. **Steps to reproduce** the vulnerability
4. **Potential impact** of the vulnerability
5. **Suggested fix** (if you have one)
6. **Your name/handle** (for acknowledgment)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 5 business days
- **Fix timeline**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: 60 days

### Public Disclosure

- Security fixes will be released as patch versions
- CVE will be requested for critical/high severity issues
- Public disclosure after fix is available (coordinated disclosure)
- Reporter will be acknowledged in CHANGELOG (unless they prefer anonymity)

## 🔐 Security Best Practices for Users

### 1. Encryption

Enable encryption for sensitive data:

```python
from iso27001_toolkit.utils.encryption import EncryptionManager

# Initialize encryption
manager = EncryptionManager()

# Encrypt sensitive files
manager.encrypt_file(Path("sensitive_data.yml"))
```

### 2. File Permissions

Ensure proper file permissions:

```bash
chmod 600 ~/.iso27001/encryption.key
chmod 700 ~/.iso27001/
chmod 600 ~/.iso27001/config.yml
```

### 3. Key Backup

**CRITICAL:** Backup your encryption key securely:

```bash
# Backup key to secure location
cp ~/.iso27001/encryption.key /secure/backup/location/
chmod 400 /secure/backup/location/encryption.key
```

Without the key, encrypted data cannot be recovered.

### 4. Dependency Updates

Keep dependencies updated:

```bash
pip install --upgrade iso27001-toolkit
pip list --outdated
```

### 5. Log Security

Review logs before sharing:

```bash
# Logs may contain sensitive information
cat ~/.iso27001/logs/iso27001_toolkit.log | grep -i "password\|secret\|key"
```

## 🔍 Security Audit

### Last Security Audit
- **Date**: 2025-11-18
- **Auditor**: Internal review
- **Score**: 8.0/10
- **Report**: See `AUDIT_REPORT.md`

### Known Limitations

1. **Encryption key storage**: Fernet key stored in plaintext on filesystem (standard limitation)
2. **YAML plaintext**: Configuration files not encrypted by default
3. **Local storage**: Data stored locally (no cloud backup by default)
4. **No multi-user**: Designed for single-user operation

### Recommended Security Controls

When deploying ISO 27001 Toolkit in production:

- [ ] Enable full-disk encryption on the host system
- [ ] Implement regular backups of `~/.iso27001/`
- [ ] Use strong passwords/passphrases for system access
- [ ] Enable file integrity monitoring (FIM)
- [ ] Regular security updates of Python and dependencies
- [ ] Network isolation if handling highly sensitive data
- [ ] Access control (file permissions) for `.iso27001` directory
- [ ] Audit logging enabled and monitored

## 📦 Dependencies Security

### Monitoring

We monitor dependencies for known vulnerabilities:

```bash
# Check for vulnerabilities
pip install safety
safety check --json

# Or with pre-commit
pre-commit run python-safety-dependencies-check --all-files
```

### Critical Dependencies

| Dependency | Purpose | Security Notes |
|------------|---------|----------------|
| `cryptography>=41.0.0` | Encryption | Keep updated for CVE fixes |
| `pyyaml>=6.0` | YAML parsing | Uses `safe_load()` (no arbitrary code execution) |
| `click>=8.0.0` | CLI framework | Input validation |
| `jinja2>=3.0.0` | Templates | Autoescape enabled |

## 🛠️ Security Tools

### Pre-commit Hooks

Security checks run automatically on commit:

```yaml
# .pre-commit-config.yaml includes:
- bandit      # Security linter for Python
- detect-private-key  # Detect committed secrets
- safety      # Dependency vulnerability scanner
```

### Manual Security Checks

```bash
# Static security analysis
bandit -r src/ -ll

# Dependency vulnerabilities
safety check

# Type checking (prevents type-related bugs)
mypy src/

# Code quality
flake8 src/ --select=S  # Security warnings
```

## 📚 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Cryptography Library Docs](https://cryptography.io/)
- [ISO 27001:2022 Standard](https://www.iso.org/standard/27001)

## 🏆 Security Hall of Fame

We acknowledge security researchers who have helped improve the security of ISO 27001 Toolkit:

<!-- Add names here as vulnerabilities are reported and fixed -->
- *No security reports yet*

Thank you for helping keep ISO 27001 Toolkit secure! 🙏

---

**Last Updated**: 2025-11-18
**Version**: 0.1.0
