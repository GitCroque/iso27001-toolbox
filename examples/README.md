# ISO 27001 Toolkit - Examples

This directory contains ready-to-use examples and scripts for ISO 27001 Toolkit.

## 📂 Directory Structure

```
examples/
├── automation/          # Automation scripts
├── integration/         # Integration examples
├── ci_cd/              # CI/CD pipeline configurations
├── scripts/            # Utility scripts
├── config/             # Configuration examples
└── README.md           # This file
```

---

## 🤖 Automation Scripts

### `automation/daily_check.py`

Daily health check script for ISO 27001 project.

**Features:**
- Runs `iso27001 doctor` diagnostic
- Checks critical risks count
- Verifies control implementation progress
- Generates daily report
- Sends email alerts if thresholds exceeded

**Usage:**
```bash
# Manual run
python examples/automation/daily_check.py

# With email alerts
python examples/automation/daily_check.py --email ciso@example.com

# Setup cron (daily at 8 AM)
0 8 * * * /usr/bin/python3 /path/to/daily_check.py
```

### `automation/weekly_backup.sh`

Weekly backup script with cloud upload support.

**Features:**
- Creates tar.gz archive of `~/.iso27001/`
- Optional upload to S3/GCS/Azure
- Automatic cleanup (90-day retention)
- Backup manifest generation

**Usage:**
```bash
# Manual run
bash examples/automation/weekly_backup.sh

# Setup cron (every Monday at 2 AM)
0 2 * * 1 /path/to/weekly_backup.sh
```

---

## 🔌 Integration Examples

### `integration/flask_api.py`

Complete Flask REST API integration.

**Endpoints:**
- `GET  /api/health` - Health check
- `GET  /api/risks` - List risks
- `POST /api/risks` - Create risk
- `GET  /api/controls` - List controls
- `GET  /api/controls/stats` - Control statistics
- `GET  /api/audit/readiness` - Audit readiness
- `GET  /api/dashboard` - Dashboard data

**Installation:**
```bash
pip install flask flask-cors
```

**Usage:**
```bash
python examples/integration/flask_api.py

# API available at http://localhost:5000
# Documentation: http://localhost:5000/api/docs
```

**Example request:**
```bash
# Create a new risk
curl -X POST http://localhost:5000/api/risks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Data breach",
    "description": "Unauthorized access to customer data",
    "probability": 4,
    "impact": 5,
    "category": "confidentiality"
  }'
```

---

## 🚀 CI/CD Pipelines

### `ci_cd/github_actions.yml`

GitHub Actions workflow for compliance checks.

**Features:**
- Runs on push, PR, and weekly schedule
- Doctor diagnostic
- Critical risk verification
- Control maturity check (≥75%)
- Generates compliance reports (SOA, risks, gap analysis)
- Exports PDF reports
- Uploads artifacts (90-day retention)

**Setup:**
```bash
# Copy to your repository
mkdir -p .github/workflows/
cp examples/ci_cd/github_actions.yml .github/workflows/iso27001-compliance.yml

# Commit and push
git add .github/workflows/
git commit -m "ci: add ISO 27001 compliance checks"
git push
```

### `ci_cd/gitlab_ci.yml`

GitLab CI pipeline for compliance.

**Setup:**
```bash
# Copy to repository root
cp examples/ci_cd/gitlab_ci.yml .gitlab-ci.yml

# Commit and push
git add .gitlab-ci.yml
git commit -m "ci: add ISO 27001 pipeline"
git push
```

---

## 📜 Utility Scripts

### `scripts/import_risks_csv.py`

Import risks from CSV file.

**CSV Format:**
```csv
title,description,probability,impact,category,treatment
Data loss,Server failure,3,5,availability,mitigate
Phishing,Email attack,4,4,confidentiality,mitigate
```

**Usage:**
```bash
# Import from CSV
python examples/scripts/import_risks_csv.py risks.csv

# Use example file
python examples/scripts/import_risks_csv.py examples/scripts/risks_example.csv
```

**Example CSV provided:** `scripts/risks_example.csv`

---

## ⚙️ Configuration Examples

### `config/config.example.yml`

Complete configuration example with all available options.

**Usage:**
```bash
# Copy to your project
cp examples/config/config.example.yml ~/.iso27001/config.yml

# Edit with your values
vim ~/.iso27001/config.yml
```

**Sections:**
- Organization information
- Key personnel (CISO, DPO, CEO)
- Policy configuration
- Governance settings
- Risk management
- Audit configuration
- Compliance requirements
- Backup settings
- Notification settings
- Custom fields

---

## 🎯 Quick Start

### 1. Daily Automation

```bash
# Setup daily health check
cp examples/automation/daily_check.py ~/bin/
chmod +x ~/bin/daily_check.py

# Add to crontab
crontab -e
# Add: 0 8 * * * /usr/bin/python3 ~/bin/daily_check.py --email ciso@example.com
```

### 2. Weekly Backup

```bash
# Setup weekly backup
cp examples/automation/weekly_backup.sh ~/bin/
chmod +x ~/bin/weekly_backup.sh

# Configure cloud upload (optional)
vim ~/bin/weekly_backup.sh  # Uncomment S3/GCS/Azure section

# Add to crontab
crontab -e
# Add: 0 2 * * 1 ~/bin/weekly_backup.sh
```

### 3. API Integration

```bash
# Install dependencies
pip install flask flask-cors

# Run API server
python examples/integration/flask_api.py

# Test
curl http://localhost:5000/api/health
```

### 4. CI/CD Setup

```bash
# For GitHub
mkdir -p .github/workflows/
cp examples/ci_cd/github_actions.yml .github/workflows/iso27001-compliance.yml

# For GitLab
cp examples/ci_cd/gitlab_ci.yml .gitlab-ci.yml

# Commit
git add .github/ .gitlab-ci.yml
git commit -m "ci: add ISO 27001 automation"
git push
```

---

## 📚 Additional Resources

- [Tutorial Démarrage Rapide](../docs/tutorials/quickstart.md)
- [Guide Utilisateur Avancé](../docs/guides/advanced-usage.md)
- [Guide Best Practices](../docs/guides/best-practices.md)
- [Documentation API](../docs/api/developer-guide.md)

---

## 💡 Tips

1. **Customize scripts** to your organization's needs
2. **Test thoroughly** before deploying to production
3. **Monitor logs** regularly
4. **Backup data** before running bulk operations
5. **Use version control** for configuration files

---

## 🐛 Troubleshooting

### Import CSV fails

```bash
# Check CSV format
head -5 risks.csv

# Verify columns
cat risks.csv | head -1
```

### Daily check fails

```bash
# Run manually to see errors
python examples/automation/daily_check.py

# Check ISO 27001 toolkit installation
iso27001 --version
```

### API returns 500

```bash
# Check if toolkit is initialized
iso27001 doctor

# View Flask logs
python examples/integration/flask_api.py
```

---

**Need help?** → [GitHub Issues](https://github.com/GitCroque/iso27001-toolbox/issues)
