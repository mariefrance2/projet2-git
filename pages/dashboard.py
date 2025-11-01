"""
Page Tableau de Bord - Hub de navigation principal
"""
from taipy.gui import Markdown

page = Markdown("""
<|container|
# 📊 Tableau de Bord

<|layout|columns=1fr auto|gap=1rem|
<|part|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
|>
<|part|
|>
|>

## Accès Rapide

<|layout|columns=1 1 1|gap=1.5rem|
<|card|
### 📈 Vue d'Ensemble du Budget
Consultez l'état général de votre budget
<|{None}|button|label=Voir le Budget|on_action=go_to_budget|class_name=card-button|>
|>

<|card|
### 💵 Revenus
Gérez vos sources de revenus
<|{None}|button|label=Gérer les Revenus|on_action=go_to_income|class_name=card-button|>
|>

<|card|
### 💳 Dépenses
Suivez vos dépenses
<|{None}|button|label=Suivre les Dépenses|on_action=go_to_expenses|class_name=card-button|>
|>
|>

<|layout|columns=1 1 1|gap=1.5rem|
<|card|
### 🎯 Objectifs d'Épargne
Définissez et suivez vos objectifs d'épargne
<|{None}|button|label=Voir les Objectifs|on_action=go_to_savings|class_name=card-button|>
|>

<|card|
### 📊 Rapports
Consultez les rapports financiers
<|{None}|button|label=Voir les Rapports|on_action=go_to_reports|class_name=card-button|>
|>

<|card|
### ⚙️ Paramètres
Configurez vos préférences
<|{None}|button|label=Paramètres|on_action=go_to_settings|class_name=card-button|>
|>
|>

|>

<style>
.nav-button {
    margin-bottom: 1rem;
    background-color: #3b82f6;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
}
.card-button {
    margin-top: 1rem;
    background-color: #2563eb;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
}
</style>
""")

def go_home(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="/")

def go_to_budget(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="budget")

def go_to_income(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="income")

def go_to_expenses(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="expenses")

def go_to_savings(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="savings")

def go_to_reports(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="reports")

def go_to_settings(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="settings")
