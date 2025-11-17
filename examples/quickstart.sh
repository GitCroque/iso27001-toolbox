#!/bin/bash
# Script de démarrage rapide pour ISO 27001 Toolkit

echo "🚀 ISO 27001 Toolkit - Démarrage rapide"
echo "======================================"
echo ""

# Étape 1 : Configuration
echo "📝 Étape 1 : Configuration de l'organisation"
echo "Lancement de la configuration interactive..."
iso27001 policies configure

echo ""
echo "✅ Configuration terminée !"
echo ""

# Étape 2 : Génération des politiques
echo "📄 Étape 2 : Génération des politiques de sécurité"
echo "Génération en cours..."
iso27001 policies generate -o output/policies

echo ""
echo "✅ Politiques générées !"
echo ""

# Étape 3 : Initialisation du suivi des contrôles
echo "✅ Étape 3 : Initialisation du suivi des contrôles"
iso27001 controls init

echo ""
echo "📊 Affichage du résumé des contrôles..."
iso27001 controls list -f summary

echo ""
echo "✅ Contrôles initialisés !"
echo ""

# Étape 4 : Initialisation du registre des risques
echo "⚠️  Étape 4 : Initialisation du registre des risques"
iso27001 risks init

echo ""
echo "📊 Affichage des risques..."
iso27001 risks list

echo ""
echo "✅ Registre des risques initialisé !"
echo ""

# Étape 5 : Évaluation de la préparation
echo "🎯 Étape 5 : Évaluation de la préparation à l'audit"
iso27001 audit readiness

echo ""
echo "✅ Évaluation terminée !"
echo ""

# Résumé
echo "=========================================="
echo "✨ Configuration initiale terminée !"
echo ""
echo "📁 Fichiers générés :"
echo "   - output/policies/ : Politiques de sécurité"
echo "   - ~/.iso27001/ : Configuration et données"
echo ""
echo "🎓 Prochaines étapes :"
echo "   1. Revoir et adapter les politiques générées"
echo "   2. Commencer à mettre à jour les contrôles :"
echo "      iso27001 controls update A.5.1 --status in_progress"
echo "   3. Ajouter vos risques spécifiques :"
echo "      iso27001 risks add --interactive"
echo "   4. Générer des rapports régulièrement :"
echo "      iso27001 controls report"
echo ""
echo "📚 Documentation : README.md"
echo "❓ Aide : iso27001 --help"
echo ""
echo "Bonne chance dans votre démarche ISO 27001 ! 🎉"
