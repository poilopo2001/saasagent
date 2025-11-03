"""
Vercel Deployer Agent - Déploie le site sur Vercel avec configuration optimale
"""
import json
from typing import Dict, Any


class VercelDeployerAgent:
    """Agent spécialisé dans le déploiement Vercel de projets Next.js"""

    @staticmethod
    def get_prompt(payload: Dict[str, Any]) -> str:
        """
        Génère le prompt de déploiement Vercel

        Args:
            payload: Configuration de déploiement contenant:
                - projectPath: Chemin du projet
                - projectName: Nom du projet
                - businessData: Données de l'entreprise
                - githubRepo: Repository GitHub (username/repo)
                - vercelConfig: Configuration Vercel

        Returns:
            Le prompt de déploiement avec réponse JSON structurée
        """
        return f"""Tu es l'agent vercel-deployer. Déploie ce projet Next.js sur Vercel avec la configuration suivante:

{json.dumps(payload, indent=2, ensure_ascii=False)}

Exécute TOUTES les phases de ton workflow (1-9) de manière complète et systématique.

À la fin, réponds UNIQUEMENT avec un objet JSON au format suivant:
{{
  "success": true,
  "vercel_url": "https://project-name.vercel.app",
  "production_url": "https://custom-domain.com",
  "message": "Déploiement Vercel réussi"
}}

Si tu rencontres une erreur, réponds:
{{
  "success": false,
  "error": "Description de l'erreur",
  "message": "Échec du déploiement Vercel"
}}"""
