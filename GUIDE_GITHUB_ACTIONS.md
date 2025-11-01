markdown
# Guide Complet: GitHub Actions avec IA

## Table des Matières
1. Créer le Repository GitHub
2. Configurer les Secrets
3. Pousser le Code
4. Configurer les Profils d'Équipe
5. Installer Pre-commit Localement
6. Configurer git-secret
7. Protéger la Branche Main
8. Tester le Workflow

## 1. Créer le Repository GitHub

```bash
# Sur GitHub.com, créez un nouveau repository
# Puis localement:
cd python-budget-app
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/python-budget-app.git
git push -u origin main
```

## 2. Configurer les Secrets

GitHub → Settings → Secrets and variables → Actions → New repository secret

Ajoutez:
- `OPENAI_API_KEY`: Votre clé OpenAI
- `EMAIL_USERNAME`: Votre Gmail
- `EMAIL_PASSWORD`: Mot de passe d'application Gmail
- `TEAM_EMAIL`: Email de notification

## 3-8. Voir le fichier complet pour les détails...
```

---

## 📋 Résumé des Chemins

Voici tous les chemins à créer dans VS Code:

```
.github/workflows/code-quality.yml
.github/scripts/ai_code_review.py
.github/scripts/check_results.py
.github/team_profiles.json
.pre-commit-config.yaml
pyproject.toml
requirements.txt
.gitignore
scripts/setup_git_secret.sh
scripts/install_pre_commit.sh
tests/test_basic.py
README.md
GUIDE_GITHUB_ACTIONS.md