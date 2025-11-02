
"""
Page d'accueil - Page de destination avec navigation vers le tableau de bord
"""
from taipy.gui import Markdown

page = Markdown("""
<|container|
# 💰 Gestionnaire de Budget Personnel

<|text-center|
Bienvenue dans votre système de gestion de budget personnel. Prenez le contrôle de vos finances et atteignez vos objectifs financiers.
|>

<|layout|columns=1 1 1|gap=2rem|
<|card|
### 📊 Suivre les Dépenses
Surveillez vos dépenses quotidiennes et catégorisez vos dépenses
|>

<|card|
### 💵 Gérer les Revenus
Enregistrez toutes vos sources de revenus et suivez vos gains
|>

<|card|
### 🎯 Définir des Objectifs
Créez et suivez vos objectifs d'épargne
|>
|>



<style>
.primary-button {
    margin-top: 2rem;
    padding: 1rem 2rem;
    font-size: 1.2rem;
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    color: white;
    border-radius: 0.75rem;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
    transition: all 0.3s ease;
}
.primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(37, 99, 235, 0.4);
}
</style>
""")

def navigate_to_dashboard(state) -> None:
    """Naviguer vers la page du tableau de bord"""
    from taipy.gui import navigate
    navigate(state, to="dashboard")
