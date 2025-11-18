"""Tests pour le moteur de templates"""

import pytest
from pathlib import Path
from iso27001_toolkit.utils.template_engine import TemplateEngine


@pytest.fixture
def engine():
    """Crée un moteur de templates pour les tests"""
    return TemplateEngine()


@pytest.fixture
def sample_context():
    """Contexte de test pour le rendu"""
    return {
        'organization_name': 'Test Corp',
        'organization_city': 'Paris',
        'organization_country': 'France',
        'ciso_name': 'John Doe',
        'ciso_email': 'john@test.com',
        'dpo_name': 'Jane Doe',
        'dpo_email': 'jane@test.com',
        'effective_date': '2024-01-01',
        'review_period': 12
    }


def test_engine_initialization(engine):
    """Test l'initialisation du moteur"""
    assert engine.env is not None
    assert engine.template_dir.exists()


def test_render_policy(engine, sample_context):
    """Test le rendu d'une politique"""
    content = engine.render_policy('information_security_policy', sample_context)

    assert 'Test Corp' in content
    assert 'John Doe' in content
    assert '2024-01-01' in content
    assert 'Politique de Sécurité de l\'Information' in content


def test_render_nonexistent_policy(engine, sample_context):
    """Test le rendu d'une politique inexistante"""
    with pytest.raises(FileNotFoundError):
        engine.render_policy('nonexistent_policy', sample_context)


def test_render_risk_report(engine):
    """Test le rendu d'un rapport de risques"""
    context = {
        'generation_date': '2024-01-01',
        'total_risks': 10,
        'critical_risks': 2,
        'high_risks': 3,
        'medium_risks': 4,
        'low_risks': 1,
        'risks': [
            {
                'id': 'RISK-001',
                'name': 'Test Risk',
                'description': 'Test',
                'category': 'confidentiality',
                'risk_level': 'high',
                'risk_score': 12,
                'treatment': 'mitigate'
            }
        ]
    }

    content = engine.render_risk_report(context)
    assert 'Rapport d\'évaluation des risques' in content
    assert 'RISK-001' in content
    assert 'Test Risk' in content


def test_render_gap_analysis(engine):
    """Test le rendu d'une analyse des écarts"""
    gaps = {
        'critical_gaps': [
            {'control_id': 'A.5.1', 'name': 'Test Control', 'category': 'A.5'}
        ],
        'major_gaps': [],
        'minor_gaps': [],
        'by_category': {
            'A.5': {'name': 'Organisationnels', 'critical': 1, 'major': 0, 'minor': 0}
        }
    }

    content = engine.render_gap_analysis(gaps)
    assert 'Analyse des écarts' in content
    assert 'A.5.1' in content


def test_render_soa(engine):
    """Test le rendu de la SOA"""
    soa_data = {
        'generated_at': '2024-01-01',
        'total_controls': 114,
        'applicable_controls': 100,
        'implemented_controls': 80,
        'controls': [
            {
                'id': 'A.5.1',
                'name': 'Test',
                'category': 'A.5',
                'applicable': True,
                'status': 'implemented',
                'justification': 'Test justification'
            }
        ]
    }

    content = engine.render_soa(soa_data)
    assert 'Déclaration d\'Applicabilité' in content
    assert 'A.5.1' in content


def test_date_filter(engine):
    """Test le filtre de date personnalisé"""
    from datetime import datetime

    # Test avec datetime
    dt = datetime(2024, 1, 15, 10, 30)
    formatted = engine._format_date(dt, '%d/%m/%Y')
    assert formatted == '15/01/2024'

    # Test avec string ISO
    formatted = engine._format_date('2024-01-15', '%d/%m/%Y')
    assert '2024' in formatted
