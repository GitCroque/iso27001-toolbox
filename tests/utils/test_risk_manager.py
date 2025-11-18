"""
Tests pour le module RiskManager
"""

import pytest
from pathlib import Path
from datetime import datetime

from iso27001_toolkit.utils.risk_manager import RiskManager


class TestRiskManagerInitialization:
    """Tests d'initialisation du RiskManager"""

    def test_init_creates_empty_register(self, mock_config_dir):
        """Test que l'initialisation crée un registre vide"""
        manager = RiskManager()
        assert manager.data['risks'] == []
        assert manager.data['last_updated'] is None

    def test_init_with_example_risks(self, mock_config_dir):
        """Test initialisation avec risques d'exemple"""
        manager = RiskManager()
        manager.initialize()

        assert len(manager.data['risks']) > 0
        assert manager.data['last_updated'] is not None

    def test_file_path_setup(self, mock_config_dir):
        """Test que le chemin du fichier est correct"""
        manager = RiskManager()
        assert manager.file_path.name == "risks.yml"
        assert "iso27001" in str(manager.file_path)


class TestRiskManagerAddRisk:
    """Tests d'ajout de risques"""

    def test_add_risk_basic(self, mock_config_dir, sample_risk_data):
        """Test ajout d'un risque basique"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        assert risk_id.startswith("RISK-")
        assert len(manager.get_all_risks()) == 1

        risk = manager.get_risk(risk_id)
        assert risk['name'] == sample_risk_data['name']
        assert risk['category'] == sample_risk_data['category']

    def test_add_risk_generates_unique_id(self, mock_config_dir, sample_risk_data):
        """Test que chaque risque a un ID unique"""
        manager = RiskManager()

        id1 = manager.add_risk(sample_risk_data)
        id2 = manager.add_risk(sample_risk_data)
        id3 = manager.add_risk(sample_risk_data)

        assert id1 != id2 != id3
        assert id1 == "RISK-001"
        assert id2 == "RISK-002"
        assert id3 == "RISK-003"

    def test_add_risk_calculates_score(self, mock_config_dir):
        """Test le calcul automatique du score"""
        manager = RiskManager()

        risk_id = manager.add_risk({
            'name': 'Test Risk',
            'category': 'confidentiality',
            'impact': 4,
            'likelihood': 3
        })

        risk = manager.get_risk(risk_id)
        assert risk['risk_score'] == 12  # 4 × 3
        assert risk['risk_level'] == 'high'

    def test_add_risk_determines_levels(self, mock_config_dir):
        """Test la détermination des niveaux de risque"""
        manager = RiskManager()

        # Critical (16-25)
        id_critical = manager.add_risk({
            'name': 'Critical Risk',
            'impact': 5,
            'likelihood': 5
        })
        assert manager.get_risk(id_critical)['risk_level'] == 'critical'
        assert manager.get_risk(id_critical)['risk_score'] == 25

        # High (10-15)
        id_high = manager.add_risk({
            'name': 'High Risk',
            'impact': 4,
            'likelihood': 3
        })
        assert manager.get_risk(id_high)['risk_level'] == 'high'
        assert manager.get_risk(id_high)['risk_score'] == 12

        # Medium (5-9)
        id_medium = manager.add_risk({
            'name': 'Medium Risk',
            'impact': 3,
            'likelihood': 2
        })
        assert manager.get_risk(id_medium)['risk_level'] == 'medium'
        assert manager.get_risk(id_medium)['risk_score'] == 6

        # Low (1-4)
        id_low = manager.add_risk({
            'name': 'Low Risk',
            'impact': 2,
            'likelihood': 1
        })
        assert manager.get_risk(id_low)['risk_level'] == 'low'
        assert manager.get_risk(id_low)['risk_score'] == 2

    def test_add_risk_with_defaults(self, mock_config_dir):
        """Test ajout de risque avec valeurs par défaut"""
        manager = RiskManager()

        risk_id = manager.add_risk({'name': 'Minimal Risk'})

        risk = manager.get_risk(risk_id)
        assert risk['impact'] == 3
        assert risk['likelihood'] == 3
        assert risk['status'] == 'identified'
        assert risk['treatment'] == 'mitigate'

    def test_add_risk_sets_timestamps(self, mock_config_dir, sample_risk_data):
        """Test que les timestamps sont créés"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        risk = manager.get_risk(risk_id)
        assert 'created_at' in risk
        assert 'updated_at' in risk
        assert 'review_date' in risk

        # Vérifier format ISO
        datetime.fromisoformat(risk['created_at'])
        datetime.fromisoformat(risk['updated_at'])


class TestRiskManagerGetRisk:
    """Tests de récupération de risques"""

    def test_get_risk_existing(self, mock_config_dir, sample_risk_data):
        """Test récupération d'un risque existant"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        risk = manager.get_risk(risk_id)
        assert risk is not None
        assert risk['id'] == risk_id

    def test_get_risk_nonexistent(self, mock_config_dir):
        """Test récupération d'un risque inexistant"""
        manager = RiskManager()

        risk = manager.get_risk("RISK-999")
        assert risk is None

    def test_get_all_risks_empty(self, mock_config_dir):
        """Test récupération tous risques quand vide"""
        manager = RiskManager()

        risks = manager.get_all_risks()
        assert risks == []

    def test_get_all_risks_multiple(self, mock_config_dir, sample_risk_data):
        """Test récupération de plusieurs risques"""
        manager = RiskManager()

        manager.add_risk(sample_risk_data)
        manager.add_risk(sample_risk_data)
        manager.add_risk(sample_risk_data)

        risks = manager.get_all_risks()
        assert len(risks) == 3


class TestRiskManagerUpdateRisk:
    """Tests de mise à jour de risques"""

    def test_update_risk_status(self, mock_config_dir, sample_risk_data):
        """Test mise à jour du statut"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        success = manager.update_risk(risk_id, {'status': 'treated'})

        assert success is True
        risk = manager.get_risk(risk_id)
        assert risk['status'] == 'treated'

    def test_update_risk_recalculates_score(self, mock_config_dir, sample_risk_data):
        """Test que la mise à jour recalcule le score"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        # Mettre à jour impact et likelihood
        manager.update_risk(risk_id, {'impact': 5, 'likelihood': 5})

        risk = manager.get_risk(risk_id)
        assert risk['risk_score'] == 25
        assert risk['risk_level'] == 'critical'

    def test_update_risk_only_impact(self, mock_config_dir):
        """Test mise à jour impact seulement"""
        manager = RiskManager()
        risk_id = manager.add_risk({
            'name': 'Test',
            'impact': 2,
            'likelihood': 3
        })

        manager.update_risk(risk_id, {'impact': 4})

        risk = manager.get_risk(risk_id)
        assert risk['impact'] == 4
        assert risk['likelihood'] == 3
        assert risk['risk_score'] == 12  # 4 × 3

    def test_update_risk_nonexistent(self, mock_config_dir):
        """Test mise à jour d'un risque inexistant"""
        manager = RiskManager()

        success = manager.update_risk("RISK-999", {'status': 'treated'})
        assert success is False

    def test_update_risk_updates_timestamp(self, mock_config_dir, sample_risk_data):
        """Test que updated_at est mis à jour"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        original_risk = manager.get_risk(risk_id)
        original_updated_at = original_risk['updated_at']

        import time
        time.sleep(0.01)  # Petit délai pour différencier les timestamps

        manager.update_risk(risk_id, {'status': 'treated'})

        updated_risk = manager.get_risk(risk_id)
        assert updated_risk['updated_at'] != original_updated_at


class TestRiskManagerDeleteRisk:
    """Tests de suppression de risques"""

    def test_delete_risk_existing(self, mock_config_dir, sample_risk_data):
        """Test suppression d'un risque existant"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        assert len(manager.get_all_risks()) == 1

        success = manager.delete_risk(risk_id)

        assert success is True
        assert len(manager.get_all_risks()) == 0
        assert manager.get_risk(risk_id) is None

    def test_delete_risk_nonexistent(self, mock_config_dir):
        """Test suppression d'un risque inexistant"""
        manager = RiskManager()

        success = manager.delete_risk("RISK-999")
        assert success is False


class TestRiskManagerFiltering:
    """Tests de filtrage de risques"""

    def test_get_risks_by_level(self, mock_config_dir):
        """Test filtrage par niveau"""
        manager = RiskManager()

        manager.add_risk({'name': 'Critical', 'impact': 5, 'likelihood': 5})
        manager.add_risk({'name': 'High', 'impact': 4, 'likelihood': 3})
        manager.add_risk({'name': 'High2', 'impact': 3, 'likelihood': 4})
        manager.add_risk({'name': 'Low', 'impact': 1, 'likelihood': 1})

        critical_risks = manager.get_risks_by_level('critical')
        high_risks = manager.get_risks_by_level('high')
        low_risks = manager.get_risks_by_level('low')

        assert len(critical_risks) == 1
        assert len(high_risks) == 2
        assert len(low_risks) == 1

    def test_get_risks_by_category(self, mock_config_dir):
        """Test filtrage par catégorie"""
        manager = RiskManager()

        manager.add_risk({'name': 'R1', 'category': 'confidentiality'})
        manager.add_risk({'name': 'R2', 'category': 'confidentiality'})
        manager.add_risk({'name': 'R3', 'category': 'integrity'})
        manager.add_risk({'name': 'R4', 'category': 'availability'})

        conf_risks = manager.get_risks_by_category('confidentiality')
        int_risks = manager.get_risks_by_category('integrity')

        assert len(conf_risks) == 2
        assert len(int_risks) == 1


class TestRiskManagerStatistics:
    """Tests de statistiques"""

    def test_get_statistics_empty(self, mock_config_dir):
        """Test statistiques sur registre vide"""
        manager = RiskManager()

        stats = manager.get_statistics()

        assert stats['total'] == 0
        assert stats['by_level'] == {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}

    def test_get_statistics_with_risks(self, mock_config_dir):
        """Test statistiques avec plusieurs risques"""
        manager = RiskManager()

        # Ajouter différents risques
        manager.add_risk({
            'name': 'R1',
            'impact': 5,
            'likelihood': 5,
            'status': 'identified',
            'treatment': 'mitigate'
        })
        manager.add_risk({
            'name': 'R2',
            'impact': 3,
            'likelihood': 3,
            'status': 'analyzed',
            'treatment': 'accept'
        })
        manager.add_risk({
            'name': 'R3',
            'impact': 1,
            'likelihood': 1,
            'status': 'treated',
            'treatment': 'mitigate'
        })

        stats = manager.get_statistics()

        assert stats['total'] == 3
        assert stats['by_level']['critical'] == 1
        assert stats['by_level']['medium'] == 1
        assert stats['by_level']['low'] == 1

        assert stats['by_status']['identified'] == 1
        assert stats['by_status']['analyzed'] == 1
        assert stats['by_status']['treated'] == 1

        assert stats['by_treatment']['mitigate'] == 2
        assert stats['by_treatment']['accept'] == 1


class TestRiskManagerPersistence:
    """Tests de persistence"""

    def test_save_and_load(self, mock_config_dir, sample_risk_data):
        """Test sauvegarde et rechargement"""
        manager1 = RiskManager()
        risk_id = manager1.add_risk(sample_risk_data)

        # Créer une nouvelle instance (recharge depuis le fichier)
        manager2 = RiskManager()

        risk = manager2.get_risk(risk_id)
        assert risk is not None
        assert risk['name'] == sample_risk_data['name']

    def test_last_updated_timestamp(self, mock_config_dir, sample_risk_data):
        """Test que last_updated est mis à jour"""
        manager = RiskManager()

        # Ajouter un risque met à jour le timestamp
        manager.add_risk(sample_risk_data)

        assert manager.data['last_updated'] is not None
        datetime.fromisoformat(manager.data['last_updated'])


class TestRiskManagerEdgeCases:
    """Tests de cas limites"""

    def test_add_risk_with_all_fields(self, mock_config_dir):
        """Test ajout avec tous les champs remplis"""
        manager = RiskManager()

        complete_risk = {
            'name': 'Complete Risk',
            'description': 'A complete risk description',
            'category': 'confidentiality',
            'assets': ['Server', 'Database', 'Network'],
            'impact': 4,
            'likelihood': 3,
            'status': 'analyzed',
            'treatment': 'transfer',
            'mitigation_measures': ['Measure 1', 'Measure 2'],
            'controls': ['A.5.1', 'A.8.5'],
            'owner': 'Security Team',
            'review_date': '2025-12-31'
        }

        risk_id = manager.add_risk(complete_risk)
        risk = manager.get_risk(risk_id)

        assert risk['name'] == 'Complete Risk'
        assert len(risk['assets']) == 3
        assert len(risk['mitigation_measures']) == 2
        assert len(risk['controls']) == 2
        assert risk['owner'] == 'Security Team'

    def test_risk_id_overflow_hundred(self, mock_config_dir):
        """Test génération d'ID au-delà de 100"""
        manager = RiskManager()

        # Simuler 150 risques
        for i in range(150):
            manager.add_risk({'name': f'Risk {i}'})

        risks = manager.get_all_risks()
        assert len(risks) == 150
        assert risks[-1]['id'] == 'RISK-150'

    def test_empty_mitigation_measures(self, mock_config_dir):
        """Test avec liste vide de mesures"""
        manager = RiskManager()

        risk_id = manager.add_risk({
            'name': 'Test',
            'mitigation_measures': []
        })

        risk = manager.get_risk(risk_id)
        assert risk['mitigation_measures'] == []
