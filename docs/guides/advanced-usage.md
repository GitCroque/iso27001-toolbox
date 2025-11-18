# Guide d'Utilisation Avancée - ISO 27001 Toolkit

> Guide complet pour les utilisateurs avancés souhaitant maîtriser toutes les fonctionnalités du toolkit

**Version**: 0.1.0  
**Dernière mise à jour**: 2025-11-18  
**Niveau**: Avancé

---

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Gestion avancée des risques](#gestion-avancée-des-risques)
- [Automatisation avec scripts](#automatisation-avec-scripts)
- [Intégration CI/CD](#intégration-cicd)
- [Personnalisation des templates](#personnalisation-des-templates)
- [Chiffrement et sécurité](#chiffrement-et-sécurité)
- [Workflow multi-sites](#workflow-multi-sites)
- [Export et rapports personnalisés](#export-et-rapports-personnalisés)
- [Best practices](#best-practices)
- [Dépannage](#dépannage)

---

## Vue d'ensemble

Ce guide couvre les fonctionnalités avancées d'ISO 27001 Toolkit pour :
- 🏢 **Organisations multi-sites** : Gérer plusieurs projets
- ⚙️ **Automatisation** : Scripts et CI/CD
- 🎨 **Personnalisation** : Templates et rapports custom
- 🔒 **Sécurité renforcée** : Chiffrement, permissions
- 📊 **Reporting avancé** : Dashboards, métriques

---

## 🎯 Gestion avancée des risques

### 1. Importation en masse de risques

**Format CSV** :

```csv
title,description,probability,impact,category,treatment
Perte de données,Défaillance serveur sans backup,3,5,availability,mitigate
Phishing,Email de phishing ciblant les employés,4,4,confidentiality,mitigate
RGPD,Non-conformité traitement données,2,4,compliance,accept
```

**Script d'importation** :

```python
#!/usr/bin/env python3
"""Import risks from CSV file"""

import csv
import subprocess
import sys

def import_risks(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cmd = [
                'iso27001', 'risks', 'add',
                '--title', row['title'],
                '--description', row['description'],
                '--probability', row['probability'],
                '--impact', row['impact'],
                '--category', row['category'],
                '--treatment', row['treatment']
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {row['title']}")
            else:
                print(f"✗ {row['title']}: {result.stderr}", file=sys.stderr)

if __name__ == '__main__':
    import_risks(sys.argv[1])
```

**Utilisation** :

```bash
python scripts/import_risks.py risks.csv
```

### 2. Analyse de tendances des risques

**Tracker l'évolution dans le temps** :

```bash
# Snapshot mensuel
iso27001 risks report --output reports/risks_$(date +%Y%m).md

# Archiver le registre
cp ~/.iso27001/data/risks.yml backups/risks_$(date +%Y%m%d).yml

# Comparer avec le mois précédent
diff backups/risks_202411.yml backups/risks_202412.yml
```

**Script de métriques** :

```python
#!/usr/bin/env python3
"""Generate risk metrics over time"""

import yaml
import glob
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

def analyze_risk_trend(backup_dir):
    """Analyze risk levels over time"""
    files = sorted(glob.glob(f"{backup_dir}/risks_*.yml"))

    dates = []
    critical_count = []
    high_count = []

    for file in files:
        date = Path(file).stem.split('_')[1]  # Extract date
        with open(file) as f:
            data = yaml.safe_load(f)
            levels = Counter(r['level'] for r in data.get('risks', []))

            dates.append(date)
            critical_count.append(levels.get('critical', 0))
            high_count.append(levels.get('high', 0))

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, critical_count, 'r-', label='Critical', marker='o')
    plt.plot(dates, high_count, 'orange', label='High', marker='s')
    plt.xlabel('Date')
    plt.ylabel('Number of Risks')
    plt.title('Risk Evolution Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('risk_trend.png')
    print("✓ Trend chart saved to risk_trend.png")

if __name__ == '__main__':
    analyze_risk_trend('backups')
```

### 3. Liens risques ↔ contrôles

**Associer des contrôles à un risque** :

```bash
# Ajouter un risque avec contrôles associés
iso27001 risks add \
  --title "Accès non autorisé aux données" \
  --description "Un utilisateur pourrait accéder à des données sans autorisation" \
  --impact 4 \
  --probability 3 \
  --category confidentiality \
  --controls "A.5.15,A.5.16,A.8.2,A.8.3"
```

**Générer une matrice risques-contrôles** :

```bash
iso27001 audit traceability-matrix --output matrix.md
```

---

## ⚙️ Automatisation avec scripts

### 1. Script de vérification quotidienne

**`daily_check.sh`** :

```bash
#!/bin/bash
# Daily ISO 27001 health check

set -e

REPORT_DIR="reports/daily"
DATE=$(date +%Y%m%d)

mkdir -p "$REPORT_DIR"

echo "📊 ISO 27001 Daily Health Check - $DATE"
echo "========================================="
echo

# 1. Diagnostic de santé
echo "1. Running doctor check..."
iso27001 doctor > "$REPORT_DIR/doctor_$DATE.txt"

# 2. Statut des contrôles
echo "2. Controls status..."
iso27001 controls list --format summary > "$REPORT_DIR/controls_$DATE.txt"

# 3. Risques critiques
echo "3. Critical risks..."
iso27001 risks list --level critical > "$REPORT_DIR/critical_risks_$DATE.txt"

# 4. Score de préparation
echo "4. Audit readiness..."
iso27001 audit readiness > "$REPORT_DIR/readiness_$DATE.txt"

echo
echo "✓ Reports generated in $REPORT_DIR"

# 5. Alertes (exemple)
CRITICAL_COUNT=$(grep -c "critical" "$REPORT_DIR/critical_risks_$DATE.txt" || echo "0")
if [ "$CRITICAL_COUNT" -gt 5 ]; then
    echo "⚠️  WARNING: $CRITICAL_COUNT critical risks detected!"
    # Envoyer notification (email, Slack, etc.)
    # send_notification "High critical risks: $CRITICAL_COUNT"
fi
```

**Configurer un cron job** :

```bash
# Exécuter tous les jours à 8h
crontab -e

# Ajouter :
0 8 * * * /path/to/daily_check.sh
```

### 2. Sauvegarde automatique

**`backup.sh`** :

```bash
#!/bin/bash
# Automated backup to cloud storage

BACKUP_DIR="$HOME/iso27001-backups"
DATE=$(date +%Y%m%d_%H%M%S)
ARCHIVE="iso27001_backup_$DATE.tar.gz"

# Créer l'archive
tar -czf "$BACKUP_DIR/$ARCHIVE" -C "$HOME" .iso27001/

# Upload to S3 (example)
# aws s3 cp "$BACKUP_DIR/$ARCHIVE" s3://my-bucket/iso27001-backups/

# Nettoyer les backups > 30 jours
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

echo "✓ Backup saved: $ARCHIVE"
```

**Cron hebdomadaire** :

```bash
# Tous les lundis à 1h du matin
0 1 * * 1 /path/to/backup.sh
```

---

## 🚀 Intégration CI/CD

### 1. GitHub Actions

**`.github/workflows/iso27001-check.yml`** :

```yaml
name: ISO 27001 Compliance Check

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am

jobs:
  compliance-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install ISO 27001 Toolkit
        run: |
          pip install iso27001-toolkit

      - name: Run doctor check
        run: |
          iso27001 doctor
          if [ $? -ne 0 ]; then
            echo "❌ Health check failed"
            exit 1
          fi

      - name: Verify controls implementation
        run: |
          IMPLEMENTED=$(iso27001 controls list --status implemented --count)
          TOTAL=$(iso27001 controls list --count)
          PERCENTAGE=$((IMPLEMENTED * 100 / TOTAL))

          echo "📊 Controls: $IMPLEMENTED/$TOTAL ($PERCENTAGE%)"

          if [ $PERCENTAGE -lt 75 ]; then
            echo "❌ Less than 75% controls implemented"
            exit 1
          fi

      - name: Check critical risks
        run: |
          CRITICAL=$(iso27001 risks list --level critical --count)

          if [ $CRITICAL -gt 5 ]; then
            echo "⚠️  $CRITICAL critical risks detected"
            exit 1
          fi

      - name: Generate reports
        run: |
          iso27001 audit soa --output reports/soa.md
          iso27001 risks report --output reports/risks.md

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: iso27001-reports
          path: reports/
```

### 2. GitLab CI

**`.gitlab-ci.yml`** :

```yaml
stages:
  - compliance
  - report

iso27001_check:
  stage: compliance
  image: python:3.11
  before_script:
    - pip install iso27001-toolkit
  script:
    - iso27001 doctor
    - iso27001 controls list --format summary
    - iso27001 risks list --level critical
  only:
    - main
    - merge_requests

generate_reports:
  stage: report
  image: python:3.11
  before_script:
    - pip install iso27001-toolkit[pdf]
  script:
    - iso27001 export soa --output soa.pdf
    - iso27001 export risks --output risks.pdf
  artifacts:
    paths:
      - "*.pdf"
    expire_in: 30 days
  only:
    - tags
```

---

## 🎨 Personnalisation des templates

### 1. Créer un template de politique personnalisée

**Étape 1 : Créer le template Jinja2**

```bash
mkdir -p ~/.iso27001/custom_templates/policies/
vim ~/.iso27001/custom_templates/policies/remote_work_policy.md
```

**Contenu** (`remote_work_policy.md`) :

```jinja2
# {{ organization_name }} - Politique de Télétravail

**Date d'effet** : {{ effective_date }}  
**Version** : 1.0  
**Responsable** : {{ ciso_name }}

---

## 1. Objectif

Cette politique définit les règles et bonnes pratiques pour le télétravail chez {{ organization_name }}, conformément à l'ISO 27001:2022 (contrôles A.6.7, A.6.8).

## 2. Périmètre

S'applique à tous les employés de {{ organization_name }} en situation de télétravail.

## 3. Exigences de sécurité

### 3.1 Équipement

- **Ordinateur professionnel** fourni par {{ organization_name }}
- **Chiffrement complet du disque** (BitLocker, FileVault)
- **VPN obligatoire** pour accès aux ressources internes
- **Antivirus à jour** (scan quotidien)

### 3.2 Accès réseau

- **VPN {{ vpn_provider }}** : Connexion obligatoire
- **MFA activé** : Google Authenticator ou Duo
- **Pas de WiFi public** sans VPN

### 3.3 Espace de travail

- **Zone sécurisée** : Bureau dédié, accès restreint
- **Écran de confidentialité** si travail dans espace partagé
- **Verrouillage automatique** après 5 min d'inactivité

## 4. Procédures

### 4.1 Début de journée

1. Vérifier les mises à jour système
2. Se connecter au VPN
3. Activer le statut "En ligne" sur Slack/Teams

### 4.2 Fin de journée

1. Fermer toutes les sessions
2. Verrouiller l'ordinateur
3. Ranger les documents physiques (si applicable)

## 5. Interdictions

- ❌ Accès aux données sensibles depuis un appareil personnel
- ❌ Partage de mot de passe
- ❌ Stockage de données professionnelles sur cloud personnel (Dropbox, Google Drive)
- ❌ Imprimer des documents confidentiels à domicile

## 6. Incidents

Tout incident (perte équipement, accès suspect, etc.) doit être signalé immédiatement à :

- **RSSI** : {{ ciso_email }}
- **Hotline sécurité** : +33 1 XX XX XX XX

## 7. Contrôles associés

- **A.6.7** : Télétravail
- **A.6.8** : Gestion des événements liés à la sécurité de l'information
- **A.8.2** : Droits d'accès privilégiés
- **A.8.3** : Restriction des droits d'accès

---

**Approuvé par** : {{ ciso_name }}, RSSI  
**Date d'approbation** : {{ current_date }}
```

**Étape 2 : Ajouter les variables personnalisées**

```bash
# Éditer config
vim ~/.iso27001/config.yml
```

Ajouter :

```yaml
vpn_provider: "Cisco AnyConnect"
mfa_tool: "Google Authenticator"
helpdesk_phone: "+33 1 23 45 67 89"
```

**Étape 3 : Générer la politique**

```bash
iso27001 policies generate \
  --template custom_templates/policies/remote_work_policy.md \
  --output policies/remote_work_policy.md
```

### 2. Template de rapport personnalisé

**Exemple : Rapport exécutif mensuel**

```jinja2
# Rapport Exécutif ISO 27001 - {{ month }} {{ year }}

**{{ organization_name }}**  
**RSSI** : {{ ciso_name }}

---

## 📊 Résumé

| Métrique | Valeur | Tendance |
|----------|--------|----------|
| Score de maturité | {{ maturity_score }}% | {{ trend_maturity }} |
| Contrôles implémentés | {{ controls_implemented }}/114 | {{ trend_controls }} |
| Risques critiques | {{ critical_risks }} | {{ trend_risks }} |
| Incidents de sécurité | {{ incidents_count }} | {{ trend_incidents }} |

## 🎯 Objectifs du mois

{% for objective in monthly_objectives %}
- {{ objective.status }} {{ objective.description }}
{% endfor %}

## ⚠️ Risques à surveiller

{% for risk in top_risks %}
### {{ risk.title }}
- **Niveau** : {{ risk.level }}
- **Score** : {{ risk.score }}/25
- **Traitement** : {{ risk.treatment }}
{% endfor %}

## 📈 Prochaines étapes

1. Finaliser implémentation contrôles A.8.x (sécurité technique)
2. Audit interne prévu {{ next_audit_date }}
3. Renouvellement certification en {{ certification_renewal }}

---

*Généré automatiquement par ISO 27001 Toolkit le {{ current_date }}*
```

---

## 🔒 Chiffrement et sécurité

### 1. Chiffrement avancé avec GPG

**Chiffrer le registre des risques** :

```bash
# Générer une clé GPG (si pas déjà fait)
gpg --full-generate-key

# Chiffrer le fichier
gpg --encrypt --recipient your.email@example.com ~/.iso27001/data/risks.yml

# Le fichier chiffré
ls ~/.iso27001/data/risks.yml.gpg

# Déchiffrer pour utilisation
gpg --decrypt ~/.iso27001/data/risks.yml.gpg > /tmp/risks.yml
```

**Script de chiffrement automatique** :

```bash
#!/bin/bash
# encrypt_sensitive_data.sh

GPG_RECIPIENT="ciso@example.com"
FILES=(
    "$HOME/.iso27001/data/risks.yml"
    "$HOME/.iso27001/config.yml"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        gpg --encrypt --recipient "$GPG_RECIPIENT" --yes --output "$file.gpg" "$file"
        echo "✓ Encrypted: $file → $file.gpg"

        # Optionnel : supprimer l'original
        # shred -u "$file"
    fi
done
```

### 2. Permissions restrictives

**Audit des permissions** :

```bash
#!/bin/bash
# audit_permissions.sh

CONFIG_DIR="$HOME/.iso27001"

echo "🔒 Auditing file permissions..."
echo

# Vérifier répertoire
DIR_PERM=$(stat -c %a "$CONFIG_DIR")
if [ "$DIR_PERM" != "700" ]; then
    echo "❌ $CONFIG_DIR permissions: $DIR_PERM (should be 700)"
    echo "   Fix: chmod 700 $CONFIG_DIR"
else
    echo "✓ $CONFIG_DIR: $DIR_PERM"
fi

# Vérifier fichiers sensibles
SENSITIVE_FILES=(
    "encryption.key"
    "data/risks.yml"
    "audit_trail.yml"
)

for file in "${SENSITIVE_FILES[@]}"; do
    FULL_PATH="$CONFIG_DIR/$file"
    if [ -f "$FULL_PATH" ]; then
        PERM=$(stat -c %a "$FULL_PATH")
        if [ "$PERM" != "600" ]; then
            echo "❌ $file permissions: $PERM (should be 600)"
            echo "   Fix: chmod 600 $FULL_PATH"
        else
            echo "✓ $file: $PERM"
        fi
    fi
done
```

### 3. Audit trail avec signature

**Signer l'audit trail pour garantir l'intégrité** :

```bash
# Après chaque modification importante
sha256sum ~/.iso27001/audit_trail.yml > ~/.iso27001/audit_trail.yml.sha256
gpg --detach-sign --armor ~/.iso27001/audit_trail.yml

# Vérifier l'intégrité
gpg --verify ~/.iso27001/audit_trail.yml.asc
sha256sum -c ~/.iso27001/audit_trail.yml.sha256
```

---

## 🌍 Workflow multi-sites

### 1. Configuration par environnement

**Structure** :

```
~/iso27001-projects/
├── production/
│   └── .iso27001/
├── staging/
│   └── .iso27001/
└── development/
    └── .iso27001/
```

**Switch d'environnement** :

```bash
# Alias dans ~/.bashrc
alias iso-prod="ISO27001_CONFIG_DIR=~/iso27001-projects/production/.iso27001 iso27001"
alias iso-staging="ISO27001_CONFIG_DIR=~/iso27001-projects/staging/.iso27001 iso27001"
alias iso-dev="ISO27001_CONFIG_DIR=~/iso27001-projects/development/.iso27001 iso27001"

# Utilisation
iso-prod controls list
iso-staging risks add
```

### 2. Synchronisation entre sites

**Réplication sélective** :

```bash
#!/bin/bash
# sync_environments.sh

SOURCE="~/iso27001-projects/staging/.iso27001"
DEST="~/iso27001-projects/production/.iso27001"

# Copier les contrôles (pas les risques, spécifiques à l'env)
rsync -av "$SOURCE/data/controls.yml" "$DEST/data/"

# Copier les politiques
rsync -av "$SOURCE/../output/policies/" "$DEST/../output/policies/"

echo "✓ Synced staging → production"
```

---

## 📊 Export et rapports personnalisés

### 1. Dashboard HTML interactif

**Générer un dashboard avec Chart.js** :

```python
#!/usr/bin/env python3
"""Generate interactive HTML dashboard"""

import yaml
from pathlib import Path
from jinja2 import Template

CONFIG_DIR = Path.home() / ".iso27001"

# Charger données
with open(CONFIG_DIR / "data/controls.yml") as f:
    controls = yaml.safe_load(f)

with open(CONFIG_DIR / "data/risks.yml") as f:
    risks = yaml.safe_load(f)

# Calculer métriques
total_controls = len(controls.get('controls', {}))
implemented = sum(1 for c in controls['controls'].values() if c['status'] in ['implemented', 'verified'])
maturity = (implemented / total_controls * 100) if total_controls > 0 else 0

# Template HTML
template = Template('''
<!DOCTYPE html>
<html>
<head>
    <title>ISO 27001 Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .metric { display: inline-block; margin: 20px; padding: 20px; background: #f0f0f0; border-radius: 5px; }
        .chart { width: 600px; margin: 20px; }
    </style>
</head>
<body>
    <h1>📊 ISO 27001 Dashboard</h1>

    <div class="metric">
        <h2>{{ maturity }}%</h2>
        <p>Maturité</p>
    </div>

    <div class="metric">
        <h2>{{ implemented }}/{{ total }}</h2>
        <p>Contrôles implémentés</p>
    </div>

    <div class="metric">
        <h2>{{ critical_risks }}</h2>
        <p>Risques critiques</p>
    </div>

    <div class="chart">
        <canvas id="controlsChart"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('controlsChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Implémentés', 'En cours', 'Non démarrés'],
                datasets: [{
                    data: [{{ implemented }}, {{ in_progress }}, {{ not_started }}],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545']
                }]
            }
        });
    </script>
</body>
</html>
''')

# Render
html = template.render(
    maturity=round(maturity, 1),
    implemented=implemented,
    total=total_controls,
    critical_risks=sum(1 for r in risks.get('risks', []) if r.get('level') == 'critical'),
    in_progress=0,  # Calculate from controls
    not_started=0   # Calculate from controls
)

# Save
output_file = Path("dashboard.html")
output_file.write_text(html)
print(f"✓ Dashboard saved to {output_file.absolute()}")
```

### 2. Rapport PDF multi-documents

**Générer un package complet** :

```bash
#!/bin/bash
# generate_full_package.sh

DATE=$(date +%Y%m%d)
OUTPUT_DIR="iso27001_package_$DATE"

mkdir -p "$OUTPUT_DIR"

echo "📦 Generating complete ISO 27001 package..."

# 1. Politiques
echo "1. Generating policies..."
iso27001 policies generate --output "$OUTPUT_DIR/policies"
iso27001 export policies --output-dir "$OUTPUT_DIR/pdf/policies"

# 2. SOA
echo "2. Generating Statement of Applicability..."
iso27001 export soa --output "$OUTPUT_DIR/pdf/soa.pdf"

# 3. Risques
echo "3. Generating risk register..."
iso27001 export risks --output "$OUTPUT_DIR/pdf/risks.pdf"

# 4. Audit checklist
echo "4. Generating audit checklist..."
iso27001 audit checklist --output "$OUTPUT_DIR/audit_checklist.md"

# 5. Gap analysis
echo "5. Generating gap analysis..."
iso27001 audit gap-analysis --output "$OUTPUT_DIR/gap_analysis.md"

# 6. Créer archive
echo "6. Creating archive..."
tar -czf "iso27001_package_$DATE.tar.gz" "$OUTPUT_DIR"

echo "✓ Package complete: iso27001_package_$DATE.tar.gz"
```

---

## ✅ Best Practices

### 1. Workflow recommandé

**Cycle mensuel** :

```
Semaine 1 : Revue des risques
  ├─ Réévaluer probabilité/impact
  ├─ Ajouter nouveaux risques identifiés
  └─ Mettre à jour traitements

Semaine 2 : Mise à jour contrôles
  ├─ Avancer implémentation
  ├─ Ajouter preuves (documents, screenshots)
  └─ Passer status implemented → verified

Semaine 3 : Génération rapports
  ├─ SOA, registre risques
  ├─ Métriques de progression
  └─ Présentation au comité direction

Semaine 4 : Amélioration continue
  ├─ Actions correctives des non-conformités
  ├─ Formation employés
  └─ Préparation mois suivant
```

### 2. Documentation continue

**Bonnes pratiques** :

- ✅ **Committer régulièrement** : Versioner `.iso27001/` avec Git
- ✅ **Notes détaillées** : Documenter le "pourquoi" de chaque décision
- ✅ **Preuves horodatées** : Toujours dater les documents (screenshots, emails)
- ✅ **Backup 3-2-1** : 3 copies, 2 supports différents, 1 off-site
- ✅ **Audit trail** : Ne jamais supprimer ou modifier l'historique

### 3. Sécurité opérationnelle

**Checklist** :

- [ ] Permissions 0700 sur `~/.iso27001/`
- [ ] Permissions 0600 sur fichiers sensibles
- [ ] Clé de chiffrement sauvegardée en lieu sûr
- [ ] Pas de secrets (mots de passe) en clair dans YAML
- [ ] Backup automatique quotidien
- [ ] Audit des accès mensuel
- [ ] Rotation de clé annuelle

---

## 🔧 Dépannage

### Problème : "Permission denied" lors de l'accès à ~/.iso27001/

**Solution** :

```bash
# Vérifier les permissions
ls -la ~/.iso27001/

# Corriger si nécessaire
chmod 700 ~/.iso27001/
chmod 600 ~/.iso27001/data/*.yml
chmod 600 ~/.iso27001/encryption.key
```

### Problème : Export PDF échoue avec "WeasyPrint not found"

**Solution** :

```bash
# Installer les dépendances système (Ubuntu/Debian)
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

# Installer WeasyPrint
pip install iso27001-toolkit[pdf]

# Vérifier
python -c "import weasyprint; print(weasyprint.__version__)"
```

### Problème : Données corrompues après crash

**Solution** :

```bash
# Restaurer depuis le backup le plus récent
cp ~/backups/iso27001-20241115/.iso27001/data/risks.yml ~/.iso27001/data/

# Ou depuis Git (si versionné)
cd ~/.iso27001/
git checkout HEAD -- data/risks.yml
```

### Problème : Performance lente avec >500 risques

**Solution** :

```bash
# Archiver les risques traités/clos
iso27001 risks archive --status closed --output archived_risks_2024.yml

# Optimiser le fichier YAML (retirer espaces)
python -c "import yaml; data=yaml.safe_load(open('~/.iso27001/data/risks.yml')); yaml.dump(data, open('~/.iso27001/data/risks.yml', 'w'), default_flow_style=False)"
```

---

## 📚 Ressources

- [Documentation officielle](https://github.com/GitCroque/iso27001-toolbox)
- [Tutorial démarrage rapide](../tutorials/quickstart.md)
- [Architecture technique](../../ARCHITECTURE.md)
- [Guide de contribution](../../CONTRIBUTING.md)
- [ISO 27001:2022 Standard](https://www.iso.org/standard/27001)

---

**Besoin d'aide ?** → [GitHub Issues](https://github.com/GitCroque/iso27001-toolbox/issues)

---

**Dernière mise à jour** : 2025-11-18  
**Version** : 1.0.0
