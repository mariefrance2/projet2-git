"""
Page Dépenses - Suivre et catégoriser les dépenses
"""
from taipy.gui import Markdown
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd

expense_records: List[Dict[str, Any]] = []

categories: List[str] = ["Logement", "Alimentation", "Transport", "Divertissement", "Services", "Santé", "Autre"]
new_category: str = categories[0]
new_description: str = ""
new_amount: float = 0.0
new_date: str = datetime.now().strftime("%Y-%m-%d")

def get_expenses_df(records):
    """Convert expense records to DataFrame"""
    if not records:
        return pd.DataFrame(columns=["ID", "Catégorie", "Description", "Montant", "Date"])
    return pd.DataFrame([
        {
            "ID": r["id"],
            "Catégorie": r["category"],
            "Description": r["description"],
            "Montant": f"{r['amount']:.2f}",
            "Date": r["date"]
        }
        for r in records
    ])

expenses_df = get_expenses_df(expense_records)

page = Markdown("""
<|container|
# 💳 Suivi des Dépenses

<|layout|columns=1fr auto|gap=1rem|
<|part|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
|>
<|part|
<|button|label=📊 Tableau de Bord|on_action=go_to_dashboard|class_name=nav-button|>
|>
|>

## Ajouter une Nouvelle Dépense

<|layout|columns=1 1 1 1|gap=1rem|
<|part|
**Catégorie**
<|{new_category}|selector|lov={categories}|>
|>
<|part|
**Description**
<|{new_description}|input|>
|>
<|part|
**Montant**
<|{new_amount}|number|>
|>
<|part|
**Date**
<|{new_date}|date|>
|>
|>

<|{None}|button|label=Ajouter une Dépense|on_action=add_expense|class_name=add-button|>

## Enregistrements de Dépenses

<|{expenses_df}|table|>

## Dépenses Totales Ce Mois
### {sum(record['amount'] for record in expense_records):.2f}

|>

<style>
.nav-button {
    margin-bottom: 1rem;
    background-color: #3b82f6;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
}
.add-button {
    margin: 1rem 0;
    background-color: #EF4444;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
}
</style>
""")

def go_home(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="/")

def go_to_dashboard(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="dashboard")

def add_expense(state) -> None:
    """Ajouter un nouvel enregistrement de dépense"""
    from utils.data_manager import DataManager
    
    if state.new_description and state.new_amount > 0:
        new_record: Dict[str, Any] = {
            "id": len(state.expense_records) + 1,
            "category": state.new_category,
            "description": state.new_description,
            "amount": state.new_amount,
            "date": state.new_date
        }
        state.expense_records.append(new_record)
        
        data_manager = DataManager()
        data_manager.save_data("expenses", state.expense_records)
        
        state.expenses_df = get_expenses_df(state.expense_records)
        
        # Réinitialiser le formulaire
        state.new_description = ""
        state.new_amount = 0.0
