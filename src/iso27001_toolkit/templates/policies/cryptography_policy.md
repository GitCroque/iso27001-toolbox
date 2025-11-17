# Politique de Cryptographie

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0
**Propriétaire:** {{ ciso_name }}

## 1. Objectif

Cette politique définit les règles d'utilisation de la cryptographie pour protéger la confidentialité, l'intégrité et l'authenticité des informations de {{ organization_name }}.

## 2. Portée

Cette politique s'applique à :
- Toutes les technologies cryptographiques utilisées
- Tous les types de données (repos, transit, traitement)
- Tous les environnements (production, développement, test)
- Tous les utilisateurs et systèmes

## 3. Principes généraux

- La cryptographie est utilisée pour protéger les informations sensibles
- Seuls les algorithmes approuvés et standards sont utilisés
- Les clés cryptographiques sont gérées de manière sécurisée
- La conformité réglementaire est respectée

## 4. Algorithmes approuvés

### 4.1 Chiffrement symétrique

**Approuvé :**
- AES (Advanced Encryption Standard) 256-bit (recommandé)
- AES 128-bit (acceptable)
- ChaCha20 (acceptable)

**Interdit :**
- DES, 3DES
- RC4
- Blowfish

### 4.2 Chiffrement asymétrique

**Approuvé :**
- RSA ≥ 3072-bit (recommandé 4096-bit)
- ECC (Elliptic Curve) ≥ 256-bit
- Ed25519 (signatures)

**Interdit :**
- RSA < 2048-bit
- DSA

### 4.3 Fonctions de hachage

**Approuvé :**
- SHA-256, SHA-384, SHA-512 (famille SHA-2)
- SHA-3 (Keccak)
- BLAKE2

**Interdit :**
- MD5
- SHA-1

### 4.4 Protocoles cryptographiques

**Approuvé :**
- TLS 1.3 (recommandé)
- TLS 1.2 (acceptable)
- SSH-2
- IPsec

**Interdit :**
- SSL v2, SSL v3
- TLS 1.0, TLS 1.1
- SSH-1

## 5. Cas d'usage

### 5.1 Données au repos (Data at Rest)

**Chiffrement obligatoire pour :**
- Données personnelles (RGPD)
- Informations classifiées "Confidentiel" ou "Secret"
- Bases de données contenant des données sensibles
- Sauvegardes
- Supports amovibles (USB, disques externes)
- Ordinateurs portables et appareils mobiles

**Méthode :**
- Chiffrement complet du disque (FDE) : BitLocker, LUKS, FileVault
- Chiffrement au niveau fichier : GPG, 7-Zip avec AES
- Chiffrement base de données : TDE (Transparent Data Encryption)

### 5.2 Données en transit (Data in Transit)

**Chiffrement obligatoire pour :**
- Authentification
- Transfert de données sensibles
- Communications email de documents confidentiels
- Accès distant (VPN)
- API et services web

**Méthode :**
- HTTPS (TLS 1.2+) pour applications web
- SFTP ou SCP pour transferts de fichiers
- S/MIME ou PGP pour emails sensibles
- VPN avec IPsec ou OpenVPN

### 5.3 Signatures électroniques

Utiliser les signatures pour :
- Documents contractuels
- Logiciels et mises à jour
- Communications officielles importantes
- Approbations électroniques

## 6. Gestion des clés cryptographiques

### 6.1 Génération des clés

- Utiliser des générateurs de nombres aléatoires cryptographiquement sûrs (CSPRNG)
- Longueur minimale selon algorithme (voir section 4)
- Génération dans un environnement sécurisé
- Documentation de la génération

### 6.2 Stockage des clés

**Clés symétriques :**
- HSM (Hardware Security Module) pour clés maîtres
- Gestionnaire de secrets (ex: HashiCorp Vault) pour clés d'application
- Jamais en clair dans le code source
- Jamais dans les fichiers de configuration non chiffrés

**Clés privées :**
- Protection par mot de passe fort
- Stockage dans HSM ou TPM si possible
- Permissions d'accès strictes
- Sauvegarde chiffrée dans un coffre-fort sécurisé

### 6.3 Distribution des clés

- Canal sécurisé séparé de la donnée chiffrée
- Mécanisme d'échange de clés sécurisé (ex: Diffie-Hellman)
- Authentification du destinataire
- Accusé de réception

### 6.4 Rotation des clés

**Fréquence de rotation :**
- Clés de chiffrement symétrique : Tous les 12 mois
- Certificats TLS : Tous les 12-24 mois
- Clés SSH : Tous les 24 mois
- Clés d'API : Tous les 6 mois
- Rotation immédiate si compromission suspectée

### 6.5 Révocation et destruction

**Révocation :**
- Processus documenté de révocation
- Mise à jour des CRL (Certificate Revocation List)
- Notification des parties concernées

**Destruction :**
- Effacement sécurisé (zéroïsation)
- Destruction physique pour clés sur matériel
- Documentation de la destruction
- Validation de la destruction complète

## 7. Certificats numériques

### 7.1 Autorités de certification

- Utiliser uniquement des CA publiques reconnues pour les services externes
- PKI interne pour les certificats internes
- Validation de la chaîne de confiance

### 7.2 Gestion des certificats

- Inventaire de tous les certificats
- Surveillance des dates d'expiration
- Renouvellement avant expiration (30 jours minimum)
- Révocation immédiate si compromis

## 8. Conformité réglementaire

### 8.1 RGPD
- Chiffrement des données personnelles sensibles
- Pseudonymisation quand approprié
- Capacité de prouver les mesures de protection

### 8.2 Contrôles à l'exportation
- Respect des lois sur l'exportation de cryptographie
- Documentation des algorithmes utilisés
- Déclaration si nécessaire

## 9. Responsabilités

### 9.1 RSSI
- Maintenir et mettre à jour cette politique
- Approuver les algorithmes et technologies
- Superviser la gestion des clés
- Auditer l'utilisation de la cryptographie

### 9.2 Administrateurs systèmes
- Implémenter les contrôles cryptographiques
- Gérer les certificats et clés
- Surveiller les expirations
- Appliquer les correctifs de sécurité

### 9.3 Développeurs
- Utiliser uniquement les algorithmes approuvés
- Ne jamais implémenter leur propre cryptographie
- Utiliser des bibliothèques cryptographiques reconnues
- Gérer les clés de manière sécurisée

### 9.4 Utilisateurs
- Protéger leurs clés privées
- Utiliser des mots de passe forts pour les clés
- Ne jamais partager leurs clés privées
- Signaler toute compromission suspectée

## 10. Bibliothèques et outils approuvés

**Bibliothèques cryptographiques :**
- OpenSSL (version récente)
- LibreSSL
- Bouncy Castle
- cryptography (Python)
- NaCl/libsodium

**Outils :**
- GnuPG pour chiffrement de fichiers
- OpenSSH pour accès distant
- BitLocker / LUKS / FileVault pour FDE
- Let's Encrypt pour certificats TLS

## 11. Restrictions

**Interdit :**
- Développer ses propres algorithmes cryptographiques
- Utiliser des algorithmes obsolètes ou faibles
- Stocker des clés en clair
- Partager des clés privées
- Contourner les contrôles cryptographiques
- Exporter la cryptographie sans autorisation

## 12. Incidents cryptographiques

Signaler immédiatement :
- Compromission suspectée de clés
- Failles dans l'implémentation cryptographique
- Découverte de faiblesses dans les algorithmes utilisés
- Perte de clés ou certificats
- Erreurs de configuration cryptographique

## 13. Veille technologique

- Surveillance des vulnérabilités cryptographiques
- Suivi des recommandations ANSSI et NIST
- Mise à jour régulière des algorithmes
- Plan de migration pour algorithmes obsolètes

## 14. Tests et audits

- Tests de configuration cryptographique
- Scans de vulnérabilité
- Audit des certificats
- Revue du code utilisant la cryptographie
- Tests de pénétration

## 15. Formation

- Formation des développeurs aux bonnes pratiques
- Sensibilisation des utilisateurs au chiffrement
- Formation spécialisée pour les administrateurs PKI

## 16. Revue

Cette politique est révisée :
- Annuellement
- Lors de découverte de vulnérabilités majeures
- Lors de changements réglementaires
- Lors d'évolution des standards

## 17. Références

- ANSSI : Référentiel Général de Sécurité (RGS)
- NIST : Cryptographic Standards and Guidelines
- ISO/IEC 27001:2022 - Contrôle A.8.24
- Politique de sécurité de l'information

## 18. Approbation

**Approuvé par :** [Nom du Directeur Général]
**Titre :** Directeur Général
**Date :** {{ effective_date }}
**Signature :** _________________________

## 19. Contact

**RSSI :** {{ ciso_name }}
**Email :** {{ ciso_email }}

---

*Document généré le {{ current_date }}*
*Conforme à ISO/IEC 27001:2022 - Contrôle A.8.24*
