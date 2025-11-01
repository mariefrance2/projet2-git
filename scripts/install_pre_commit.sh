bash
#!/bin/bash

echo "🔧 Installation des pre-commit hooks"
echo "====================================="
echo ""

# Vérifier si Python est installé
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python n'est pas installé."
    exit 1
fi

# Utiliser python3 si disponible, sinon python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "✅ Python trouvé: $PYTHON_CMD"
echo ""

# Installer pre-commit
echo "📦 Installation de pre-commit..."
$PYTHON_CMD -m pip install pre-commit

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation de pre-commit"
    exit 1
fi

echo "✅ pre-commit installé"
echo ""

# Installer les hooks
echo "🔗 Installation des hooks Git..."
pre-commit install

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation des hooks"
    exit 1
fi

echo "✅ Hooks installés"
echo ""

# Exécuter les hooks sur tous les fichiers
echo "🧪 Test des hooks sur tous les fichiers..."
echo "(Cela peut prendre quelques minutes la première fois)"
echo ""

pre-commit run --all-files

echo ""
echo "🎉 Installation terminée!"
echo ""
echo "📝 Les hooks s'exécuteront automatiquement avant chaque commit."
echo ""
echo "💡 Commandes utiles:"
echo "  - Exécuter manuellement: pre-commit run --all-files"
echo "  - Mettre à jour les hooks: pre-commit autoupdate"
echo "  - Désinstaller: pre-commit uninstall"
echo ""