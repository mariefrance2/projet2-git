
#!/usr/bin/env python3
"""
Script d'analyse IA du code avec profilage personnalisé.
Utilise Groq API (gratuit).
"""

import os
import sys
import json
import subprocess
import requests
from typing import List, Dict, Any


def get_changed_files() -> List[str]:
    """Récupère la liste des fichiers Python modifiés."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f.endswith('.py')]
        return files
    except subprocess.CalledProcessError:
        result = subprocess.run(
            ['git', 'ls-files', '*.py'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip().split('\n')


def get_commit_author() -> str:
    """Récupère l'auteur du commit."""
    result = subprocess.run(
        ['git', 'log', '-1', '--pretty=format:%ae'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def load_team_profiles() -> Dict[str, Any]:
    """Charge les profils de l'équipe."""
    profile_path = '.github/team_profiles.json'
    if os.path.exists(profile_path):
        with open(profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def read_file_content(filepath: str) -> str:
    """Lit le contenu d'un fichier."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Erreur de lecture: {str(e)}"


def analyze_code_with_groq(files: List[str], author_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Analyse le code avec l'IA Groq."""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("⚠️ GROQ_API_KEY non trouvée, analyse IA ignorée.")
        return {"analyses": []}
    
    results = []
    
    personality = author_profile.get('personality', 'standard')
    experience = author_profile.get('experience_level', 'intermediate')
    preferences = author_profile.get('preferences', {})
    
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        
        code = read_file_content(filepath)
        
        prompt = f"""
Tu es un expert en revue de code Python. Analyse ce code et fournis un feedback personnalisé.

**Profil du développeur:**
- Niveau: {experience}
- Personnalité: {personality}
- Préférences: {json.dumps(preferences, ensure_ascii=False)}

**Code à analyser ({filepath}):**
```python
{code}
```

**Instructions:**
1. Adapte ton ton selon la personnalité ({personality})
2. Ajuste la profondeur selon le niveau ({experience})
3. Identifie les problèmes critiques (bugs, sécurité)
4. Vérifie le typage Python (type hints)
5. Suggère des optimisations de performance
6. Propose des améliorations de style

Réponds en JSON avec cette structure exacte:
{{
    "score": 8,
    "critical_issues": ["liste des problèmes critiques"],
    "type_issues": ["problèmes de typage"],
    "performance_tips": ["conseils de performance"],
    "style_suggestions": ["suggestions de style"],
    "summary": "Résumé personnalisé en 2-3 phrases"
}}
"""
        
        try:
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama-3.1-70b-versatile',
                    'messages': [
                        {'role': 'system', 'content': 'Tu es un expert en revue de code Python.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.3,
                    'max_tokens': 2000
                }
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(content)
                analysis["file"] = filepath
                results.append(analysis)
            else:
                raise Exception(f"Erreur API: {response.status_code}")
            
        except Exception as e:
            results.append({
                "file": filepath,
                "error": str(e),
                "score": 5,
                "critical_issues": [],
                "type_issues": [],
                "performance_tips": [],
                "style_suggestions": [],
                "summary": f"Erreur lors de l'analyse: {str(e)}"
            })
    
    return {"analyses": results}


def generate_report(analysis_results: Dict[str, Any], author: str) -> str:
    """Génère un rapport détaillé."""
    report = f"""
# Rapport d'Analyse IA du Code (Groq)

**Auteur**: {author}
**Date**: {subprocess.run(['date'], capture_output=True, text=True, shell=True).stdout.strip()}

---

"""
    
    for analysis in analysis_results.get("analyses", []):
        filepath = analysis.get("file", "Unknown")
        score = analysis.get("score", 0)
        
        report += f"\n## {filepath}\n"
        report += f"**Score de qualité**: {score}/10\n\n"
        
        if analysis.get("error"):
            report += f"**Erreur**: {analysis['error']}\n\n"
            continue
        
        if analysis.get("critical_issues"):
            report += "### Problèmes Critiques\n"
            for issue in analysis["critical_issues"]:
                report += f"- {issue}\n"
            report += "\n"
        
        if analysis.get("type_issues"):
            report += "### Problèmes de Typage\n"
            for issue in analysis["type_issues"]:
                report += f"- {issue}\n"
            report += "\n"
        
        if analysis.get("performance_tips"):
            report += "### Optimisations Possibles\n"
            for tip in analysis["performance_tips"]:
                report += f"- {tip}\n"
            report += "\n"
        
        if analysis.get("style_suggestions"):
            report += "### Suggestions de Style\n"
            for suggestion in analysis["style_suggestions"]:
                report += f"- {suggestion}\n"
            report += "\n"
        
        if analysis.get("summary"):
            report += f"**Résumé**: {analysis['summary']}\n\n"
        
        report += "---\n"
    
    return report


def main():
    """Fonction principale."""
    print("Démarrage de l'analyse IA du code avec Groq...")
    
    changed_files = get_changed_files()
    if not changed_files or changed_files == ['']:
        print("Aucun fichier Python modifié.")
        return
    
    print(f"Fichiers à analyser: {', '.join(changed_files)}")
    
    profiles = load_team_profiles()
    author = get_commit_author()
    author_profile = profiles.get(author, {})
    
    print(f"Auteur: {author}")
    if author_profile:
        print(f"Profil: {author_profile.get('personality', 'standard')}")
    
    results = analyze_code_with_groq(changed_files, author_profile)
    report = generate_report(results, author)
    
    with open("ai-review-report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n" + report)
    
    has_critical = any(
        analysis.get("critical_issues")
        for analysis in results.get("analyses", [])
    )
    
    if has_critical:
        print("\nDes problèmes critiques ont été détectés!")
        sys.exit(1)
    
    print("\nAnalyse IA terminée avec succès!")


if __name__ == "__main__":
    main()