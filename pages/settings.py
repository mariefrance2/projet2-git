"""
Page Paramètres - Configurer les préférences de l'application
"""
from taipy.gui import Markdown, notify
from typing import List

currency: str = "FCFA"
currencies: List[str] = ["EUR", "USD", "GBP", "CAD", "CHF", "FCFA"]
theme: str = "Clair"
themes: List[str] = ["Clair", "Sombre"]
notifications: bool = True
email_reports: bool = False
user_email: str = "utilisateur@exemple.com"

currency_symbols = {
    "EUR": "€",
    "USD": "$",
    "GBP": "£",
    "CAD": "CA$",
    "CHF": "CHF",
    "FCFA": "FCFA"
}

page = Markdown("""
<|container|
# ⚙️ Paramètres

<|layout|columns=1fr auto|gap=1rem|
<|part|
<|button|label=🏠 Accueil|on_action=go_home|class_name=nav-button|>
|>
<|part|
<|button|label=📊 Tableau de Bord|on_action=go_to_dashboard|class_name=nav-button|>
|>
|>

## Paramètres Généraux

<|layout|columns=1 1|gap=2rem|
<|part|
### Devise
<|{currency}|selector|lov={currencies}|>

### Thème
<|{theme}|selector|lov={themes}|>
|>

<|part|
### Notifications
<|{notifications}|toggle|label=Activer les notifications|>

### Rapports par Email
<|{email_reports}|toggle|label=Recevoir des rapports mensuels par email|>
|>
|>

## Paramètres du Compte

**Adresse Email**
<|{user_email}|input|>

<|{None}|button|label=💾 Enregistrer les Paramètres|on_action=save_settings|class_name=save-button|>

## Gestion des Données

<|layout|columns=1 1|gap=1rem|
<|part|
<|{None}|button|label=📤 Exporter les Données|on_action=export_data|class_name=data-button|>
|>
<|part|
<|{None}|button|label=📥 Importer les Données|on_action=import_data|class_name=data-button|>
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
.save-button {
    margin: 1rem 0;
    background-color: #10B981;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-size: 1.1rem;
}
.data-button {
    background-color: #6366f1;
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

def save_settings(state) -> None:
    """Enregistrer les paramètres utilisateur"""
    from utils.data_manager import DataManager
    from utils.state_manager import AppState
    
    settings_data = {
        "currency": state.currency,
        "theme": state.theme,
        "notifications": state.notifications,
        "email_reports": state.email_reports,
        "user_email": state.user_email
    }
    
    data_manager = DataManager()
    success = data_manager.save_data("settings", settings_data)
    
    if success:
        from main import app_state
        app_state.currency = state.currency
        app_state.theme = state.theme
        
        notify(state, "success", "✅ Paramètres enregistrés avec succès!")
    else:
        notify(state, "error", "❌ Erreur lors de l'enregistrement des paramètres")

def export_data(state) -> None:
    """Exporter les données utilisateur"""
    from utils.data_manager import DataManager
    import json
    
    data_manager = DataManager()
    all_data = data_manager.export_all_data()
    
    export_success = data_manager.save_data("export_backup", all_data)
    
    if export_success:
        notify(state, "success", "✅ Données exportées avec succès dans data/export_backup.json")
    else:
        notify(state, "error", "❌ Erreur lors de l'export des données")

def import_data(state) -> None:
    """Importer les données utilisateur"""
    notify(state, "info", "ℹ️ Fonctionnalité d'import en cours de développement")
