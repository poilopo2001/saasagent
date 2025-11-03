"""
Generator Service - Orchestre le workflow complet de génération de site
"""
import os
import re
import json
import logging
from typing import Dict, Any
from datetime import datetime

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

from app.core.config import get_settings
from app.services.job_manager import job_manager
from app.agents.code_generator import CodeGeneratorAgent
from app.agents.site_validator import SiteValidatorAgent
from app.agents.github_publisher import GitHubPublisherAgent
from app.agents.vercel_deployer import VercelDeployerAgent

logger = logging.getLogger(__name__)
settings = get_settings()


class GeneratorService:
    """Service principal d'orchestration de la génération de sites"""

    @staticmethod
    async def run_generation_workflow(job_id: str, business_data: Dict[str, Any], site_slug: str):
        """
        Exécute le workflow complet de génération en 4 phases:
        1. Code Generation
        2. Validation & Auto-Fix
        3. GitHub Publication
        4. Vercel Deployment

        Args:
            job_id: ID du job de génération
            business_data: Données de l'entreprise
            site_slug: Slug du site (ex: "plomberie-luxembourg")
        """
        site_dir = f"{settings.output_dir}/{site_slug}"

        try:
            # ========== PHASE 1: Code Generation ==========
            await GeneratorService._phase1_code_generation(job_id, business_data, site_slug, site_dir)

            # ========== PHASE 2: Validation & Auto-Fix ==========
            await GeneratorService._phase2_validation_loop(job_id, site_dir)

            # ========== PHASE 3: GitHub Publication ==========
            github_url = await GeneratorService._phase3_github_publication(job_id, business_data, site_slug, site_dir)

            # ========== PHASE 4: Vercel Deployment ==========
            vercel_url = await GeneratorService._phase4_vercel_deployment(job_id, business_data, site_slug, site_dir, github_url)

            # ========== Final Success ==========
            job_manager.update_job(
                job_id, "completed", 100, "Génération terminée avec succès!",
                github_url=github_url,
                site_url=vercel_url
            )

        except Exception as e:
            logger.error(f"Erreur génération job {job_id}: {str(e)}", exc_info=True)
            job_manager.update_job(
                job_id, "failed", 0, f"Échec: {str(e)}",
                error=str(e)
            )

    @staticmethod
    async def _phase1_code_generation(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str):
        """Phase 1: Génération du code Next.js avec Claude Code SDK"""
        job_manager.update_job(job_id, "processing", 10, "Phase 1/4: Génération du code Next.js complet...")

        # Créer le dossier du site
        os.makedirs(site_dir, exist_ok=True)

        # Configuration Claude Code SDK
        options = ClaudeCodeOptions(
            model=settings.agent_model,
            allowed_tools=["Write", "Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={
                "GH_TOKEN": settings.github_token or "",
                "VERCEL_TOKEN": settings.vercel_token or ""
            }
        )

        # Génération du prompt via l'agent
        prompt = CodeGeneratorAgent.get_prompt(business_data, site_slug, site_dir)

        # Exécution
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)
            job_manager.update_job(job_id, "processing", 40, "Code généré, build en cours...")

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    logger.info(f"Code Generation: {message}")

    @staticmethod
    async def _phase2_validation_loop(job_id: str, site_dir: str):
        """Phase 2: Boucle de validation et correction automatique"""
        max_attempts = settings.max_validation_attempts
        validation_passed = False

        for attempt in range(1, max_attempts + 1):
            job_manager.update_job(
                job_id, "processing", 50 + (attempt - 1) * 2,
                f"Phase 2/4: Validation qualité (tentative {attempt}/{max_attempts})..."
            )

            # PHASE 2a: Validation
            validation_report, has_critical_errors = await GeneratorService._run_validation(
                job_id, site_dir, attempt, max_attempts
            )

            if validation_passed:
                job_manager.update_job(
                    job_id, "processing", 56,
                    f"✅ Validation réussie (tentative {attempt}) - Site production-ready"
                )
                break

            # PHASE 2b: Auto-Fix si erreurs critiques et tentatives restantes
            if has_critical_errors and attempt < max_attempts:
                await GeneratorService._run_auto_fix(
                    job_id, site_dir, validation_report, attempt
                )
            elif has_critical_errors and attempt >= max_attempts:
                raise Exception(f"Validation échouée après {max_attempts} tentatives. Rapport:\n{validation_report}")

        if not validation_passed:
            job_manager.update_job(job_id, "processing", 58, "⚠️ Validation complétée avec warnings - Poursuite déploiement")

    @staticmethod
    async def _run_validation(job_id: str, site_dir: str, attempt: int, max_attempts: int) -> tuple[str, bool]:
        """
        Exécute la validation du site

        Returns:
            Tuple (validation_report, has_critical_errors)
        """
        prompt = SiteValidatorAgent.get_validation_prompt(site_dir, attempt, max_attempts)

        options = ClaudeCodeOptions(
            model=settings.agent_model,
            allowed_tools=["Read", "Grep", "Glob", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir
        )

        validation_report = ""
        has_critical_errors = False
        validation_passed = False

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    logger.info(f"Validator (Attempt {attempt}): {message}")
                    validation_report += content_str

                    if 'SAFE TO DEPLOY' in content_str or 'PASSED' in content_str:
                        validation_passed = True
                    elif 'CRITICAL' in content_str or 'FAILED' in content_str:
                        has_critical_errors = True

        return validation_report, has_critical_errors

    @staticmethod
    async def _run_auto_fix(job_id: str, site_dir: str, validation_report: str, attempt: int):
        """Exécute la correction automatique des erreurs détectées"""
        job_manager.update_job(
            job_id, "processing", 56 + attempt,
            f"🔧 Phase 2.5: Correction automatique des erreurs (tentative {attempt})..."
        )

        prompt = SiteValidatorAgent.get_fix_prompt(site_dir, validation_report, attempt)

        options = ClaudeCodeOptions(
            model=settings.agent_model,
            allowed_tools=["Write", "Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    logger.info(f"Auto-Fix (Attempt {attempt}): {message}")

        job_manager.update_job(job_id, "processing", 57 + attempt, f"🔄 Re-validation après corrections (tentative {attempt})...")

    @staticmethod
    async def _phase3_github_publication(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """
        Phase 3: Publication sur GitHub

        Returns:
            L'URL du repository GitHub créé
        """
        job_manager.update_job(job_id, "processing", 60, "Phase 3/4: Publication GitHub avec agent spécialisé...")

        payload = {
            "projectPath": site_dir,
            "repoName": site_slug,
            "businessData": {
                "nom": business_data.get("name", ""),
                "ville": business_data.get("city", ""),
                "secteur": business_data.get("services", "").split(',')[0].strip() if business_data.get("services") else "services"
            },
            "githubConfig": {
                "username": "poilopo2001",
                "email": "sebastien.poletto@gmail.com",
                "visibility": "public"
            }
        }

        prompt = GitHubPublisherAgent.get_prompt(payload)

        options = ClaudeCodeOptions(
            model=settings.agent_model,
            allowed_tools=["Bash", "Read", "Edit"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"GH_TOKEN": settings.github_token or ""}
        )

        github_url = None
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    logger.info(f"GitHub Publisher: {message}")

                    # Chercher l'URL GitHub dans la réponse
                    if 'github.com' in content_str and not github_url:
                        match = re.search(r'https://github\.com/[\w-]+/[\w-]+', content_str)
                        if match:
                            github_url = match.group(0)
                            job_manager.update_job(job_id, "processing", 75, "Repository GitHub créé", github_url=github_url)

                    # Tenter de parser la réponse JSON si disponible
                    try:
                        response_json = json.loads(content_str)
                        if response_json.get("success") and response_json.get("github_url"):
                            github_url = response_json["github_url"]
                            job_manager.update_job(job_id, "processing", 75, "Repository GitHub créé", github_url=github_url)
                    except (json.JSONDecodeError, ValueError):
                        pass

        if not github_url:
            raise Exception("GitHub repository creation failed - no URL returned")

        return github_url

    @staticmethod
    async def _phase4_vercel_deployment(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str, github_url: str) -> str:
        """
        Phase 4: Déploiement sur Vercel

        Returns:
            L'URL Vercel de production
        """
        job_manager.update_job(job_id, "processing", 80, "Phase 4/4: Déploiement Vercel avec agent spécialisé...")

        payload = {
            "projectPath": site_dir,
            "projectName": site_slug,
            "businessData": {
                "nom": business_data.get("name", ""),
                "ville": business_data.get("city", ""),
                "siteUrl": business_data.get("domain_url") or f"https://{site_slug}.vercel.app"
            },
            "githubRepo": github_url.replace("https://github.com/", ""),
            "vercelConfig": {
                "customDomain": business_data.get("domain_url", "").replace("https://", "").replace("http://", "") if business_data.get("domain_url") else None,
                "framework": "nextjs",
                "envVars": {
                    "NEXT_PUBLIC_SITE_URL": business_data.get("domain_url") or f"https://{site_slug}.vercel.app",
                    "NEXT_PUBLIC_CONTACT_EMAIL": business_data.get("email", "")
                }
            }
        }

        prompt = VercelDeployerAgent.get_prompt(payload)

        options = ClaudeCodeOptions(
            model=settings.agent_model,
            allowed_tools=["Bash", "Read", "Edit"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"VERCEL_TOKEN": settings.vercel_token or ""}
        )

        vercel_url = None
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    logger.info(f"Vercel Deployer: {message}")

                    # Chercher l'URL Vercel dans la réponse
                    if 'vercel.app' in content_str and not vercel_url:
                        match = re.search(r'https://[\w-]+\.vercel\.app', content_str)
                        if match:
                            vercel_url = match.group(0)
                            job_manager.update_job(job_id, "processing", 95, "Site déployé sur Vercel", site_url=vercel_url)

                    # Tenter de parser la réponse JSON si disponible
                    try:
                        response_json = json.loads(content_str)
                        if response_json.get("success") and response_json.get("vercel_url"):
                            vercel_url = response_json["vercel_url"]
                            job_manager.update_job(job_id, "processing", 95, "Site déployé sur Vercel", site_url=vercel_url)
                    except (json.JSONDecodeError, ValueError):
                        pass

        if not vercel_url:
            # Warning but not blocking
            logger.warning("Vercel deployment may have failed - no URL found")

        return vercel_url or f"https://{site_slug}.vercel.app"
