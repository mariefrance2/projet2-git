"""
Application de Tableau de Bord de Budget Personnel
Point d'entrée principal pour l'application Taipy
"""
from typing import Optional
import taipy as tp
from taipy.gui import Gui, navigate, State
# AJOUTER 'table' ICI
from pages import home, dashboard, budget_overview, income, expenses, savings, reports, settings, table 
from utils.state_manager import AppState
from utils.data_manager import DataManager

app_state = AppState()
data_manager = DataManager()

def load_initial_data():
    """Load all saved data from files"""
    saved_income = data_manager.load_data("income")
    saved_expenses = data_manager.load_data("expenses")
    saved_goals = data_manager.load_data("savings_goals")
    saved_settings = data_manager.load_data("settings")[0] if data_manager.load_data("settings") else {}
    
    if saved_income:
        income.income_records = saved_income
    if saved_expenses:
        expenses.expense_records = saved_expenses
    if saved_goals:
        savings.savings_goals = saved_goals
    if saved_settings:
        settings.currency = saved_settings.get("currency", "EUR")
        settings.theme = saved_settings.get("theme", "Clair")
        settings.notifications = saved_settings.get("notifications", True)
        settings.email_reports = saved_settings.get("email_reports", False)
        settings.user_email = saved_settings.get("user_email", "utilisateur@exemple.com")
        app_state.currency = settings.currency
        app_state.theme = settings.theme

pages = {
    "/": home.page,
    "dashboard": dashboard.page,
    "budget": budget_overview.page,
    "income": income.page,
    "expenses": expenses.page,
    "savings": savings.page,
    "reports": reports.page,
    "settings": settings.page,
    "transactions": table.page, # <-- NOUVELLE PAGE
}

def on_navigate(state: State, page_name: str) -> None:
    """Gérer la navigation entre les pages"""
    navigate(state, to=page_name)

if __name__ == "__main__":
    load_initial_data()
    
    gui = Gui(pages=pages)
    gui.run(
        title="Tableau de Bord Budget Personnel",
        port=5000,
        dark_mode=(app_state.theme == "Sombre"),
        use_reloader=True
    )