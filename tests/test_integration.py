"""
Tests d'intégration end-to-end pour ISO 27001 Toolkit

Ces tests simulent des workflows complets d'utilisateur
"""

import pytest
from pathlib import Path
from datetime import datetime

from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.audit_helper import AuditHelper
from iso27001_toolkit.utils.controls_data import get_all_controls


class TestWorkflowNewOrganization:
    """Tests du workflow pour une nouvelle organisation"""

    def test_complete_setup_workflow(self, mock_config_dir, tmp_path):
        """
        Test le workflow complet de setup pour une nouvelle organisation:
        1. Initialiser le suivi des contrôles
        2. Initialiser le registre des risques
        3. Évaluer l'état initial
        """
        # 1. Initialiser les contrôles
        controls = ControlsTracker()
        controls.initialize()

        stats_initial = controls.get_statistics()
        assert stats_initial['total'] == 114
        assert stats_initial['not_started'] == 114

        # 2. Initialiser les risques
        risks = RiskManager()
        risks.initialize()

        all_risks = risks.get_all_risks()
        assert len(all_risks) > 0

        # 3. Première évaluation
        helper = AuditHelper()
        readiness = helper.assess_readiness()

        assert readiness['overall_score'] < 50  # Nouvelle org, score bas
        assert len(readiness['recommendations']) > 0


class TestWorkflowImplementation:
    """Tests du workflow d'implémentation"""

    def test_phased_implementation_workflow(self, mock_config_dir):
        """
        Test workflow d'implémentation par phases:
        Phase 1: Contrôles organisationnels (A.5)
        Phase 2: Contrôles physiques (A.7)
        Phase 3: Contrôles technologiques (A.8)
        Phase 4: Contrôles des personnes (A.6)
        """
        controls = ControlsTracker()
        controls.initialize()

        helper = AuditHelper()

        # Score initial
        readiness_initial = helper.assess_readiness()
        score_initial = readiness_initial['overall_score']

        # Phase 1: Implémenter contrôles A.5 (Organisationnels)
        all_controls = get_all_controls()
        a5_controls = [c for c in all_controls if c['id'].startswith('A.5.')]

        for control in a5_controls:
            controls.update_control_status(control['id'], 'implemented')
            controls.add_control_evidence(control['id'], [f'evidence_{control["id"]}.pdf'])

        controls.save()

        # Vérifier progression
        readiness_phase1 = helper.assess_readiness()
        score_phase1 = readiness_phase1['overall_score']
        assert score_phase1 > score_initial

        # Phase 2: Implémenter contrôles A.7 (Physiques)
        a7_controls = [c for c in all_controls if c['id'].startswith('A.7.')]

        for control in a7_controls:
            controls.update_control_status(control['id'], 'implemented')

        controls.save()

        readiness_phase2 = helper.assess_readiness()
        score_phase2 = readiness_phase2['overall_score']
        assert score_phase2 > score_phase1

        # Phase 3: Implémenter contrôles A.8 (Technologiques)
        a8_controls = [c for c in all_controls if c['id'].startswith('A.8.')]

        for control in a8_controls:
            controls.update_control_status(control['id'], 'in_progress')

        controls.save()

        readiness_phase3 = helper.assess_readiness()
        # Score peut baisser car in_progress compte moins qu'implemented
        assert readiness_phase3['overall_score'] != score_phase2

        # Phase 4: Finaliser tout
        for control in a8_controls:
            controls.update_control_status(control['id'], 'implemented')

        a6_controls = [c for c in all_controls if c['id'].startswith('A.6.')]
        for control in a6_controls:
            controls.update_control_status(control['id'], 'implemented')

        controls.save()

        readiness_final = helper.assess_readiness()
        score_final = readiness_final['overall_score']

        # Score final devrait être très élevé
        assert score_final >= 70
        assert score_final > score_initial


class TestWorkflowRiskManagement:
    """Tests du workflow de gestion des risques"""

    def test_complete_risk_management_cycle(self, mock_config_dir):
        """
        Test cycle complet de gestion des risques:
        1. Identification
        2. Analyse
        3. Traitement
        4. Monitoring
        """
        risks = RiskManager()

        # 1. Identification de risques
        risk_ids = []
        for i in range(5):
            risk_data = {
                'name': f'Risk {i+1}',
                'description': f'Description of risk {i+1}',
                'category': ['confidentiality', 'integrity', 'availability'][i % 3],
                'assets': [f'Asset {i+1}'],
                'impact': (i % 5) + 1,
                'likelihood': ((i * 2) % 5) + 1
            }
            risk_id = risks.add_risk(risk_data)
            risk_ids.append(risk_id)

        assert len(risks.get_all_risks()) == 5

        # 2. Analyse des risques
        stats_initial = risks.get_statistics()
        assert stats_initial['total'] == 5

        # Mettre à jour les statuts
        for risk_id in risk_ids:
            risks.update_risk(risk_id, {'status': 'analyzed'})

        # 3. Traitement des risques critiques/élevés
        high_risks = risks.get_risks_by_level('high') + risks.get_risks_by_level('critical')

        for risk in high_risks:
            risks.update_risk(risk['id'], {
                'status': 'treated',
                'treatment': 'mitigate'
            })

        # 4. Acceptation des risques faibles
        low_risks = risks.get_risks_by_level('low')

        for risk in low_risks:
            risks.update_risk(risk['id'], {
                'status': 'accepted',
                'treatment': 'accept'
            })

        # Vérifier état final
        final_stats = risks.get_statistics()
        assert final_stats['by_status'].get('treated', 0) >= 0
        assert final_stats['by_status'].get('accepted', 0) >= 0


class TestWorkflowAuditPreparation:
    """Tests du workflow de préparation d'audit"""

    def test_complete_audit_preparation_workflow(self, mock_config_dir, tmp_path):
        """
        Test workflow complet de préparation d'audit:
        1. Implémentation des contrôles
        2. Documentation des risques
        3. Collecte des preuves
        4. Génération des rapports
        5. Évaluation de la préparation
        """
        # Setup
        controls = ControlsTracker()
        controls.initialize()

        risks = RiskManager()
        risks.initialize()

        helper = AuditHelper()

        # 1. Implémenter des contrôles avec preuves
        high_priority_controls = ['A.5.1', 'A.5.15', 'A.5.16', 'A.8.1', 'A.8.2', 'A.8.5']

        for control_id in high_priority_controls:
            controls.update_control_status(control_id, 'implemented')
            controls.update_control_priority(control_id, 'high')
            controls.update_control_notes(control_id, f'Implémenté et testé pour {control_id}')
            controls.add_control_evidence(control_id, [
                f'{control_id}_policy.pdf',
                f'{control_id}_procedure.pdf',
                f'{control_id}_evidence.xlsx'
            ])

        controls.save()

        # 2. Documenter les risques principaux
        major_risks = [
            {
                'name': 'Accès non autorisé aux données',
                'category': 'confidentiality',
                'impact': 5,
                'likelihood': 3,
                'treatment': 'mitigate',
                'mitigation_measures': [
                    'Mise en place de l\'authentification multi-facteurs',
                    'Contrôles d\'accès basés sur les rôles',
                    'Audit des accès'
                ],
                'controls': ['A.5.15', 'A.5.16', 'A.8.5']
            },
            {
                'name': 'Perte de données',
                'category': 'availability',
                'impact': 4,
                'likelihood': 2,
                'treatment': 'mitigate',
                'mitigation_measures': [
                    'Sauvegardes régulières',
                    'Plan de reprise d\'activité',
                    'Réplication des données'
                ],
                'controls': ['A.8.13', 'A.8.14']
            }
        ]

        for risk_data in major_risks:
            risk_id = risks.add_risk(risk_data)
            risks.update_risk(risk_id, {'status': 'treated'})

        # 3. Collecte des preuves
        evidence_dir = tmp_path / "audit_evidence"

        helper.collect_controls_evidence(evidence_dir)
        helper.collect_risk_evidence(evidence_dir)

        # Vérifier que les fichiers sont créés
        assert (evidence_dir / "controls_evidence.md").exists()
        assert (evidence_dir / "risk_register.md").exists()

        # Vérifier le contenu
        controls_evidence = (evidence_dir / "controls_evidence.md").read_text()
        assert 'A.5.1' in controls_evidence
        assert 'policy.pdf' in controls_evidence

        risk_evidence = (evidence_dir / "risk_register.md").read_text()
        assert 'RISK-001' in risk_evidence

        # 4. Génération des rapports
        reports_dir = tmp_path / "audit_reports"

        # Rapport de synthèse
        helper.generate_summary_reports(reports_dir)
        assert (reports_dir / "readiness_summary.md").exists()

        # Checklist d'audit
        checklist = helper.generate_checklist()
        assert len(checklist['categories']) == 4

        # Analyse des écarts
        gaps = helper.perform_gap_analysis()
        assert 'critical_gaps' in gaps
        assert 'major_gaps' in gaps

        # SOA
        soa = helper.generate_soa()
        assert soa['implemented_controls'] >= len(high_priority_controls)

        # 5. Évaluation finale de la préparation
        readiness = helper.assess_readiness()

        # Vérifier que nous avons un score raisonnable
        assert readiness['overall_score'] > 0
        assert 'recommendations' in readiness

        # Planifier l'audit
        helper.schedule_audit({
            'date': '2025-12-15',
            'auditor': 'External Certification Body',
            'type': 'certification',
            'scope': 'Full ISMS'
        })

        assert len(helper.data['audits']) == 1


class TestWorkflowContinuousImprovement:
    """Tests du workflow d'amélioration continue"""

    def test_continuous_improvement_cycle(self, mock_config_dir):
        """
        Test cycle PDCA (Plan-Do-Check-Act):
        1. Plan: Identifier les écarts
        2. Do: Implémenter les contrôles
        3. Check: Vérifier l'implémentation
        4. Act: Corriger et améliorer
        """
        controls = ControlsTracker()
        controls.initialize()

        helper = AuditHelper()

        # Cycle 1: Premier tour PDCA

        # Plan: Identifier les écarts critiques
        gaps_cycle1 = helper.perform_gap_analysis()
        critical_controls = [g['control_id'] for g in gaps_cycle1['critical_gaps'][:10]]

        # Do: Implémenter les contrôles critiques
        for control_id in critical_controls:
            controls.update_control_status(control_id, 'in_progress')

        controls.save()

        # Check: Vérifier la progression
        readiness_mid = helper.assess_readiness()
        score_mid = readiness_mid['overall_score']

        # Act: Finaliser l'implémentation
        for control_id in critical_controls:
            controls.update_control_status(control_id, 'implemented')

        controls.save()

        readiness_end_cycle1 = helper.assess_readiness()
        score_end_cycle1 = readiness_end_cycle1['overall_score']

        # Vérifier amélioration
        assert score_end_cycle1 > score_mid

        # Cycle 2: Deuxième tour PDCA

        # Plan: Identifier les nouveaux écarts
        gaps_cycle2 = helper.perform_gap_analysis()

        # Do: Implémenter plus de contrôles
        major_controls = [g['control_id'] for g in gaps_cycle2['major_gaps'][:10]]

        for control_id in major_controls:
            controls.update_control_status(control_id, 'implemented')

        controls.save()

        # Check: Évaluation finale
        readiness_final = helper.assess_readiness()
        score_final = readiness_final['overall_score']

        # Act: Vérification de l'amélioration continue
        assert score_final > score_end_cycle1


class TestWorkflowRecertification:
    """Tests du workflow de recertification"""

    def test_recertification_workflow(self, mock_config_dir):
        """
        Test workflow de recertification (après 3 ans):
        1. Audit de l'état actuel
        2. Mise à jour des contrôles
        3. Revue des risques
        4. Préparation audit de surveillance
        """
        # Simuler une organisation déjà certifiée
        controls = ControlsTracker()
        controls.initialize()

        risks = RiskManager()
        risks.initialize()

        helper = AuditHelper()

        # État initial: tous les contrôles implémentés
        all_controls = get_all_controls()
        for control in all_controls:
            controls.update_control_status(control['id'], 'implemented')

        controls.save()

        # 1. Audit initial (score devrait être élevé)
        readiness_initial = helper.assess_readiness()
        assert readiness_initial['overall_score'] >= 70

        # 2. Mise à jour: simuler quelques contrôles à revoir
        controls_to_review = all_controls[:20]

        for control in controls_to_review:
            controls.update_control_status(control['id'], 'in_progress')

        controls.save()

        # Score devrait baisser temporairement
        readiness_review = helper.assess_readiness()
        assert readiness_review['overall_score'] < readiness_initial['overall_score']

        # 3. Revue et mise à jour des contrôles
        for control in controls_to_review:
            controls.update_control_status(control['id'], 'verified')
            controls.add_control_evidence(control['id'], [
                f'{control["id"]}_review_2025.pdf'
            ])

        controls.save()

        # 4. Préparation finale
        readiness_final = helper.assess_readiness()

        # Score devrait revenir au niveau élevé
        assert readiness_final['overall_score'] >= readiness_initial['overall_score']

        # Vérifier que les contrôles sont à jour
        stats = controls.get_statistics()
        assert stats['verified'] >= len(controls_to_review)


class TestWorkflowMultipleOrganizations:
    """Tests simulant plusieurs organisations"""

    def test_different_organization_profiles(self, mock_config_dir):
        """
        Test différents profils d'organisation:
        1. Startup (peu de contrôles)
        2. PME (contrôles moyens)
        3. Grande entreprise (tous les contrôles)
        """
        # Profil 1: Startup - Contrôles essentiels seulement
        controls_startup = ControlsTracker()
        controls_startup.initialize()

        essential_controls = [
            'A.5.1',   # Politiques
            'A.5.15',  # Contrôle d'accès
            'A.5.16',  # Gestion des identités
            'A.5.33',  # Sécurité des enregistrements
            'A.8.1',   # Équipements terminaux
            'A.8.5',   # Authentification
            'A.8.9',   # Gestion de la configuration
            'A.8.23',  # Filtrage web
        ]

        for control_id in essential_controls:
            controls_startup.update_control_status(control_id, 'implemented')

        controls_startup.save()

        helper_startup = AuditHelper()
        readiness_startup = helper_startup.assess_readiness()

        # Startup devrait avoir un score modéré
        assert 10 < readiness_startup['overall_score'] < 40

        # Profil 2: PME - 50% des contrôles
        controls_pme = ControlsTracker()
        controls_pme.initialize()

        all_controls = get_all_controls()
        pme_controls = all_controls[:len(all_controls)//2]

        for control in pme_controls:
            controls_pme.update_control_status(control['id'], 'implemented')

        controls_pme.save()

        helper_pme = AuditHelper()
        readiness_pme = helper_pme.assess_readiness()

        # PME devrait avoir un score moyen
        assert 30 < readiness_pme['overall_score'] < 60

        # Profil 3: Grande entreprise - 100% des contrôles
        controls_enterprise = ControlsTracker()
        controls_enterprise.initialize()

        for control in all_controls:
            controls_enterprise.update_control_status(control['id'], 'verified')
            controls_enterprise.add_control_evidence(control['id'], [
                f'{control["id"]}_policy.pdf',
                f'{control["id"]}_procedure.pdf',
                f'{control["id"]}_audit_report.pdf'
            ])

        controls_enterprise.save()

        helper_enterprise = AuditHelper()
        readiness_enterprise = helper_enterprise.assess_readiness()

        # Grande entreprise devrait avoir le meilleur score
        assert readiness_enterprise['overall_score'] > 70
        assert readiness_enterprise['overall_score'] > readiness_pme['overall_score']
        assert readiness_pme['overall_score'] > readiness_startup['overall_score']


class TestWorkflowErrorRecovery:
    """Tests de récupération après erreurs"""

    def test_recovery_from_audit_failure(self, mock_config_dir):
        """
        Test récupération après échec d'audit:
        1. Audit échoué
        2. Analyse des écarts
        3. Plan d'action
        4. Implémentation corrective
        5. Ré-audit
        """
        controls = ControlsTracker()
        controls.initialize()

        helper = AuditHelper()

        # Simuler implémentation partielle (audit va échouer)
        all_controls = get_all_controls()

        for i, control in enumerate(all_controls):
            if i % 3 == 0:  # Seulement 33% implémentés
                controls.update_control_status(control['id'], 'implemented')
            elif i % 3 == 1:
                controls.update_control_status(control['id'], 'in_progress')
            # Le reste: not_started

        controls.save()

        # 1. Premier audit (échec attendu)
        readiness_audit1 = helper.assess_readiness()
        assert readiness_audit1['overall_score'] < 75  # Échec

        # 2. Analyse des écarts détaillée
        gaps = helper.perform_gap_analysis()

        critical_gaps_count = len(gaps['critical_gaps'])
        major_gaps_count = len(gaps['major_gaps'])

        assert critical_gaps_count > 0

        # 3. Plan d'action: Corriger les écarts critiques en priorité
        for gap in gaps['critical_gaps']:
            controls.update_control_status(gap['control_id'], 'in_progress')

        controls.save()

        # 4. Implémentation corrective
        for gap in gaps['critical_gaps']:
            controls.update_control_status(gap['control_id'], 'implemented')
            controls.add_control_evidence(gap['control_id'], [
                f'{gap["control_id"]}_corrective_action.pdf'
            ])

        # Corriger aussi les écarts majeurs
        for gap in gaps['major_gaps']:
            controls.update_control_status(gap['control_id'], 'implemented')

        controls.save()

        # 5. Ré-audit
        readiness_audit2 = helper.assess_readiness()

        # Score devrait être beaucoup mieux
        assert readiness_audit2['overall_score'] > readiness_audit1['overall_score']
        assert readiness_audit2['overall_score'] >= 70  # Succès


class TestWorkflowRealWorld:
    """Tests de scénarios réels complexes"""

    def test_realistic_18_month_implementation(self, mock_config_dir, tmp_path):
        """
        Test scénario réaliste d'implémentation sur 18 mois:
        Mois 0-3: Planification et contrôles organisationnels
        Mois 3-6: Contrôles techniques de base
        Mois 6-12: Contrôles techniques avancés et physiques
        Mois 12-15: Contrôles des personnes et finalisation
        Mois 15-18: Préparation audit et certification
        """
        controls = ControlsTracker()
        controls.initialize()

        risks = RiskManager()
        helper = AuditHelper()

        scores_timeline = []

        # Mois 0-3: Phase 1
        phase1_controls = [c for c in get_all_controls() if c['id'].startswith('A.5.')][:15]

        for control in phase1_controls:
            controls.update_control_status(control['id'], 'implemented')
            controls.update_control_priority(control['id'], 'high')

        controls.save()

        readiness_month3 = helper.assess_readiness()
        scores_timeline.append(('Month 3', readiness_month3['overall_score']))

        # Ajouter des risques identifiés
        risks.add_risk({
            'name': 'Unauthorized access to sensitive data',
            'category': 'confidentiality',
            'impact': 5,
            'likelihood': 4,
            'treatment': 'mitigate'
        })

        # Mois 3-6: Phase 2
        phase2_controls = [c for c in get_all_controls() if c['id'].startswith('A.8.')][:10]

        for control in phase2_controls:
            controls.update_control_status(control['id'], 'implemented')

        controls.save()

        readiness_month6 = helper.assess_readiness()
        scores_timeline.append(('Month 6', readiness_month6['overall_score']))

        # Mois 6-12: Phase 3
        phase3_controls = (
            [c for c in get_all_controls() if c['id'].startswith('A.8.')][10:] +
            [c for c in get_all_controls() if c['id'].startswith('A.7.')]
        )

        for control in phase3_controls:
            controls.update_control_status(control['id'], 'implemented')

        controls.save()

        readiness_month12 = helper.assess_readiness()
        scores_timeline.append(('Month 12', readiness_month12['overall_score']))

        # Mois 12-15: Phase 4
        phase4_controls = (
            [c for c in get_all_controls() if c['id'].startswith('A.6.')] +
            [c for c in get_all_controls() if c['id'].startswith('A.5.')][15:]
        )

        for control in phase4_controls:
            controls.update_control_status(control['id'], 'implemented')
            controls.add_control_evidence(control['id'], [f'{control["id"]}_evidence.pdf'])

        controls.save()

        readiness_month15 = helper.assess_readiness()
        scores_timeline.append(('Month 15', readiness_month15['overall_score']))

        # Mois 15-18: Préparation finale
        # Vérifier tous les contrôles implémentés
        all_controls = get_all_controls()
        for control in all_controls:
            current_status = controls.get_control_status(control['id'])
            if current_status == 'implemented':
                controls.update_control_status(control['id'], 'verified')

        controls.save()

        # Collecter toutes les preuves
        evidence_dir = tmp_path / "certification_evidence"
        helper.collect_controls_evidence(evidence_dir)
        helper.collect_risk_evidence(evidence_dir)
        helper.generate_summary_reports(evidence_dir)

        # Générer le SOA final
        soa = helper.generate_soa()

        readiness_month18 = helper.assess_readiness()
        scores_timeline.append(('Month 18', readiness_month18['overall_score']))

        # Vérifications finales
        # 1. Progression constante
        for i in range(len(scores_timeline) - 1):
            assert scores_timeline[i+1][1] >= scores_timeline[i][1], \
                f"Score devrait augmenter entre {scores_timeline[i][0]} et {scores_timeline[i+1][0]}"

        # 2. Score final élevé
        assert readiness_month18['overall_score'] >= 70

        # 3. SOA complet
        assert soa['implemented_controls'] == 114 or soa['implemented_controls'] == soa['total_controls']

        # 4. Tous les fichiers de preuves créés
        assert (evidence_dir / "controls_evidence.md").exists()
        assert (evidence_dir / "risk_register.md").exists()
        assert (evidence_dir / "readiness_summary.md").exists()

        # 5. Recommandations minimales
        assert len(readiness_month18['recommendations']) <= 3

        # Planifier l'audit de certification
        helper.schedule_audit({
            'date': '2026-06-15',
            'auditor': 'ISO Certification Body',
            'type': 'certification',
            'scope': 'Full ISMS - All 114 controls',
            'expected_duration': '5 days'
        })

        assert len(helper.data['audits']) == 1
