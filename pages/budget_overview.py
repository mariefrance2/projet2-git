"""
Page Vue d'Ensemble du Budget - Afficher l'état général du budget
"""
from taipy.gui import Markdown
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from utils.data_manager import DataManager

data_manager = DataManager()

# --- LOGIQUE DE FILTRAGE PAR MOIS ---

def filter_records_by_current_month(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filtre les enregistrements pour le mois et l'année en cours."""
    if not records:
        return []
        
    now = datetime.now()
    current_month_year = now.strftime("%Y-%m")
    
    filtered_records = []
    for record in records:
        try:
            record_date = datetime.strptime(record["date"], "%Y-%m-%d")
            if record_date.strftime("%Y-%m") == current_month_year:
                filtered_records.append(record)
        except (KeyError, ValueError):
            continue
            
    return filtered_records

# --- FONCTIONS DE CALCUL MISES À JOUR (AVEC FILTRE) ---

def calculate_budget_summary(state) -> Dict[str, float]:
    """Calculer le résumé du budget à partir des données réelles du mois en cours"""
    # Charger et filtrer les revenus
    income_data = data_manager.load_data("income") or []
    monthly_income_data = filter_records_by_current_month(income_data)
    total_income = sum(item.get("amount", 0) for item in monthly_income_data)
    
    # Charger et filtrer les dépenses
    expenses_data = data_manager.load_data("expenses") or []
    monthly_expenses_data = filter_records_by_current_month(expenses_data)
    total_expenses = sum(item.get("amount", 0) for item in monthly_expenses_data)
    
    # Calculer le restant et le taux d'épargne
    remaining = total_income - total_expenses
    savings_rate = (remaining / total_income * 100) if total_income > 0 else 0
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "remaining": remaining,
        "savings_rate": savings_rate
    }

def calculate_category_expenses(state) -> Dict[str, List[Any]]:
    """Calculer les dépenses par catégorie pour le mois en cours"""
    expenses_data = data_manager.load_data("expenses") or []
    monthly_expenses_data = filter_records_by_current_month(expenses_data)
    
    # Grouper par catégorie
    category_totals: Dict[str, float] = {}
    for expense in monthly_expenses_data:
        category = expense.get("category", "Autre")
        amount = expense.get("amount", 0)
        category_totals[category] = category_totals.get(category, 0) + amount
    
    if not category_totals:
        return {
            "Catégorie": ["Aucune dépense"],
            "Montant": [0]
        }
    
    return {
        "Catégorie": list(category_totals.keys()),
        "Montant": list(category_totals.values())
    }

# --- VARIABLES ET INITIALISATION ---

budget_data: Dict[str, float] = {
    "total_income": 0.0,
    "total_expenses": 0.0,
    "remaining": 0.0,
    "savings_rate": 0.0
}

category_chart_data: Dict[str, List[Any]] = {
    "Catégorie": ["Aucune donnée"],
    "Montant": [0]
}

budget_categories: List[Dict[str, Any]] = []
new_category_name: str = ""
new_category_limit: float = 0.0
selected_category_index: int = -1
currency_symbol: str = "€" # Symbole par défaut

def load_budget_categories(state) -> None:
    """Charger les catégories de budget"""
    loaded_categories = data_manager.load_data("budget_categories")
    if loaded_categories:
        state.budget_categories = loaded_categories
    else:
        # Catégories par défaut
        state.budget_categories = [
            {"name": "Logement", "limit": 1500.0, "spent": 0.0},
            {"name": "Alimentation", "limit": 600.0, "spent": 0.0},
            {"name": "Transport", "limit": 400.0, "spent": 0.0},
            {"name": "Divertissement", "limit": 300.0, "spent": 0.0},
            {"name": "Services", "limit": 500.0, "spent": 0.0}
        ]

def add_category(state) -> None:
    """Ajouter une nouvelle catégorie de budget"""
    if state.new_category_name and state.new_category_limit > 0:
        state.budget_categories.append({
            "name": state.new_category_name,
            "limit": state.new_category_limit,
            "spent": 0.0
        })
        data_manager.save_data("budget_categories", state.budget_categories)
        state.new_category_name = ""
        state.new_category_limit = 0.0
        update_page_data(state)

def delete_category(state, index: int) -> None:
    """Supprimer une catégorie de budget"""
    if 0 <= index < len(state.budget_categories):
        state.budget_categories.pop(index)
        data_manager.save_data("budget_categories", state.budget_categories)
        update_page_data(state)

def update_page_data(state) -> None:
    """Mettre à jour toutes les données de la page"""
    state.budget_data = calculate_budget_summary(state) 
    state.category_chart_data = calculate_category_expenses(state)
    
    expenses_data = data_manager.load_data("expenses") or []
    monthly_expenses_data = filter_records_by_current_month(expenses_data)
    
    for category in state.budget_categories:
        spent = sum(
            expense.get("amount", 0) 
            for expense in monthly_expenses_data
            if expense.get("category") == category["name"]
        )
        category["spent"] = spent
    
    # Obtenir le symbole de devise
    settings = data_manager.load_data("settings") or {}
    state.currency_symbol = settings.get("currency", "€")


def on_init(state) -> None:
    """Initialiser la page avec les données"""
    load_budget_categories(state)
    update_page_data(state)

# --- TAIPY MARKDOWN (CORRIGÉ) ---

page = Markdown("""
<|container|
# 📈 Vue d'Ensemble du Budget

<|layout|columns=1fr auto|gap=1rem|
<|part|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
|>
<|part|
<|button|label=📊 Tableau de Bord|on_action=go_to_dashboard|class_name=nav-button|>
|>
|>

## Résumé Financier

<|layout|columns=1 1 1 1|gap=1rem|
<|card|
### Revenu Total
<|{budget_data['total_income']}|text|format=%.2f {currency_symbol}|class_name=amount-text|>
|>

<|card|
### Dépenses Totales
<|{budget_data['total_expenses']}|text|format=%.2f {currency_symbol}|class_name=amount-text|>
|>

<|card|
### Restant
<|{budget_data['remaining']}|text|format=%.2f {currency_symbol}|class_name=amount-text positive|>
|>

<|card|
### Taux d'Épargne
<|{budget_data['savings_rate']}|text|format=%.1f %%|class_name=amount-text|>
|>
|>

## Répartition des Dépenses

<|{category_chart_data}|chart|type=pie|title=Dépenses par Catégorie|>

## Catégories de Budget

### Ajouter une Catégorie

<|layout|columns=2fr 1fr auto|gap=1rem|
<|{new_category_name}|input|label=Nom de la catégorie|>
<|{new_category_limit}|number|label=Limite (en {currency_symbol})|>
<|button|label=➕ Ajouter|on_action=add_category|class_name=add-button|>
|>

### Mes Catégories

<|{budget_categories}|table|columns=name;limit;spent|column[name].label=Catégorie|column[limit].label=Limite ({currency_symbol})|column[spent].label=Dépensé ({currency_symbol})|>

<|button|label=🔄 Actualiser|on_action=update_page_data|class_name=refresh-button|>

|>

<style>
.nav-button {
    margin-bottom: 1rem;
    background-color: #3b82f6;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
}
.amount-text {
    font-size: 1.5rem;
    color: #2563eb;
    font-weight: bold;
}
.positive {
    color: #10B981;
}
.add-button {
    background-color: #10B981;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
}
.refresh-button {
    background-color: #3b82f6;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    margin-top: 1rem;
}
</style>
""")

def go_home(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="/")

def go_to_dashboard(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="dashboard")