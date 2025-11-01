"""
Page Objectifs d'Épargne - Définir et suivre les objectifs d'épargne
"""
from taipy.gui import Markdown
from typing import List, Dict, Any
import pandas as pd

savings_goals: List[Dict[str, Any]] = []

new_goal: str = ""
new_target: float = 0.0
new_current: float = 0.0

def get_savings_df(records):
    """Convert savings goals to DataFrame"""
    if not records:
        return pd.DataFrame(columns=["ID", "Objectif", "Cible", "Actuel", "Progrès (%)"])
    return pd.DataFrame([
        {
            "ID": r["id"],
            "Objectif": r["goal"],
            "Cible": f"{r['target']:.2f}",
            "Actuel": f"{r['current']:.2f}",
            "Progrès (%)": f"{r['progress']:.1f}%"
        }
        for r in records
    ])

savings_df = get_savings_df(savings_goals)

page = Markdown("""
<|container|
# 🎯 Objectifs d'Épargne

<|layout|columns=1fr auto|gap=1rem|
<|part|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
|>
<|part|
<|button|label=📊 Tableau de Bord|on_action=go_to_dashboard|class_name=nav-button|>
|>
|>

## Ajouter un Nouvel Objectif

<|layout|columns=1 1 1|gap=1rem|
<|part|
**Nom de l'Objectif**
<|{new_goal}|input|>
|>
<|part|
**Montant Cible**
<|{new_target}|number|>
|>
<|part|
**Montant Actuel**
<|{new_current}|number|>
|>
|>

<|{None}|button|label=Ajouter un Objectif|on_action=add_goal|class_name=add-button|>

## Vos Objectifs d'Épargne

<|{savings_df}|table|>

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
    background-color: #8B5CF6;
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

def add_goal(state) -> None:
    """Ajouter un nouvel objectif d'épargne"""
    from utils.data_manager import DataManager
    
    if state.new_goal and state.new_target > 0:
        progress: float = (state.new_current / state.new_target * 100) if state.new_target > 0 else 0.0
        new_record: Dict[str, Any] = {
            "id": len(state.savings_goals) + 1,
            "goal": state.new_goal,
            "target": state.new_target,
            "current": state.new_current,
            "progress": progress
        }
        state.savings_goals.append(new_record)
        
        data_manager = DataManager()
        data_manager.save_data("savings_goals", state.savings_goals)
        
        state.savings_df = get_savings_df(state.savings_goals)
        
        # Réinitialiser le formulaire
        state.new_goal = ""
        state.new_target = 0.0
        state.new_current = 0.0
