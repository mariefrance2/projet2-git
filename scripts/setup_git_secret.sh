bash
#!/bin/bash

echo "🔐 Configuration de git-secret"
echo "================================"

# Vérifier si git-secret est installé
if ! command -v git-secret &> /dev/null; then
    echo "❌ git-secret n'est pas installé."
    echo ""
    echo "Installation:"
    echo "  macOS: brew install git-secret"
    echo "  Linux: sudo apt-get install git-secret"
    echo "  Windows: Utilisez WSL ou Git Bash"
    exit 1
fi

# Vérifier si GPG est installé
if ! command -v gpg &> /dev/null; then
    echo "❌ GPG n'est pas installé."
    echo ""
    echo "Installation:"
    echo "  macOS: brew install gnupg"
    echo "  Linux: sudo apt-get install gnupg"
    exit 1
fi

echo "✅ git-secret et GPG sont installés"
echo ""

# Initialiser git-secret
if [ ! -d ".gitsecret" ]; then
    echo "📦 Initialisation de git-secret..."
    git secret init
    echo "✅ git-secret initialisé"
else
    echo "✅ git-secret déjà initialisé"
fi

echo ""
echo "📧 Configuration de votre clé GPG"
echo ""

# Lister les clés GPG
echo "Vos clés GPG existantes:"
gpg --list-keys

echo ""
read -p "Entrez votre email GPG (ou appuyez sur Entrée pour en créer une nouvelle): " gpg_email

if [ -z "$gpg_email" ]; then
    echo ""
    echo "🔑 Création d'une nouvelle clé GPG..."
    echo "Suivez les instructions à l'écran."
    gpg --full-generate-key
    
    echo ""
    echo "Vos clés GPG:"
    gpg --list-keys
    
    read -p "Entrez l'email de la clé que vous venez de créer: " gpg_email
fi

# Ajouter l'utilisateur à git-secret
echo ""
echo "➕ Ajout de votre clé à git-secret..."
git secret tell "$gpg_email"

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "📝 Prochaines étapes:"
echo "  1. Créez un fichier .env avec vos secrets:"
echo "     echo 'OPENAI_API_KEY=sk-...' > .env"
echo ""
echo "  2. Ajoutez-le à git-secret:"
echo "     git secret add .env"
echo ""
echo "  3. Chiffrez les fichiers:"
echo "     git secret hide"
echo ""
echo "  4. Commitez les fichiers chiffrés:"
echo "     git add .env.secret .gitsecret"
echo "     git commit -m 'Add encrypted secrets'"
echo ""
echo "  5. Pour déchiffrer (membres autorisés):"
echo "     git secret reveal"
echo ""
echo "🎉 Terminé!"