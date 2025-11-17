# Politique de Sécurité des Communications

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0

## 1. Objectif
Protéger les informations dans les réseaux et leurs installations de support.

## 2. Sécurité réseau
- Segmentation réseau (VLANs)
- Pare-feu entre segments
- IDS/IPS pour détection intrusions
- DMZ pour services exposés

## 3. Chiffrement des communications
- TLS 1.2+ obligatoire pour web
- VPN pour accès distant
- WiFi WPA3 uniquement
- Emails sensibles chiffrés (S/MIME/PGP)

## 4. Transfert d'information
- HTTPS pour transferts web
- SFTP/SCP pour fichiers
- Validation destinataire
- Confirmation de réception si sensible

## 5. Messagerie électronique
- Formation anti-phishing
- SPF, DKIM, DMARC configurés
- Filtrage anti-spam
- Bannières emails externes
- Signature automatique

## 6. Accords de confidentialité
- NDA pour partenaires/fournisseurs
- Clauses confidentialité dans contrats
- Revue annuelle des accords

## 7. Accès distant
- VPN avec MFA obligatoire
- Postes conformes standards sécurité
- Journalisation connexions
- Revue trimestrielle des accès

## 8. WiFi
- Réseau invités isolé
- Authentification 802.1X pour réseau corporate
- SSID non diffusé pour réseau interne
- Revue trimestrielle des accès WiFi

## 9. Contact
**RSSI :** {{ ciso_name }} - {{ ciso_email }}

---
*Conforme ISO 27001:2022 - Contrôles A.5.13-14, A.8.20-24*
