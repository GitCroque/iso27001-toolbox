# Guide de contribution

Merci de votre intérêt pour contribuer à ISO 27001 Toolkit ! 🎉

## Comment contribuer

### Signaler des bugs

Si vous trouvez un bug :

1. Vérifiez qu'il n'a pas déjà été signalé dans les [Issues](https://github.com/GitCroque/iso27001-toolbox/issues)
2. Ouvrez une nouvelle issue avec :
   - Un titre clair et descriptif
   - Les étapes pour reproduire le problème
   - Le comportement attendu vs le comportement observé
   - Votre environnement (OS, version Python, etc.)

### Proposer des améliorations

Pour proposer une nouvelle fonctionnalité :

1. Ouvrez une issue pour discuter de votre idée
2. Attendez les retours de la communauté
3. Si approuvé, vous pouvez commencer à travailler dessus

### Soumettre des changements

1. **Forkez** le repository
2. **Créez une branche** depuis `main` :
   ```bash
   git checkout -b feature/ma-super-fonctionnalite
   ```
3. **Faites vos changements** en suivant les conventions du projet
4. **Testez** vos changements
5. **Committez** avec des messages clairs :
   ```bash
   git commit -m "feat: ajoute la génération de rapport PDF"
   ```
6. **Pushez** vers votre fork :
   ```bash
   git push origin feature/ma-super-fonctionnalite
   ```
7. **Ouvrez une Pull Request**

## Standards de code

### Style Python

- Suivez [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Utilisez `black` pour le formatage :
  ```bash
  black src/
  ```
- Utilisez `flake8` pour le linting :
  ```bash
  flake8 src/
  ```

### Documentation

- Documentez toutes les fonctions publiques
- Utilisez des docstrings au format Google :
  ```python
  def ma_fonction(param1: str, param2: int) -> bool:
      """
      Description courte de la fonction.

      Args:
          param1: Description du paramètre 1
          param2: Description du paramètre 2

      Returns:
          Description de la valeur de retour

      Raises:
          ValueError: Quand param2 est négatif
      """
      pass
  ```

### Messages de commit

Utilisez les préfixes suivants :

- `feat:` - Nouvelle fonctionnalité
- `fix:` - Correction de bug
- `docs:` - Documentation seulement
- `style:` - Changements de style (formatage, etc.)
- `refactor:` - Refactoring de code
- `test:` - Ajout ou modification de tests
- `chore:` - Maintenance (dépendances, etc.)

Exemples :
```
feat: ajoute la commande export en PDF
fix: corrige le calcul du score de risque
docs: améliore le README avec plus d'exemples
```

## Domaines de contribution

### Templates

Vous pouvez contribuer en ajoutant de nouveaux templates :

1. Créez le fichier dans `src/iso27001_toolkit/templates/policies/`
2. Utilisez les variables Jinja2 standards
3. Documentez les variables spécifiques si nécessaire
4. Ajoutez la politique à la liste dans `policies.py`

### Traductions

Pour ajouter une nouvelle langue :

1. Créez un dossier `templates_<langue>/`
2. Traduisez les templates
3. Mettez à jour la documentation

### Tests

Tous les nouveaux codes devraient inclure des tests :

```python
# tests/test_controls.py
import pytest
from iso27001_toolkit.utils.controls_tracker import ControlsTracker

def test_control_status_update():
    tracker = ControlsTracker()
    tracker.update_control_status('A.5.1', 'implemented')
    assert tracker.get_control_status('A.5.1') == 'implemented'
```

Exécutez les tests :
```bash
pytest tests/
```

## Questions ?

N'hésitez pas à :
- Ouvrir une [Discussion](https://github.com/GitCroque/iso27001-toolbox/discussions)
- Poser des questions dans les issues
- Contacter les mainteneurs

## Code de conduite

- Soyez respectueux et inclusif
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est le mieux pour la communauté

Merci de contribuer à rendre la conformité ISO 27001 plus accessible ! 🙏
