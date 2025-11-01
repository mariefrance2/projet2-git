"""
Page Rapports - Consulter les rapports financiers et analyses
"""
from taipy.gui import Markdown
from typing import List, Dict, Any

monthly_summary: Dict[str, List[Any]] = {
    "Mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun"],
    "Revenus": [4500, 4800, 5000, 4900, 5200, 5000],
    "Dépenses": [3200, 3400, 3100, 3300, 3500, 3200],
    "Épargne": [1300, 1400, 1900, 1600, 1700, 1800]
}

page = Markdown("""
<|container|
# 📊 Rapports Financiers

<|layout|columns=1fr auto|gap=1rem|
<|part|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
|>
<|part|
<|button|label=📊 Tableau de Bord|on_action=go_to_dashboard|class_name=nav-button|>
|>
|>

## Tendances Mensuelles

<|{monthly_summary}|chart|type=bar|x=Mois|y[1]=Revenus|y[2]=Dépenses|y[3]=Épargne|title=Aperçu Financier sur 6 Mois|>

## Indicateurs Clés

<|layout|columns=1 1 1|gap=1rem|
<|card|
### Revenu Mensuel Moyen
**4 900,00 €**
|>

<|card|
### Dépenses Mensuelles Moyennes
**3 283,33 €**
|>

<|card|
### Épargne Mensuelle Moyenne
**1 616,67 €**
|>
|>

## Répartition des Dépenses

<|layout|columns=1 1|gap=1rem|
<|part|
### Principales Catégories de Dépenses
1. Logement: 1 200,00 € (37,5%)
2. Services: 700,00 € (21,9%)
3. Alimentation: 600,00 € (18,8%)
4. Transport: 400,00 € (12,5%)
5. Divertissement: 300,00 € (9,4%)
|>

<|part|
### Tendance du Taux d'Épargne
Votre taux d'épargne s'est amélioré de **8%** au cours des 6 derniers mois.
Taux actuel: **33%**
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
</style>
""")

def go_home(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="/")

def go_to_dashboard(state) -> None:
    from taipy.gui import navigate
    navigate(state, to="dashboard")
