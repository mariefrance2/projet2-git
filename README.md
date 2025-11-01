markdown
# 💰 Application de Gestion de Budget Personnel

Application moderne de gestion de budget personnel développée avec Taipy, Python et IA.

## ✨ Fonctionnalités

- 📊 **Tableau de bord** interactif avec visualisations
- 💵 **Gestion des revenus** avec catégorisation
- 💸 **Suivi des dépenses** par catégorie
- 🎯 **Objectifs d'épargne** avec suivi de progression
- 📈 **Rapports financiers** détaillés
- ⚙️ **Paramètres personnalisables** (devise, thème)
- 💾 **Sauvegarde automatique** des données

## 🌍 Devises Supportées

- EUR (€) - Euro
- USD ($) - Dollar américain
- GBP (£) - Livre sterling
- **FCFA (CFA)** - Franc CFA
- JPY (¥) - Yen japonais
- CAD (C$) - Dollar canadien

## 🚀 Installation

### Prérequis

- Python 3.11 ou supérieur
- pip

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/python-budget-app.git
cd python-budget-app
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python main.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:5000`

## 🔧 Configuration GitHub Actions

Ce projet utilise GitHub Actions pour la vérification automatique du code avec IA.

### Configuration Rapide

1. **Configurer les secrets GitHub**
   - Allez dans Settings → Secrets and variables → Actions
   - Ajoutez ces secrets:
     - `OPENAI_API_KEY`: Votre clé API OpenAI
     - `EMAIL_USERNAME`: Votre email Gmail
     - `EMAIL_PASSWORD`: Mot de passe d'application Gmail
     - `TEAM_EMAIL`: Email de l'équipe pour les notifications

2. **Installer pre-commit localement**
```bash
chmod +x scripts/install_pre_commit.sh
./scripts/install_pre_commit.sh
```

3. **Configurer git-secret (optionnel)**
```bash
chmod +x scripts/setup_git_secret.sh
./scripts/setup_git_secret.sh
```

Pour plus de détails, consultez [GUIDE_GITHUB_ACTIONS.md](GUIDE_GITHUB_ACTIONS.md)

## 📁 Structure du Projet

```
python-budget-app/
├── .github/
│   ├── workflows/
│   │   └── code-quality.yml
│   ├── scripts/
│   │   ├── ai_code_review.py
│   │   └── check_results.py
│   └── team_profiles.json
├── pages/
│   ├── home.py
│   ├── dashboard.py
│   ├── budget_overview.py
│   ├── income.py
│   ├── expenses.py
│   ├── savings.py
│   ├── reports.py
│   └── settings.py
├── utils/
│   ├── data_manager.py
│   └── state_manager.py
├── scripts/
│   ├── setup_git_secret.sh
│   └── install_pre_commit.sh
├── tests/
│   └── test_basic.py
├── data/
│   └── (fichiers JSON générés automatiquement)
├── main.py
├── requirements.txt
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest tests/ -v

# Vérifier le typage
mypy . --ignore-missing-imports

# Vérifier le style
ruff check .

# Formater le code
black .
```

## 🤝 Contribution

1. Créez une branche: `git checkout -b feature/ma-fonctionnalite`
2. Commitez vos changements: `git commit -m 'Add: nouvelle fonctionnalité'`
3. Poussez vers la branche: `git push origin feature/ma-fonctionnalite`
4. Ouvrez une Pull Request

Les pre-commit hooks vérifieront automatiquement votre code avant chaque commit.

## 📧 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

## 📄 Licence

MIT License

## 🎉 Remerciements

- [Taipy](https://www.taipy.io/) pour le framework UI
- [OpenAI](https://openai.com/) pour l'analyse IA du code
- Tous les contributeurs du projet