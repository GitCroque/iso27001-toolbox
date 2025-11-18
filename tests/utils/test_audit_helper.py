"""
Tests pour le module AuditHelper
"""

import pytest
from pathlib import Path
from datetime import datetime

from iso27001_toolkit.utils.audit_helper import AuditHelper
from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.controls_data import get_all_controls


class TestAuditHelperInitialization:
    """Tests d'initialisation de AuditHelper"""

    def test_init_creates_helper(self, mock_config_dir):
        """Test que l'initialisation fonctionne"""
        helper = AuditHelper()
        assert helper.data['audits'] == []
        assert helper.data['checklists'] == []
        assert isinstance(helper.controls_tracker, ControlsTracker)
        assert isinstance(helper.risk_manager, RiskManager)

    def test_file_path_setup(self, mock_config_dir):
        """Test que le chemin du fichier est correct"""
        helper = AuditHelper()
        assert helper.file_path.name == "audit.yml"
        assert "iso27001" in str(helper.file_path)


class TestAuditHelperGenerateChecklist:
    """Tests de génération de checklist"""

    def test_generate_checklist_structure(self, mock_config_dir):
        """Test la structure de la checklist générée"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        checklist = helper.generate_checklist()

        assert 'generated_at' in checklist
        assert 'categories' in checklist
        assert len(checklist['categories']) > 0

        # Vérifier format timestamp
        datetime.fromisoformat(checklist['generated_at'])

    def test_generate_checklist_all_categories(self, mock_config_dir):
        """Test que toutes les catégories sont présentes"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        checklist = helper.generate_checklist()

        # Les 4 catégories ISO 27001:2022
        expected_categories = ['A.5', 'A.6', 'A.7', 'A.8']

        for category in expected_categories:
            assert category in checklist['categories']
            assert 'name' in checklist['categories'][category]
            assert 'controls' in checklist['categories'][category]

    def test_generate_checklist_control_details(self, mock_config_dir):
        """Test les détails des contrôles dans la checklist"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        checklist = helper.generate_checklist()

        # Vérifier un contrôle
        category_controls = checklist['categories']['A.5']['controls']
        assert len(category_controls) > 0

        control = category_controls[0]
        assert 'id' in control
        assert 'name' in control
        assert 'status' in control
        assert 'evidence_count' in control
        assert 'check_items' in control
        assert len(control['check_items']) == 4

    def test_generate_checklist_with_evidence(self, mock_config_dir):
        """Test checklist avec preuves"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Ajouter des preuves à un contrôle
        helper.controls_tracker.add_control_evidence('A.5.1', ['doc1.pdf', 'doc2.pdf'])
        helper.controls_tracker.save()

        checklist = helper.generate_checklist()

        # Trouver le contrôle A.5.1
        a5_controls = checklist['categories']['A.5']['controls']
        control_a51 = next(c for c in a5_controls if c['id'] == 'A.5.1')

        assert control_a51['evidence_count'] == 2


class TestAuditHelperAssessReadiness:
    """Tests d'évaluation de préparation"""

    def test_assess_readiness_basic_structure(self, mock_config_dir):
        """Test la structure du rapport de préparation"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        readiness = helper.assess_readiness()

        assert 'overall_score' in readiness
        assert 'controls_status' in readiness
        assert 'required_documents' in readiness
        assert 'recommendations' in readiness
        assert 'assessed_at' in readiness

        # Vérifier types
        assert isinstance(readiness['overall_score'], (int, float))
        assert isinstance(readiness['controls_status'], dict)
        assert isinstance(readiness['required_documents'], list)
        assert isinstance(readiness['recommendations'], list)

    def test_assess_readiness_no_implementation(self, mock_config_dir):
        """Test score avec aucune implémentation"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        readiness = helper.assess_readiness()

        # Score devrait être très bas si rien n'est implémenté
        assert readiness['overall_score'] < 50

    def test_assess_readiness_partial_implementation(self, mock_config_dir):
        """Test score avec implémentation partielle"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Implémenter 50% des contrôles
        all_controls = get_all_controls()
        for i, control in enumerate(all_controls):
            if i % 2 == 0:
                helper.controls_tracker.update_control_status(control['id'], 'implemented')

        helper.controls_tracker.save()

        readiness = helper.assess_readiness()

        # Score devrait être autour de 50% (pondéré à 70% pour les contrôles)
        assert 30 < readiness['overall_score'] < 60

    def test_assess_readiness_full_implementation(self, mock_config_dir):
        """Test score avec implémentation complète"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Tout implémenter
        all_controls = get_all_controls()
        for control in all_controls:
            helper.controls_tracker.update_control_status(control['id'], 'implemented')

        helper.controls_tracker.save()

        readiness = helper.assess_readiness()

        # Score devrait être élevé (70% des points car documents manquent)
        assert readiness['overall_score'] >= 70

    def test_assess_readiness_recommendations_not_started(self, mock_config_dir):
        """Test recommandations pour contrôles non démarrés"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        readiness = helper.assess_readiness()

        # Devrait recommander de démarrer les contrôles
        assert len(readiness['recommendations']) > 0
        assert any('non commencés' in rec for rec in readiness['recommendations'])

    def test_assess_readiness_recommendations_in_progress(self, mock_config_dir):
        """Test recommandations pour contrôles en cours"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Mettre quelques contrôles en cours
        helper.controls_tracker.update_control_status('A.5.1', 'in_progress')
        helper.controls_tracker.update_control_status('A.5.2', 'in_progress')
        helper.controls_tracker.save()

        readiness = helper.assess_readiness()

        # Devrait recommander de finaliser
        assert any('en cours' in rec for rec in readiness['recommendations'])

    def test_assess_readiness_required_documents(self, mock_config_dir):
        """Test la liste des documents requis"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        readiness = helper.assess_readiness()

        required_docs = readiness['required_documents']
        assert len(required_docs) >= 5

        # Vérifier structure
        for doc in required_docs:
            assert 'name' in doc
            assert 'exists' in doc
            assert isinstance(doc['exists'], bool)


class TestAuditHelperCollectPolicies:
    """Tests de collecte de politiques"""

    def test_collect_policies_creates_directory(self, mock_config_dir, tmp_path):
        """Test que le répertoire de sortie est créé"""
        helper = AuditHelper()
        output_dir = tmp_path / "policies"

        result = helper.collect_policies(output_dir)

        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_collect_policies_creates_readme(self, mock_config_dir, tmp_path):
        """Test qu'un README est créé"""
        helper = AuditHelper()
        output_dir = tmp_path / "policies"

        result = helper.collect_policies(output_dir)

        readme_path = output_dir / "README.md"
        assert readme_path.exists()

        content = readme_path.read_text()
        assert "Politiques de Sécurité" in content

    def test_collect_policies_statistics(self, mock_config_dir, tmp_path):
        """Test les statistiques retournées"""
        helper = AuditHelper()
        output_dir = tmp_path / "policies"

        result = helper.collect_policies(output_dir)

        assert 'total_policies' in result
        assert 'copied' in result
        assert 'missing' in result
        assert 'copied_files' in result
        assert 'missing_files' in result

        assert result['total_policies'] == 11
        assert result['copied'] + result['missing'] == result['total_policies']

    def test_collect_policies_with_existing_policy(self, mock_config_dir, tmp_path):
        """Test collecte avec une politique existante"""
        helper = AuditHelper()

        # Créer une fausse politique
        policies_dir = tmp_path / "policies_source"
        policies_dir.mkdir()
        (policies_dir / "information_security_policy.md").write_text("# Test Policy")

        # Patcher le chemin des politiques
        import iso27001_toolkit.utils.audit_helper as audit_module
        original_get_policies = audit_module.get_policies_dir

        def mock_get_policies():
            return policies_dir

        audit_module.get_policies_dir = mock_get_policies

        output_dir = tmp_path / "output"
        result = helper.collect_policies(output_dir)

        # Restaurer
        audit_module.get_policies_dir = original_get_policies

        assert result['copied'] >= 1
        assert 'information_security_policy.md' in result['copied_files']


class TestAuditHelperCollectEvidence:
    """Tests de collecte de preuves"""

    def test_collect_controls_evidence_creates_file(self, mock_config_dir, tmp_path):
        """Test que le fichier de preuves est créé"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        output_dir = tmp_path / "evidence"
        helper.collect_controls_evidence(output_dir)

        evidence_file = output_dir / "controls_evidence.md"
        assert evidence_file.exists()

        content = evidence_file.read_text()
        assert "Preuves d'implémentation" in content

    def test_collect_controls_evidence_with_implemented(self, mock_config_dir, tmp_path):
        """Test collecte avec contrôles implémentés"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Implémenter un contrôle avec preuves
        helper.controls_tracker.update_control_status('A.5.1', 'implemented')
        helper.controls_tracker.update_control_notes('A.5.1', 'Politique approuvée')
        helper.controls_tracker.add_control_evidence('A.5.1', ['doc1.pdf'])
        helper.controls_tracker.save()

        output_dir = tmp_path / "evidence"
        helper.collect_controls_evidence(output_dir)

        content = (output_dir / "controls_evidence.md").read_text()
        assert 'A.5.1' in content
        assert 'implemented' in content
        assert 'Politique approuvée' in content
        assert 'doc1.pdf' in content

    def test_collect_risk_evidence_creates_file(self, mock_config_dir, tmp_path):
        """Test que le registre des risques est créé"""
        helper = AuditHelper()

        output_dir = tmp_path / "evidence"
        helper.collect_risk_evidence(output_dir)

        risk_file = output_dir / "risk_register.md"
        assert risk_file.exists()

        content = risk_file.read_text()
        assert "Registre des risques" in content

    def test_collect_risk_evidence_with_risks(self, mock_config_dir, tmp_path):
        """Test collecte avec des risques"""
        helper = AuditHelper()

        # Ajouter un risque
        helper.risk_manager.add_risk({
            'name': 'Test Risk',
            'category': 'confidentiality',
            'impact': 4,
            'likelihood': 3,
            'mitigation_measures': ['Measure 1', 'Measure 2']
        })

        output_dir = tmp_path / "evidence"
        helper.collect_risk_evidence(output_dir)

        content = (output_dir / "risk_register.md").read_text()
        assert 'RISK-001' in content
        assert 'Test Risk' in content
        assert 'confidentiality' in content
        assert 'Measure 1' in content


class TestAuditHelperSummaryReports:
    """Tests de rapports de synthèse"""

    def test_generate_summary_reports_creates_file(self, mock_config_dir, tmp_path):
        """Test que le rapport de synthèse est créé"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        output_dir = tmp_path / "reports"
        helper.generate_summary_reports(output_dir)

        summary_file = output_dir / "readiness_summary.md"
        assert summary_file.exists()

        content = summary_file.read_text()
        assert "Rapport de préparation" in content
        assert "Score de préparation" in content

    def test_generate_summary_reports_includes_statistics(self, mock_config_dir, tmp_path):
        """Test que les statistiques sont incluses"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Implémenter quelques contrôles
        helper.controls_tracker.update_control_status('A.5.1', 'implemented')
        helper.controls_tracker.update_control_status('A.5.2', 'verified')
        helper.controls_tracker.save()

        output_dir = tmp_path / "reports"
        helper.generate_summary_reports(output_dir)

        content = (output_dir / "readiness_summary.md").read_text()

        assert 'Total:' in content
        assert 'Vérifiés:' in content
        assert 'Implémentés:' in content

    def test_generate_summary_reports_includes_recommendations(self, mock_config_dir, tmp_path):
        """Test que les recommandations sont incluses"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        output_dir = tmp_path / "reports"
        helper.generate_summary_reports(output_dir)

        content = (output_dir / "readiness_summary.md").read_text()

        assert 'Recommandations' in content


class TestAuditHelperGapAnalysis:
    """Tests d'analyse des écarts"""

    def test_perform_gap_analysis_structure(self, mock_config_dir):
        """Test la structure de l'analyse des écarts"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        gaps = helper.perform_gap_analysis()

        assert 'critical_gaps' in gaps
        assert 'major_gaps' in gaps
        assert 'minor_gaps' in gaps
        assert 'by_category' in gaps

        assert isinstance(gaps['critical_gaps'], list)
        assert isinstance(gaps['major_gaps'], list)
        assert isinstance(gaps['by_category'], dict)

    def test_perform_gap_analysis_all_not_started(self, mock_config_dir):
        """Test analyse avec tous les contrôles non démarrés"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        gaps = helper.perform_gap_analysis()

        all_controls = get_all_controls()

        # Tous devraient être des écarts critiques
        assert len(gaps['critical_gaps']) == len(all_controls)
        assert len(gaps['major_gaps']) == 0

    def test_perform_gap_analysis_in_progress(self, mock_config_dir):
        """Test analyse avec contrôles en cours"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Mettre quelques contrôles en cours
        helper.controls_tracker.update_control_status('A.5.1', 'in_progress')
        helper.controls_tracker.update_control_status('A.5.2', 'in_progress')
        helper.controls_tracker.save()

        gaps = helper.perform_gap_analysis()

        # Ces contrôles devraient être des écarts majeurs
        assert len(gaps['major_gaps']) == 2

        # Vérifier structure
        major_gap = gaps['major_gaps'][0]
        assert 'control_id' in major_gap
        assert 'name' in major_gap
        assert 'category' in major_gap
        assert major_gap['severity'] == 'major'

    def test_perform_gap_analysis_implemented_not_in_gaps(self, mock_config_dir):
        """Test que les contrôles implémentés ne sont pas dans les écarts"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Implémenter tous les contrôles
        all_controls = get_all_controls()
        for control in all_controls:
            helper.controls_tracker.update_control_status(control['id'], 'implemented')

        helper.controls_tracker.save()

        gaps = helper.perform_gap_analysis()

        # Aucun écart
        assert len(gaps['critical_gaps']) == 0
        assert len(gaps['major_gaps']) == 0

    def test_perform_gap_analysis_by_category(self, mock_config_dir):
        """Test répartition par catégorie"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        gaps = helper.perform_gap_analysis()

        # Vérifier que toutes les catégories sont présentes
        assert 'A.5' in gaps['by_category']
        assert 'A.6' in gaps['by_category']
        assert 'A.7' in gaps['by_category']
        assert 'A.8' in gaps['by_category']

        # Vérifier structure
        category_gaps = gaps['by_category']['A.5']
        assert 'name' in category_gaps
        assert 'critical' in category_gaps
        assert 'major' in category_gaps
        assert 'minor' in category_gaps


class TestAuditHelperScheduleAudit:
    """Tests de planification d'audit"""

    def test_schedule_audit_adds_to_list(self, mock_config_dir):
        """Test que l'audit est ajouté à la liste"""
        helper = AuditHelper()

        audit_info = {
            'date': '2025-12-15',
            'auditor': 'External Auditor Inc.',
            'type': 'certification',
            'scope': 'Full ISMS'
        }

        helper.schedule_audit(audit_info)

        assert len(helper.data['audits']) == 1
        assert helper.data['audits'][0] == audit_info

    def test_schedule_multiple_audits(self, mock_config_dir):
        """Test planification de plusieurs audits"""
        helper = AuditHelper()

        for i in range(3):
            helper.schedule_audit({
                'date': f'2025-{i+1:02d}-15',
                'type': 'internal' if i < 2 else 'external'
            })

        assert len(helper.data['audits']) == 3


class TestAuditHelperGenerateSOA:
    """Tests de génération de SOA"""

    def test_generate_soa_structure(self, mock_config_dir):
        """Test la structure du SOA"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        soa = helper.generate_soa()

        assert 'generated_at' in soa
        assert 'total_controls' in soa
        assert 'applicable_controls' in soa
        assert 'implemented_controls' in soa
        assert 'controls' in soa

        # Vérifier timestamp
        datetime.fromisoformat(soa['generated_at'])

    def test_generate_soa_all_controls(self, mock_config_dir):
        """Test que tous les contrôles sont dans le SOA"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        soa = helper.generate_soa()

        all_controls = get_all_controls()
        assert soa['total_controls'] == len(all_controls)
        assert len(soa['controls']) == len(all_controls)

    def test_generate_soa_control_details(self, mock_config_dir):
        """Test les détails des contrôles dans le SOA"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        soa = helper.generate_soa()

        control = soa['controls'][0]

        assert 'id' in control
        assert 'name' in control
        assert 'category' in control
        assert 'applicable' in control
        assert 'status' in control
        assert 'justification' in control
        assert 'implementation_notes' in control

    def test_generate_soa_counts_implemented(self, mock_config_dir):
        """Test le comptage des contrôles implémentés"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Implémenter 10 contrôles
        all_controls = get_all_controls()
        for i in range(10):
            helper.controls_tracker.update_control_status(all_controls[i]['id'], 'implemented')

        helper.controls_tracker.save()

        soa = helper.generate_soa()

        assert soa['implemented_controls'] == 10

    def test_generate_soa_with_notes(self, mock_config_dir):
        """Test SOA avec notes de justification"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Ajouter des notes à un contrôle
        helper.controls_tracker.update_control_notes('A.5.1', 'Custom justification notes')
        helper.controls_tracker.save()

        soa = helper.generate_soa()

        # Trouver le contrôle A.5.1
        control_a51 = next(c for c in soa['controls'] if c['id'] == 'A.5.1')

        assert control_a51['justification'] == 'Custom justification notes'
        assert control_a51['implementation_notes'] == 'Custom justification notes'


class TestAuditHelperPersistence:
    """Tests de persistence"""

    def test_save_and_load(self, mock_config_dir):
        """Test sauvegarde et rechargement"""
        helper1 = AuditHelper()

        helper1.schedule_audit({
            'date': '2025-12-15',
            'type': 'certification'
        })

        # Créer une nouvelle instance (recharge depuis le fichier)
        helper2 = AuditHelper()

        assert len(helper2.data['audits']) == 1
        assert helper2.data['audits'][0]['date'] == '2025-12-15'


class TestAuditHelperIntegration:
    """Tests d'intégration complets"""

    def test_full_audit_preparation_workflow(self, mock_config_dir, tmp_path):
        """Test workflow complet de préparation d'audit"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # 1. Implémenter quelques contrôles
        helper.controls_tracker.update_control_status('A.5.1', 'implemented')
        helper.controls_tracker.add_control_evidence('A.5.1', ['policy.pdf'])
        helper.controls_tracker.save()

        # 2. Ajouter un risque
        helper.risk_manager.add_risk({
            'name': 'Data breach',
            'category': 'confidentiality',
            'impact': 4,
            'likelihood': 3
        })

        # 3. Évaluer la préparation
        readiness = helper.assess_readiness()
        assert readiness['overall_score'] > 0

        # 4. Générer la checklist
        checklist = helper.generate_checklist()
        assert len(checklist['categories']) == 4

        # 5. Effectuer l'analyse des écarts
        gaps = helper.perform_gap_analysis()
        assert 'critical_gaps' in gaps

        # 6. Générer le SOA
        soa = helper.generate_soa()
        assert soa['implemented_controls'] >= 1

        # 7. Collecter les preuves
        evidence_dir = tmp_path / "evidence"
        helper.collect_controls_evidence(evidence_dir)
        helper.collect_risk_evidence(evidence_dir)

        assert (evidence_dir / "controls_evidence.md").exists()
        assert (evidence_dir / "risk_register.md").exists()

        # 8. Générer les rapports
        reports_dir = tmp_path / "reports"
        helper.generate_summary_reports(reports_dir)

        assert (reports_dir / "readiness_summary.md").exists()

    def test_readiness_progression(self, mock_config_dir):
        """Test progression du score de préparation"""
        helper = AuditHelper()
        helper.controls_tracker.initialize()

        # Score initial (0%)
        readiness1 = helper.assess_readiness()
        initial_score = readiness1['overall_score']

        # Implémenter 25% des contrôles
        all_controls = get_all_controls()
        quarter = len(all_controls) // 4

        for control in all_controls[:quarter]:
            helper.controls_tracker.update_control_status(control['id'], 'implemented')

        helper.controls_tracker.save()

        # Score après 25%
        readiness2 = helper.assess_readiness()
        quarter_score = readiness2['overall_score']

        # Implémenter 50% des contrôles
        for control in all_controls[:len(all_controls)//2]:
            helper.controls_tracker.update_control_status(control['id'], 'implemented')

        helper.controls_tracker.save()

        # Score après 50%
        readiness3 = helper.assess_readiness()
        half_score = readiness3['overall_score']

        # Vérifier progression
        assert initial_score < quarter_score < half_score
