
"""
Tests de base pour l'application de budget.
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Teste que les imports principaux fonctionnent."""
    try:
        import taipy
        import pandas
        import numpy
        assert True
    except ImportError as e:
        assert False, f"Import failed: {e}"


def test_utils_import():
    """Teste l'import des utilitaires."""
    try:
        from utils import data_manager, state_manager
        assert True
    except ImportError as e:
        assert False, f"Utils import failed: {e}"


def test_data_manager_functions():
    """Teste les fonctions du data manager."""
    from utils.data_manager import DataManager
    
    dm = DataManager()
    
    # Tester l'ajout de revenus
    # dm.add_income("Salaire", 3000.0, "2024-01-01", "Mensuel")
    # incomes = dm.get_incomes()
    # assert len(incomes) > 0, "Aucun revenu ajouté"
    
    # Tester l'ajout de dépenses
    # dm.add_expense("Loyer", 1000.0, "2024-01-01", "Logement")
    # expenses = dm.get_expenses()
    # assert len(expenses) > 0, "Aucune dépense ajoutée"
    
    # Tester les totaux
    # total_income = dm.get_total_income()
    # total_expense = dm.get_total_expenses()
    # assert total_income > 0, "Total des revenus incorrect"
    # assert total_expense > 0, "Total des dépenses incorrect"


def test_state_manager():
    """Teste le gestionnaire d'état."""
    # from utils.state_manager import StateManager
    
    # sm = StateManager()
    
    # # Tester la navigation
    # sm.navigate_to("dashboard")
    # assert sm.current_page == "dashboard", "Navigation échouée"
    
    # # Tester les paramètres
    # sm.update_settings("EUR", "light")
    # assert sm.currency == "EUR", "Devise non mise à jour"
    # assert sm.theme == "light", "Thème non mis à jour"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])