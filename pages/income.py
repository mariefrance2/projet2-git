"""
Page Revenus - Gérer les sources de revenus
"""
from taipy.gui import Markdown
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd

income_records: List[Dict[str, Any]] = []

new_source: str = ""
new_amount: float = 0.0
new_date: str = datetime.now().strftime("%Y-%m-%d")
new_recurring: bool = False

def get_income_df(records):
    """Convert income records to DataFrame"""
    if not records:
        return pd.DataFrame(columns=["ID", "Source", "Montant", "Date", "Récurrent"])
    return pd.DataFrame([
        {
            "ID": r["id"],
            "Source": r["source"],
            "Montant": f"{r['amount']:.2f}",
            "Date": r["date"],
            "Récurrent": "Oui" if r["recurring"] else "Non"
        }
        for r in records
    ])

income_df = get_income_df(income_records)

page = Markdown("""
<|container|
# 💵 Gestion des Revenus

<|layout|columns=1fr auto|gap=1rem|
<|part|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
|>
<|part|
<|button|label=📊 Tableau de Bord|on_action=go_to_dashboard|class_name=nav-button|>
|>
|>

## Ajouter un Nouveau Revenu

<|layout|columns=1 1 1 1|gap=1rem|
<|part|
**Source**
<|{new_source}|input|>
|>
<|part|
**Montant**
<|{new_amount}|number|>
|>
<|part|
**Date**
<|{new_date}|date|>
|>
<|part|
**Récurrent**
<|{new_recurring}|toggle|>
|>
|>

<|{None}|button|label=Ajouter un Revenu|on_action=add_income|class_name=add-button|>

## Enregistrements de Revenus

<|{income_df}|table|>

## Revenu Total Ce Mois
## {sum(record['amount'] for record in income_records):.2f}

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
    background-color: #10B981;
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

def add_income(state) -> None:
    """Ajouter un nouvel enregistrement de revenu"""
    from utils.data_manager import DataManager
    
    if state.new_source and state.new_amount > 0:
        new_record: Dict[str, Any] = {
            "id": len(state.income_records) + 1,
            "source": state.new_source,
            "amount": state.new_amount,
            "date": state.new_date,
            "recurring": state.new_recurring
        }
        state.income_records.append(new_record)
        
        data_manager = DataManager()
        data_manager.save_data("income", state.income_records)
        
        state.income_df = get_income_df(state.income_records)
        
        # Réinitialiser le formulaire
        state.new_source = ""
        state.new_amount = 0.0
        state.new_recurring = False
