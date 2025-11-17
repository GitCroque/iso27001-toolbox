"""Configuration globale pour pytest"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))
