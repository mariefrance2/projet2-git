# dashboard_logic.py

from datetime import datetime
from typing import List, Dict, Any

def filter_records_by_current_month(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filtre les enregistrements (revenus ou dépenses) pour le mois et l'année en cours.
    Nécessite que chaque enregistrement ait une clé 'date' au format 'YYYY-MM-DD'.
    """
    if not records:
        return []
        
    now = datetime.now()
    current_month_year = now.strftime("%Y-%m")
    
    filtered_records = []
    for record in records:
        try:
            # Conversion de la chaîne de date en objet datetime
            record_date = datetime.strptime(record["date"], "%Y-%m-%d")
            # Comparaison Année-Mois
            if record_date.strftime("%Y-%m") == current_month_year:
                filtered_records.append(record)
        except (KeyError, ValueError):
            # Ignorer les enregistrements sans date ou avec une date mal formatée
            continue
            
    return filtered_records

def calculer_revenu_total_mois(income_records: List[Dict[str, Any]]) -> float:
    """Calcule le revenu total pour le mois en cours."""
    monthly_income = filter_records_by_current_month(income_records)
    return sum(record["amount"] for record in monthly_income)

def calculer_depenses_totales_mois(expense_records: List[Dict[str, Any]]) -> float:
    """Calcule les dépenses totales pour le mois en cours."""
    # Note : Le format de 'expense_records' doit être similaire à 'income_records'
    monthly_expenses = filter_records_by_current_month(expense_records)
    return sum(record["amount"] for record in monthly_expenses)

def calculer_restant(revenus: float, depenses: float) -> float:
    """Calcule l'épargne nette (Restant) pour le mois."""
    return revenus - depenses

def calculer_taux_epargne(revenus: float, restant: float) -> float:
    """Calcule le taux d'épargne en pourcentage pour le mois."""
    if revenus == 0:
        return 0.0
    # Retourne un pourcentage arrondi à une décimale
    return round((restant / revenus) * 100, 1)