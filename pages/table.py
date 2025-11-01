from taipy.gui import Markdown
from typing import List, Dict, Any
from utils.data_manager import DataManager
from datetime import datetime

# Instancier le DataManager (doit être fait une seule fois)
data_manager = DataManager()

# --- VARIABLES ET INITIALISATION ---
# La liste qui contiendra toutes les transactions fusionnées et filtrées
transactions_data: List[Dict[str, Any]] = []

# Synchronisation avec l'autre page (à simplifier avec l'état global plus tard)
available_months: List[str] = ["2025-11", "2025-10", "2025-09"] # Placeholder, sera mis à jour
selected_month_year: str = datetime.now().strftime("%Y-%m")
currency_symbol: str = "€" 

# --- FONCTIONS DE LOGIQUE ---

def filter_records_by_current_month(records: List[Dict[str, Any]], selected_month: str) -> List[Dict[str, Any]]:
    """Filtre les enregistrements pour le mois et l'année sélectionnés."""
    if not records:
        return []
    
    month_year_prefix = selected_month
    filtered_records = [
        record for record in records
        if record.get("date", "").startswith(month_year_prefix)
    ]
    return filtered_records

def load_and_filter_transactions(state) -> None:
    """Charge, fusionne et filtre toutes les transactions (revenus et dépenses)."""
    
    income_data = data_manager.load_data("income") or []
    expenses_data = data_manager.load_data("expenses") or []
    
    # 1. Marquer les types de transaction pour l'affichage
    for item in income_data:
        item['type'] = 'Revenu'
        item['class_name'] = 'positive-row' # Pour le style de la ligne
        
    for item in expenses_data:
        item['type'] = 'Dépense'
        item['class_name'] = 'negative-row' # Pour le style de la ligne
        
    # 2. Fusionner et filtrer
    all_records = income_data + expenses_data
    state.transactions_data = filter_records_by_current_month(all_records, state.selected_month_year)
    
    # Mettre à jour le symbole monétaire
    settings = data_manager.load_data("settings") or {}
    state.currency_symbol = settings.get("currency", "€")


def on_init(state) -> None:
    """Initialiser la page"""
    load_and_filter_transactions(state)

def on_change(state, var_name, value) -> None:
    """Met à jour les données quand le mois sélectionné change."""
    if var_name == "selected_month_year":
        load_and_filter_transactions(state)


# --- TAIPY MARKDOWN (Affichage) ---

page = Markdown("""
<|container|
# 📋 Tableau de Bord des Transactions

<|layout|columns=1fr auto|gap=1rem|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
<|button|label=📈 Vue d'Ensemble|on_action=go_to_budget_overview|class_name=nav-button|>
|>

<br/>

<|layout|columns=1 1|
<|{selected_month_year}|selector|label=Filtrer par Mois|lov={available_months}|dropdown=True|>

<|part|>
|>

## Transactions pour {selected_month_year}

<|{transactions_data}|table|
columns=date;description;amount;category;type|
column[amount].label=Montant ({currency_symbol})|
column[type].label=Type|
column[date].label=Date|
reorderable[data]=True|
height=500px|
row_class_name=class_name
|>

|>

<style>
/* Styles pour mettre en évidence les revenus (vert) et les dépenses (rouge) */
.positive-row {
    background-color: #d1f7e0; 
}
.negative-row {
    background-color: #fcebeb; 
}
</style>
""")

# Fonctions de navigation (à ajouter si elles manquent dans main.py)
def go_home(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="/")

def go_to_budget_overview(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="budget_overview")