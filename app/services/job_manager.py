"""
Job Manager - Gestion centralisée des jobs de génération
"""
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JobManager:
    """Gestionnaire de jobs avec stockage en mémoire"""

    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}

    def create_job(self, site_slug: str) -> str:
        """
        Crée un nouveau job de génération

        Args:
            site_slug: Slug du site (ex: "plomberie-luxembourg")

        Returns:
            L'ID du job créé
        """
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.jobs[job_id] = {
            "id": job_id,
            "status": "pending",
            "progress": 0,
            "message": "Initialisation...",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "site_slug": site_slug
        }

        logger.info(f"Job créé: {job_id} pour {site_slug}")
        return job_id

    def update_job(self, job_id: str, status: str, progress: int, message: str, **kwargs):
        """
        Met à jour un job existant

        Args:
            job_id: ID du job
            status: Nouveau statut (pending, processing, completed, failed)
            progress: Progression en % (0-100)
            message: Message de statut
            **kwargs: Champs additionnels (github_url, site_url, error, etc.)
        """
        if job_id not in self.jobs:
            logger.warning(f"Tentative de mise à jour d'un job inexistant: {job_id}")
            return

        self.jobs[job_id].update({
            "status": status,
            "progress": progress,
            "message": message,
            "updated_at": datetime.now().isoformat(),
            **kwargs
        })

        logger.info(f"Job {job_id} mis à jour: {status} ({progress}%) - {message}")

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère les informations d'un job

        Args:
            job_id: ID du job

        Returns:
            Dictionnaire avec les infos du job ou None si introuvable
        """
        return self.jobs.get(job_id)

    def get_all_jobs(self) -> list:
        """
        Récupère tous les jobs

        Returns:
            Liste de tous les jobs triés par date de création (plus récents en premier)
        """
        return sorted(
            self.jobs.values(),
            key=lambda x: x["created_at"],
            reverse=True
        )

    def delete_job(self, job_id: str) -> bool:
        """
        Supprime un job

        Args:
            job_id: ID du job à supprimer

        Returns:
            True si supprimé, False si inexistant
        """
        if job_id in self.jobs:
            del self.jobs[job_id]
            logger.info(f"Job supprimé: {job_id}")
            return True
        return False


# Singleton instance
job_manager = JobManager()
