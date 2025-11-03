"""
GitHub Publisher Agent - Publie le code sur GitHub avec configuration intelligente
"""
import json
from typing import Dict, Any


class GitHubPublisherAgent:
    """Agent spécialisé dans la publication de projets sur GitHub"""

    @staticmethod
    def get_prompt(payload: Dict[str, Any]) -> str:
        """
        Génère le prompt de publication GitHub

        Args:
            payload: Configuration de publication contenant:
                - projectPath: Chemin du projet
                - repoName: Nom du repository
                - businessData: Données de l'entreprise
                - githubConfig: Configuration GitHub

        Returns:
            Le prompt de publication avec réponse JSON structurée
        """
        return f"""Tu es l'agent github-publisher. Publie ce projet sur GitHub avec la configuration suivante:

{json.dumps(payload, indent=2, ensure_ascii=False)}

Exécute TOUTES les phases de ton workflow (1-6) de manière complète et systématique.

À la fin, réponds UNIQUEMENT avec un objet JSON au format suivant:
{{
  "success": true,
  "github_url": "https://github.com/username/repo-name",
  "message": "Repository créé et code publié avec succès"
}}

Si tu rencontres une erreur, réponds:
{{
  "success": false,
  "error": "Description de l'erreur",
  "message": "Échec de la publication GitHub"
}}"""
