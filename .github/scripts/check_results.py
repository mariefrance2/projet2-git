
#!/usr/bin/env python3
"""
Vérifie les résultats des tests et envoie un email si erreurs.
"""

import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def check_env_vars() -> bool:
    """Vérifie que les variables d'environnement sont présentes."""
    required = ['EMAIL_USERNAME', 'EMAIL_PASSWORD', 'TEAM_EMAIL']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print(f"Variables manquantes: {', '.join(missing)}")
        return False
    return True


def read_ai_report() -> str:
    """Lit le rapport d'analyse IA."""
    try:
        with open('ai-review-report.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Rapport IA non disponible."


def check_failures() -> dict:
    """Vérifie les échecs des différents outils."""
    failures = {
        'mypy': os.getenv('MYPY_FAILED') == 'true',
        'ruff': os.getenv('RUFF_FAILED') == 'true',
        'pytest': os.getenv('PYTEST_FAILED') == 'true',
        'ai_review': os.getenv('AI_REVIEW_FAILED') == 'true'
    }
    return failures


def generate_email_body(failures: dict, ai_report: str) -> str:
    """Génère le corps de l'email."""
    has_failures = any(failures.values())
    
    if not has_failures:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
        <h2 style="color: #28a745;">✅ Vérification du Code Réussie</h2>
        <p>Tous les tests sont passés avec succès!</p>
        <ul>
            <li>✅ Vérification de typage (mypy)</li>
            <li>✅ Vérification de style (ruff)</li>
            <li>✅ Tests unitaires (pytest)</li>
            <li>✅ Analyse IA</li>
        </ul>
        <p><strong>Date:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
</body>
</html>
"""
    
    # Email d'erreur
    email_body = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff3cd; border-radius: 10px; border-left: 5px solid #ffc107;">
        <h2 style="color: #dc3545;">⚠️ Problèmes Détectés dans le Code</h2>
        <p>Des erreurs ont été détectées lors de la vérification automatique du code.</p>
        
        <h3>Résumé des Vérifications:</h3>
        <ul>
"""
    
    if failures['mypy']:
        email_body += '<li style="color: #dc3545;">❌ <strong>Typage (mypy)</strong>: Erreurs détectées</li>'
    else:
        email_body += '<li style="color: #28a745;">✅ <strong>Typage (mypy)</strong>: OK</li>'
    
    if failures['ruff']:
        email_body += '<li style="color: #dc3545;">❌ <strong>Style (ruff)</strong>: Erreurs détectées</li>'
    else:
        email_body += '<li style="color: #28a745;">✅ <strong>Style (ruff)</strong>: OK</li>'
    
    if failures['pytest']:
        email_body += '<li style="color: #dc3545;">❌ <strong>Tests (pytest)</strong>: Échecs détectés</li>'
    else:
        email_body += '<li style="color: #28a745;">✅ <strong>Tests (pytest)</strong>: OK</li>'
    
    if failures['ai_review']:
        email_body += '<li style="color: #dc3545;">❌ <strong>Analyse IA</strong>: Problèmes critiques</li>'
    else:
        email_body += '<li style="color: #28a745;">✅ <strong>Analyse IA</strong>: OK</li>'
    
    email_body += """
        </ul>
        
        <h3>Comment Corriger:</h3>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
"""
    
    if failures['mypy']:
        email_body += """
            <h4>Erreurs de Typage (mypy):</h4>
            <p>Exécutez localement: <code style="background-color: #e9ecef; padding: 2px 5px; border-radius: 3px;">mypy . --ignore-missing-imports</code></p>
            <p>Ajoutez des type hints à vos fonctions:</p>
            <pre style="background-color: #e9ecef; padding: 10px; border-radius: 5px; overflow-x: auto;">
def ma_fonction(param: str) -> int:
    return len(param)
            </pre>
"""
    
    if failures['ruff']:
        email_body += """
            <h4>Erreurs de Style (ruff):</h4>
            <p>Exécutez localement: <code style="background-color: #e9ecef; padding: 2px 5px; border-radius: 3px;">ruff check . --fix</code></p>
            <p>Ruff corrigera automatiquement la plupart des problèmes de style.</p>
"""
    
    if failures['pytest']:
        email_body += """
            <h4>Tests Échoués (pytest):</h4>
            <p>Exécutez localement: <code style="background-color: #e9ecef; padding: 2px 5px; border-radius: 3px;">pytest tests/ -v</code></p>
            <p>Vérifiez les tests qui échouent et corrigez le code correspondant.</p>
"""
    
    email_body += """
        </div>
        
        <h3>Rapport d'Analyse IA:</h3>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; white-space: pre-wrap; font-family: monospace; font-size: 12px;">
""" + ai_report + """
        </div>
        
        <p><strong>Date:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        
        <hr style="border: none; border-top: 1px solid #dee2e6; margin: 20px 0;">
        <p style="font-size: 12px; color: #6c757d;">
            Ce message a été généré automatiquement par GitHub Actions.<br>
            Pour plus d'informations, consultez les logs de l'action sur GitHub.
        </p>
    </div>
</body>
</html>
"""
    
    return email_body


def send_email(subject: str, body: str) -> bool:
    """Envoie un email."""
    if not check_env_vars():
        print("Impossible d'envoyer l'email: variables manquantes")
        return False
    
    sender = os.getenv('EMAIL_USERNAME')
    password = os.getenv('EMAIL_PASSWORD')
    recipient = os.getenv('TEAM_EMAIL')
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    html_part = MIMEText(body, 'html')
    msg.attach(html_part)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"Email envoyé avec succès à {recipient}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {str(e)}")
        return False


def main():
    """Fonction principale."""
    print("Vérification des résultats...")
    
    failures = check_failures()
    ai_report = read_ai_report()
    
    has_failures = any(failures.values())
    
    if has_failures:
        subject = "⚠️ Problèmes Détectés dans le Code - Action Requise"
        print("\nDes erreurs ont été détectées!")
    else:
        subject = "✅ Vérification du Code Réussie"
        print("\nTous les tests sont passés!")
    
    email_body = generate_email_body(failures, ai_report)
    
    if send_email(subject, email_body):
        print("Notification envoyée avec succès")
    else:
        print("Échec de l'envoi de la notification")
    
    # Sortir avec un code d'erreur si des problèmes ont été détectés
    if has_failures:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
