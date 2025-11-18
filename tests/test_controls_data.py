"""Tests pour les données des contrôles ISO 27001"""

import pytest
from iso27001_toolkit.utils.controls_data import (
    get_all_controls,
    get_control_by_id,
    get_controls_by_category,
    get_controls_by_type
)


def test_get_all_controls():
    """Test la récupération de tous les contrôles"""
    controls = get_all_controls()
    assert len(controls) == 114  # ISO 27001:2022 a 114 contrôles
    assert all('id' in c for c in controls)
    assert all('name' in c for c in controls)
    assert all('category' in c for c in controls)


def test_get_control_by_id():
    """Test la récupération d'un contrôle par ID"""
    control = get_control_by_id('A.5.1')
    assert control is not None
    assert control['id'] == 'A.5.1'
    assert 'Politiques de sécurité' in control['name']

    # Test avec ID invalide
    control = get_control_by_id('A.99.99')
    assert control is None


def test_get_controls_by_category():
    """Test le filtrage par catégorie"""
    # Catégorie A.5 - Contrôles organisationnels (37 contrôles)
    controls = get_controls_by_category('A.5')
    assert len(controls) == 37
    assert all(c['category'] == 'A.5' for c in controls)

    # Catégorie A.6 - Contrôles relatifs aux personnes (8 contrôles)
    controls = get_controls_by_category('A.6')
    assert len(controls) == 8

    # Catégorie A.7 - Contrôles physiques (14 contrôles)
    controls = get_controls_by_category('A.7')
    assert len(controls) == 14

    # Catégorie A.8 - Contrôles technologiques (34 contrôles)
    controls = get_controls_by_category('A.8')
    assert len(controls) == 34


def test_get_controls_by_type():
    """Test le filtrage par type"""
    org_controls = get_controls_by_type('Organizational')
    assert len(org_controls) == 37

    people_controls = get_controls_by_type('People')
    assert len(people_controls) == 8

    physical_controls = get_controls_by_type('Physical')
    assert len(physical_controls) == 14

    tech_controls = get_controls_by_type('Technological')
    assert len(tech_controls) == 34


def test_control_structure():
    """Test la structure des contrôles"""
    control = get_control_by_id('A.5.1')

    required_fields = [
        'id', 'category', 'category_name', 'name',
        'type', 'description', 'purpose'
    ]

    for field in required_fields:
        assert field in control, f"Field '{field}' missing in control"
        assert control[field], f"Field '{field}' is empty"


def test_all_categories_present():
    """Test que toutes les catégories sont présentes"""
    all_controls = get_all_controls()
    categories = set(c['category'] for c in all_controls)

    expected_categories = {'A.5', 'A.6', 'A.7', 'A.8'}
    assert categories == expected_categories


def test_control_ids_unique():
    """Test que tous les IDs sont uniques"""
    all_controls = get_all_controls()
    ids = [c['id'] for c in all_controls]

    assert len(ids) == len(set(ids)), "Duplicate control IDs found"


def test_control_ids_format():
    """Test le format des IDs de contrôles"""
    all_controls = get_all_controls()

    for control in all_controls:
        control_id = control['id']
        # Format: A.X.Y où X est 5-8 et Y est un nombre
        assert control_id.startswith('A.')
        parts = control_id.split('.')
        assert len(parts) == 3
        assert parts[1] in ['5', '6', '7', '8']
        assert parts[2].isdigit()
