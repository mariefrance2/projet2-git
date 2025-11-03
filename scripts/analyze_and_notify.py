import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from google.genai.errors import APIError

# --- PARTIE 1 : Récupération des arguments et des secrets d'environnement ---
# (La lecture des arguments (auteur de l'e-mail et fichiers modifiés))
# Les secrets sont fournis par GitHub Actions via les variables d'environnement.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

# Le script reçoit l'email et la liste des fichiers en arguments de ligne de commande.
if len(sys.argv) != 3:
    print("Erreur : Ce script nécessite l'email de l'auteur et la liste des fichiers modifiés en arguments.")
    sys.exit(1)

recipient_email = sys.argv[1] # L'email de l'auteur du push
changed_files_str = sys.argv[2] # La liste des fichiers modifiés (séparés par des espaces)

# Lecture des contenus des fichiers
changed_files_list = changed_files_str.split(' ')
code_content = ""
files_found = 0

for file_path in changed_files_list:
    # On filtre les fichiers non-pertinents pour la revue (docs, config)
    if file_path and not file_path.startswith(('.github', 'README', 'requirements', 'package', '.git')) and os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Ajout du contenu du fichier au bloc de code principal
                code_content += f"\n--- Contenu du fichier: {file_path} ---\n\n{content}\n"
                files_found += 1
        except Exception as e:
            print(f"Impossible de lire le fichier {file_path}: {e}")

# Si aucun code à analyser, on envoie un e-mail de confirmation et on s'arrête.
if files_found == 0 or not code_content.strip():
    subject = "✅ Revue de Code Automatisée - Aucun Fichier à Examiner"
    body_html = "<h1>Revue Automatisée</h1><p>Aucun fichier de code pertinent n'a été modifié dans ce push.</p>"
    # Une fonction send_email doit exister pour que cela fonctionne (définie plus bas)
    send_email(recipient_email, subject, body_html)
    sys.exit(0)


# --- PARTIE 2 : Construction du prompt pour l'IA ---
# (La construction du prompt pour l'IA, incluant le code)
prompt = f"""
Tu es un expert en revue de code, critique mais toujours constructif et poli.
Ton objectif est d'analyser le code ci-dessous et de fournir une revue détaillée.

Instructions Clés:
1.  **Format de la Réponse:** La réponse DOIT être uniquement en **HTML esthétique et professionnel**. Utilise des balises de mise en forme (`<h1>`, `<ul>`, `<code>`) pour structurer le rapport. N'ajoute rien d'autre que le code HTML.
2.  **Contenu de la Revue:**
    * **Points Positifs:** Mentionne les aspects bien réalisés.
    * **Points à Améliorer:** Surligne les bugs potentiels, les failles de sécurité, ou les optimisations.
    * **Conclusion:** Un résumé et un encouragement final.

CODE À ANALYSER:
{code_content}
"""


# --- PARTIE 3 : Appel à l'API Gemini ---
# (L'appel à l'API Gemini)
try:
    # Initialisation du client avec la clé
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Appel à l'API
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    # Le corps de l'e-mail est la réponse HTML de Gemini
    email_body_html = response.text
    email_subject = "⚠️ Revue de Code Automatisée - Votre Feedback"
    
except APIError as e:
    # Gestion des erreurs de l'API (clé invalide, quota dépassé, etc.)
    print(f"Erreur de l'API Gemini: {e}")
    email_subject = "❌ Erreur de l'API Gemini"
    email_body_html = f"<h1>Erreur de l'API Gemini</h1><p>La revue de code n'a pas pu être complétée.</p>"
except Exception as e:
    # Autres erreurs (clé manquante, etc.)
    print(f"Erreur inconnue: {e}")
    email_subject = "❌ Erreur Critique du Script"
    email_body_html = f"<h1>Erreur Critique</h1><p>Le script a échoué.</p>"


# --- PARTIE 4 : Fonction d'Envoi d'E-mail ---
# (L'envoi de l'e-mail final au développeur)
def send_email(to_email, subject, html_content):
    """Envoie un e-mail via SMTP Gmail."""
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email

    # Le contenu est envoyé en HTML pour un rapport esthétique
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        # Utilisation de SMTP_SSL pour se connecter au serveur Gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        # Authentification avec l'adresse et le mot de passe d'application
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        
        # Envoi de l'e-mail
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.close()
        print(f"E-mail de feedback envoyé avec succès à {to_email}")
    except Exception as e:
        print(f"Échec de l'envoi de l'e-mail: {e}")

# --- EXÉCUTION FINALE ---
# Appel de la fonction pour envoyer le résultat de Gemini ou le message d'erreur.
send_email(recipient_email, email_subject, email_body_html)