# FAQ - Questions Fréquentes

> Réponses aux questions les plus posées sur ISO 27001 Toolkit

**Dernière mise à jour** : 2024-11-18  
**Version** : 1.0.0

---

## 📋 Table des matières

- [Général](#général)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Certification ISO 27001](#certification-iso-27001)
- [Technique](#technique)
- [Sécurité](#sécurité)
- [Contribution](#contribution)

---

## Général

### Qu'est-ce qu'ISO 27001 Toolkit ?

ISO 27001 Toolkit est une suite d'outils en ligne de commande (CLI) open-source qui facilite la démarche de certification ISO 27001:2022. Il vous aide à :
- Gérer le registre des risques
- Suivre l'implémentation des 114 contrôles
- Générer des politiques de sécurité
- Préparer les audits
- Exporter des rapports PDF professionnels

### Est-ce gratuit ?

Oui, ISO 27001 Toolkit est **100% gratuit et open-source** sous licence MIT. Vous pouvez :
- ✅ Utiliser gratuitement (usage commercial inclus)
- ✅ Modifier le code source
- ✅ Distribuer des copies
- ✅ Contribuer au projet

### Qui devrait utiliser cet outil ?

- **RSSI (Responsables Sécurité SI)** : Piloter la démarche ISO 27001
- **DSI** : Suivre l'implémentation des contrôles techniques
- **Consultants** : Accompagner plusieurs clients
- **PME** : Simplifier la certification sans gros budget
- **Auditeurs** : Vérifier la conformité

### Puis-je utiliser sans être expert ISO 27001 ?

**Oui !** Le toolkit est conçu pour être accessible :
- 📖 [Tutorial 30 minutes](docs/tutorials/quickstart.md) pour démarrer
- 📚 Documentation complète avec exemples
- 🤖 Commande `iso27001 doctor` pour diagnostiquer les problèmes
- ✅ Validation automatique des données

**Cependant** : Pour la certification, nous recommandons de vous faire accompagner par un consultant ISO 27001 expérimenté.

### Quelle est la différence avec d'autres solutions ?

| Critère | ISO 27001 Toolkit | Solutions commerciales | Excel/Word |
|---------|-------------------|------------------------|------------|
| **Prix** | Gratuit | 5k-50k€/an | Gratuit |
| **Expertise requise** | Moyenne | Variable | Élevée |
| **Automatisation** | Élevée | Très élevée | Faible |
| **Personnalisation** | Totale (open-source) | Limitée | Totale |
| **Export PDF** | ✅ Oui | ✅ Oui | Manuelle |
| **Audit trail** | ✅ Automatique | ✅ Oui | ❌ Non |
| **CI/CD** | ✅ Oui | Parfois | ❌ Non |
| **Courbe d'apprentissage** | 1-2 jours | 1-4 semaines | N/A |

**Quand choisir ISO 27001 Toolkit ?**
- Budget limité (< 10k€ pour certification)
- Équipe technique à l'aise avec CLI/scripts
- Besoin de personnalisation
- Organisation < 500 employés

**Quand choisir une solution commerciale ?**
- Budget confortable (> 50k€)
- Équipe non-technique
- Besoin d'interface web sophistiquée
- Organisation > 1000 employés

---

## Installation

### Quels sont les prérequis ?

**Système d'exploitation** :
- ✅ Linux (Ubuntu, Debian, CentOS, Arch, etc.)
- ✅ macOS (10.14+)
- ✅ Windows (via WSL2 ou Git Bash)

**Logiciels** :
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- 50 MB d'espace disque

**Optionnel (pour export PDF)** :
- WeasyPrint (+ dépendances système)

### Comment installer sur Ubuntu/Debian ?

```bash
# 1. Installer Python et pip
sudo apt update
sudo apt install python3 python3-pip -y

# 2. Installer le toolkit
pip install iso27001-toolkit

# 3. (Optionnel) Installer support PDF
pip install iso27001-toolkit[pdf]

# 4. Vérifier
iso27001 --version
```

### Comment installer sur macOS ?

```bash
# 1. Installer Python via Homebrew
brew install python

# 2. Installer le toolkit
pip3 install iso27001-toolkit

# 3. (Optionnel) PDF support
pip3 install iso27001-toolkit[pdf]

# 4. Vérifier
iso27001 --version
```

### Comment installer sur Windows ?

**Option 1 : WSL2 (recommandé)**
```powershell
# 1. Installer WSL2 + Ubuntu
wsl --install

# 2. Dans Ubuntu WSL
pip install iso27001-toolkit
```

**Option 2 : Python Windows**
```powershell
# 1. Télécharger Python depuis python.org
# 2. Dans PowerShell
pip install iso27001-toolkit
```

### L'installation échoue avec "error: externally-managed-environment"

Sur Ubuntu 23.04+, utilisez un environnement virtuel :

```bash
# Créer environnement virtuel
python3 -m venv ~/.venv/iso27001

# Activer
source ~/.venv/iso27001/bin/activate

# Installer
pip install iso27001-toolkit

# Ajouter à .bashrc pour activation auto
echo "source ~/.venv/iso27001/bin/activate" >> ~/.bashrc
```

### WeasyPrint ne s'installe pas

**Ubuntu/Debian** :
```bash
sudo apt install python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
pip install weasyprint
```

**macOS** :
```bash
brew install pango
pip install weasyprint
```

**Windows** : Utilisez WSL2 (WeasyPrint ne fonctionne pas bien sur Windows natif).

---

## Utilisation

### Comment démarrer un nouveau projet ?

```bash
# 1. Initialiser
iso27001 init

# 2. Configurer organisation
iso27001 policies configure

# 3. Vérifier santé
iso27001 doctor
```

Suivez ensuite le [Tutorial 30 min](docs/tutorials/quickstart.md).

### Où sont stockées mes données ?

Toutes vos données sont stockées localement dans `~/.iso27001/` :

```
~/.iso27001/
├── config.yml              # Configuration organisation
├── data/
│   ├── controls.yml        # État des 114 contrôles
│   ├── risks.yml          # Registre des risques
│   └── audit.yml          # Données d'audit
├── audit_trail.yml         # Journal d'audit (immuable)
└── encryption.key          # Clé de chiffrement (0600)
```

**Aucune donnée n'est envoyée sur Internet** (sauf si vous utilisez les scripts de backup cloud optionnels).

### Comment sauvegarder mes données ?

**Option 1 : Backup manuel**
```bash
cp -r ~/.iso27001/ ~/backups/iso27001-$(date +%Y%m%d)/
```

**Option 2 : Backup automatique**
```bash
# Utiliser le script fourni
bash examples/automation/weekly_backup.sh

# Ajouter au cron (hebdomadaire)
0 2 * * 1 /path/to/weekly_backup.sh
```

**Option 3 : Git (recommandé)**
```bash
cd ~/.iso27001/
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:company/iso27001-private.git
git push -u origin main
```

### Comment restaurer depuis un backup ?

```bash
# Depuis archive
tar -xzf iso27001_backup_20241115.tar.gz -C ~/

# Depuis Git
cd ~/.iso27001/
git pull origin main

# Ou
rm -rf ~/.iso27001/
git clone git@github.com:company/iso27001-private.git ~/.iso27001
```

### Puis-je travailler en équipe ?

Oui ! Plusieurs options :

**Option 1 : Git partagé (recommandé)**
```bash
# Repository Git privé (GitHub, GitLab, Bitbucket)
cd ~/.iso27001/
git init
git remote add origin git@github.com:company/iso27001.git

# Chaque membre :
git clone git@github.com:company/iso27001.git ~/.iso27001
# Travailler, puis :
git add .
git commit -m "Update controls"
git push
```

**Option 2 : Répertoire réseau partagé**
```bash
# Monter partage réseau
sudo mount -t cifs //server/iso27001 ~/.iso27001

# Ou lien symbolique
ln -s /mnt/shared/iso27001 ~/.iso27001
```

**Option 3 : API Flask (voir `examples/integration/flask_api.py`)**

### Comment migrer d'un autre outil ?

**Depuis Excel** :

1. Exporter risques en CSV
2. Utiliser `examples/scripts/import_risks_csv.py`

**Depuis un outil commercial** :

1. Exporter données (format CSV/JSON)
2. Créer script d'import personnalisé
3. Nous contacter pour assistance (ouvrir issue GitHub)

**Depuis Word/Google Docs** :

Malheureusement, import manuel requis. Comptez 1-2 jours selon volume.

---

## Certification ISO 27001

### Combien de temps pour obtenir la certification ?

**Timeline typique** :

```
Mois 1-3   : Fondations (politiques, analyse risques)
Mois 4-9   : Implémentation contrôles (vagues 1-2)
Mois 10-12 : Finalisation + audit interne
Mois 13    : Stage 1 (audit documentaire)
Mois 14-15 : Corrections
Mois 16    : Stage 2 (audit sur site)
Mois 17    : Certificat obtenu ✅
```

**Total : 12-18 mois** pour une organisation bien préparée.

**Facteurs d'accélération** :
- Équipe dédiée à temps plein
- Budget suffisant
- Culture sécurité existante
- Support consultant externe

**Facteurs de ralentissement** :
- Équipe à temps partiel
- Budget limité
- Résistance au changement
- Manque de sponsorship direction

### Quel est le coût total de la certification ?

**Budget type pour PME (50-250 employés)** :

| Poste | Coût estimé |
|-------|-------------|
| **Audit de certification** | 15k-40k€ |
| **Consultant externe** (optionnel) | 10k-50k€ |
| **Outils techniques** (MFA, SIEM, etc.) | 5k-20k€ |
| **ISO 27001 Toolkit** | Gratuit ✅ |
| **Formation équipe** | 2k-5k€ |
| **Temps interne** (RSSI, IT, etc.) | 50-100 j/h |
| **TOTAL** | **30k-120k€** |

**Audits de surveillance** (année 2-3) : 5k-15k€/an

Le toolkit permet d'**économiser 10k-30k€** vs solutions commerciales.

### Dois-je implémenter les 114 contrôles ?

**Non**, mais vous devez les **justifier tous** dans le Statement of Applicability (SoA).

**Options** :
1. **Applicable** : Implémenter (contrôle pertinent)
2. **Non applicable** : Justifier exclusion (contrôle non pertinent)

**Exemple** :
- Contrôle A.7.4 "Surveillance physique" → Non applicable si 100% télétravail
- Justification : "Organisation 100% distante, pas de locaux physiques"

**Recommandation** : Implémenter minimum 80-90% des contrôles pour certification réussie.

### Puis-je me certifier seul avec ce toolkit ?

**Techniquement oui**, mais **fortement déconseillé** si :
- Première certification
- Équipe < 5 personnes
- Budget disponible pour consultant

**Recommandation** :
- Utiliser le toolkit pour la gestion quotidienne
- Consultant externe pour :
  - Audit à blanc (pré-certification)
  - Revue documentation
  - Formation équipe
  - Support audit de certification

**Économie** : 20-30k€ avec toolkit vs 50-80k€ avec solution complète.

### Quels organismes de certification recommandez-vous ?

**Principaux organismes accrédités (France)** :
- AFNOR Certification
- Bureau Veritas
- LRQA
- SGS
- DEKRA

**Critères de choix** :
1. Accréditation COFRAC (obligatoire)
2. Expérience dans votre secteur
3. Tarifs et disponibilité
4. Recommandations pairs

**Astuce** : Demander 3 devis, comparer.

---

## Technique

### Puis-je utiliser l'API Python dans mon application ?

Oui ! Voir [Guide Développeur API](docs/api/developer-guide.md).

**Exemple rapide** :
```python
from iso27001_toolkit.utils.risk_manager import RiskManager

manager = RiskManager()
risk_id = manager.add_risk(
    title="Data breach",
    description="SQL injection vulnerability",
    probability=4,
    impact=5,
    category="confidentiality"
)
print(f"Risk created: {risk_id}")
```

### Comment intégrer dans mon CI/CD ?

Voir exemples :
- `examples/ci_cd/github_actions.yml`
- `examples/ci_cd/gitlab_ci.yml`

**GitHub Actions** :
```bash
cp examples/ci_cd/github_actions.yml .github/workflows/iso27001.yml
git add .github/
git commit -m "ci: add ISO 27001 checks"
git push
```

### Puis-je personnaliser les templates de politiques ?

Oui ! Les templates sont en **Jinja2** dans `src/iso27001_toolkit/templates/`.

**Option 1 : Modifier templates existants**
```bash
# Éditer
vim src/iso27001_toolkit/templates/policies/information_security_policy.md

# Régénérer
iso27001 policies generate -p information_security_policy
```

**Option 2 : Créer templates personnalisés**

Voir exemple détaillé dans [Guide Avancé](docs/guides/advanced-usage.md#personnalisation-des-templates).

### Comment exporter vers Excel ?

Pas d'export Excel natif, mais vous pouvez :

**Option 1 : Via Python**
```python
import yaml
import pandas as pd

# Charger risks.yml
with open('~/.iso27001/data/risks.yml') as f:
    data = yaml.safe_load(f)

# Convertir en DataFrame
df = pd.DataFrame(data['risks'])

# Export Excel
df.to_excel('risks.xlsx', index=False)
```

**Option 2 : Via CSV**
```bash
# Export en CSV (à créer)
iso27001 risks export --format csv > risks.csv

# Ouvrir dans Excel
```

---

## Sécurité

### Mes données sont-elles chiffrées ?

**Partiellement** :

✅ **Chiffrées** :
- Données sensibles via `encryption.py` (Fernet/AES-128)
- Clé stockée dans `~/.iso27001/encryption.key` (permissions 0600)

❌ **Non chiffrées** :
- Fichiers YAML (lisibles en clair)
- Audit trail

**Recommandation pour données très sensibles** :
```bash
# Chiffrer tout le répertoire avec GPG
tar -czf - ~/.iso27001/ | gpg --encrypt --recipient ciso@example.com > iso27001.tar.gz.gpg

# Ou utiliser LUKS (Linux)
# Ou FileVault (macOS)
# Ou BitLocker (Windows)
```

### Que faire en cas de fuite de données ?

**Si `~/.iso27001/` est compromis** :

1. **Immédiatement** :
   - Changer tous les mots de passe mentionnés
   - Révoquer clés de chiffrement
   - Notifier RSSI/DPO

2. **Court terme** :
   - Analyser audit trail pour identifier actions suspectes
   - Restaurer depuis backup propre
   - Renforcer permissions (`chmod 700 ~/.iso27001/`)

3. **Moyen terme** :
   - Audit de sécurité complet
   - Revoir processus d'accès
   - Former équipe

**Rappel** : Ne jamais commiter `~/.iso27001/` sur GitHub public !

### Les logs sont-ils sécurisés ?

Oui, l'**audit trail** est :
- ✅ **Append-only** (ajout uniquement, pas de suppression)
- ✅ **Horodaté** (timestamp ISO 8601)
- ✅ **Permissions restrictives** (0600)
- ✅ **Intégrité vérifiable** (via hash SHA256 optionnel)

**Recommandation** : Signer l'audit trail avec GPG mensuellement.

```bash
gpg --detach-sign --armor ~/.iso27001/audit_trail.yml
# Créé audit_trail.yml.asc

# Vérifier intégrité
gpg --verify ~/.iso27001/audit_trail.yml.asc
```

---

## Contribution

### Comment puis-je contribuer ?

Plusieurs façons :

1. **Rapporter des bugs** : [GitHub Issues](https://github.com/GitCroque/iso27001-toolbox/issues)
2. **Proposer fonctionnalités** : [GitHub Discussions](https://github.com/GitCroque/iso27001-toolbox/discussions)
3. **Soumettre code** : Fork → Branch → Pull Request
4. **Améliorer documentation** : PRs bienvenues
5. **Traduire** : Aider avec l'i18n (EN, ES, DE)

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour détails.

### Puis-je utiliser commercialement ?

**Oui !** Licence MIT permet :
- ✅ Usage commercial
- ✅ Modification
- ✅ Distribution
- ✅ Sublicensing

**Seule obligation** : Conserver la notice de copyright.

**Vous pouvez même** :
- Vendre services basés sur le toolkit
- Créer version propriétaire
- Intégrer dans produit commercial

### Y a-t-il un support commercial ?

Actuellement **non**, mais :
- 📖 Documentation exhaustive disponible
- 💬 Community support via GitHub Discussions
- 🐛 Bug fixes via GitHub Issues

**Alternatives** :
- Engager consultant ISO 27001 indépendant
- Nous contacter pour besoins spécifiques (via GitHub)

### Quelle est la roadmap du projet ?

Voir [README.md - Roadmap](README.md#roadmap).

**Priorités v0.2.0** :
- [ ] Interface web (React)
- [ ] API REST (FastAPI)
- [ ] Support multilingue (EN, ES)
- [ ] Intégration Jira/ServiceNow
- [ ] Templates procédures opérationnelles

**Contribuer à la roadmap** : [GitHub Discussions](https://github.com/GitCroque/iso27001-toolbox/discussions)

---

## 🆘 Besoin d'aide ?

**Vous ne trouvez pas votre réponse ?**

1. 📖 Consultez la [Documentation complète](README.md)
2. 🔍 Recherchez dans [GitHub Issues](https://github.com/GitCroque/iso27001-toolbox/issues)
3. 💬 Posez votre question dans [Discussions](https://github.com/GitCroque/iso27001-toolbox/discussions)
4. 🐛 Signalez un bug via [New Issue](https://github.com/GitCroque/iso27001-toolbox/issues/new)

---

**Dernière mise à jour** : 2024-11-18  
**Version FAQ** : 1.0.0  
**Contributions** : Bienvenues via PR !
