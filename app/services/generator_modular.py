"""
Generator Service Modular - Orchestre le workflow avec agents modulaires (5 phases)
Cette version remplace le prompt monolithique par 5 phases séquentielles
"""
import os
import re
import json
import logging
from typing import Dict, Any
from datetime import datetime

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

from app.core.config import get_settings
from app.services.job_manager import job_manager
from app.agents.modular import SetupAgent, ComponentAgent, SectionAgent, PageAgent, ContentAgent

logger = logging.getLogger(__name__)
settings = get_settings()


class GeneratorServiceModular:
    """
    Service principal avec architecture modulaire 5 phases

    PHASES DE GÉNÉRATION:
    0. Phase 1: Setup (structure + config)
    1. Phase 2: Components (composants UI de base)
    2. Phase 3: Sections (sections homepage)
    3. Phase 4: Pages (layout + pages complètes)
    4. Phase 5: Content (SEO + métadonnées)

    PHASES DE DÉPLOIEMENT:
    5. Phase Validation & Auto-Fix
    6. Phase GitHub Publication
    7. Phase Vercel Deployment
    """

    @staticmethod
    async def run_generation_workflow(job_id: str, business_data: Dict[str, Any], site_slug: str):
        """
        Exécute le workflow complet de génération en 8 phases:

        GÉNÉRATION (40% du workflow):
        1. Phase 1: Setup - 0-8%
        2. Phase 2: Components - 8-16%
        3. Phase 3: Sections - 16-24%
        4. Phase 4: Pages - 24-32%
        5. Phase 5: Content/SEO - 32-40%

        DÉPLOIEMENT (60% du workflow):
        6. Validation & Auto-Fix - 40-58%
        7. GitHub Publication - 58-75%
        8. Vercel Deployment - 75-100%

        Args:
            job_id: ID du job de génération
            business_data: Données de l'entreprise
            site_slug: Slug du site (ex: "plomberie-luxembourg")
        """
        site_dir = f"{settings.output_dir}/{site_slug}"

        try:
            # ========== GÉNÉRATION MODULAIRE ==========

            # Phase 1: Setup
            await GeneratorServiceModular._phase1_setup(job_id, business_data, site_slug, site_dir)

            # Phase 2: Components
            await GeneratorServiceModular._phase2_components(job_id, business_data, site_dir)

            # Phase 3: Sections
            await GeneratorServiceModular._phase3_sections(job_id, business_data, site_dir)

            # Phase 4: Pages
            await GeneratorServiceModular._phase4_pages(job_id, business_data, site_slug, site_dir)

            # Phase 5: Content/SEO
            await GeneratorServiceModular._phase5_content(job_id, business_data, site_slug, site_dir)

            # ========== VALIDATION ==========
            await GeneratorServiceModular._phase6_validation_loop(job_id, site_dir)

            # ========== DÉPLOIEMENT ==========
            # Phase 7: GitHub
            github_url = await GeneratorServiceModular._phase7_github_publication(job_id, business_data, site_slug, site_dir)

            # Phase 8: Vercel
            vercel_url = await GeneratorServiceModular._phase8_vercel_deployment(job_id, business_data, site_slug, site_dir, github_url)

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
    async def _execute_phase(job_id: str, phase_name: str, agent_class, business_data: Dict[str, Any],
                            site_slug: str, site_dir: str, start_progress: int, end_progress: int):
        """
        Méthode générique pour exécuter une phase

        Args:
            job_id: ID du job
            phase_name: Nom de la phase (ex: "Phase 1: Setup")
            agent_class: Classe de l'agent (SetupAgent, ComponentAgent, etc.)
            business_data: Données business
            site_slug: Slug du site
            site_dir: Répertoire du site
            start_progress: Progression de départ (%)
            end_progress: Progression de fin (%)
        """
        job_manager.update_job(
            job_id, "processing", start_progress,
            f"🔨 {phase_name} en cours..."
        )

        # Créer le dossier si Phase 1
        if "Setup" in phase_name:
            os.makedirs(site_dir, exist_ok=True)

        # Générer le prompt via l'agent spécialisé
        prompt = agent_class.get_prompt(business_data, site_slug, site_dir)

        # Configuration Claude Agent SDK
        options = ClaudeAgentOptions(
            model=settings.agent_model,
            allowed_tools=["Write", "Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            system_prompt={"type": "preset", "preset": "claude_code"}
        )

        # Exécution
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    logger.info(f"{phase_name}: {message}")

        job_manager.update_job(
            job_id, "processing", end_progress,
            f"✅ {phase_name} terminée"
        )

    @staticmethod
    async def _phase1_setup(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str):
        """Phase 1: Setup - Structure + Configuration (0-8%)"""
        await GeneratorServiceModular._execute_phase(
            job_id, "Phase 1/5: Setup", SetupAgent,
            business_data, site_slug, site_dir, 0, 8
        )

    @staticmethod
    async def _phase2_components(job_id: str, business_data: Dict[str, Any], site_dir: str):
        """Phase 2: Components UI de base (8-16%)"""
        await GeneratorServiceModular._execute_phase(
            job_id, "Phase 2/5: Components UI", ComponentAgent,
            business_data, "", site_dir, 8, 16
        )

    @staticmethod
    async def _phase3_sections(job_id: str, business_data: Dict[str, Any], site_dir: str):
        """Phase 3: Sections homepage (16-24%)"""
        await GeneratorServiceModular._execute_phase(
            job_id, "Phase 3/5: Sections", SectionAgent,
            business_data, "", site_dir, 16, 24
        )

    @staticmethod
    async def _phase4_pages(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str):
        """Phase 4: Pages + Layout (24-32%)"""
        await GeneratorServiceModular._execute_phase(
            job_id, "Phase 4/5: Pages & Layout", PageAgent,
            business_data, site_slug, site_dir, 24, 32
        )

    @staticmethod
    async def _phase5_content(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str):
        """Phase 5: Content/SEO + Métadonnées (32-40%)"""
        await GeneratorServiceModular._execute_phase(
            job_id, "Phase 5/5: SEO & Content", ContentAgent,
            business_data, site_slug, site_dir, 32, 40
        )

    @staticmethod
    async def _phase6_validation_loop(job_id: str, site_dir: str):
        """Phase 6: Boucle de validation et correction automatique (40-58%)"""
        max_attempts = settings.max_validation_attempts
        validation_passed = False

        for attempt in range(1, max_attempts + 1):
            job_manager.update_job(
                job_id, "processing", 40 + (attempt - 1) * 6,
                f"🔍 Phase 6: Validation qualité (tentative {attempt}/{max_attempts})..."
            )

            # Validation
            validation_report, has_critical_errors = await GeneratorServiceModular._run_validation(
                job_id, site_dir, attempt, max_attempts
            )

            if not has_critical_errors:
                validation_passed = True
                job_manager.update_job(
                    job_id, "processing", 56,
                    f"✅ Validation réussie - Site production-ready"
                )
                break

            # Auto-Fix si erreurs critiques et tentatives restantes
            if has_critical_errors and attempt < max_attempts:
                await GeneratorServiceModular._run_auto_fix(
                    job_id, site_dir, validation_report, attempt
                )
            elif has_critical_errors and attempt >= max_attempts:
                raise Exception(f"Validation échouée après {max_attempts} tentatives. Rapport:\n{validation_report}")

        if not validation_passed:
            job_manager.update_job(job_id, "processing", 58, "⚠️ Validation complétée avec warnings")

    @staticmethod
    async def _run_validation(job_id: str, site_dir: str, attempt: int, max_attempts: int) -> tuple[str, bool]:
        """Exécute la validation du site"""
        prompt = SiteValidatorAgent.get_validation_prompt(site_dir, attempt, max_attempts)

        options = ClaudeAgentOptions(
            model=settings.agent_model,
            allowed_tools=["Read", "Grep", "Glob", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            system_prompt={"type": "preset", "preset": "claude_code"}
        )

        validation_report = ""
        has_critical_errors = False

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    logger.info(f"Validator (Attempt {attempt}): {message}")
                    validation_report += content_str

                    if 'SAFE TO DEPLOY' in content_str or 'PASSED' in content_str:
                        has_critical_errors = False
                    elif 'CRITICAL' in content_str or 'FAILED' in content_str:
                        has_critical_errors = True

        return validation_report, has_critical_errors

    @staticmethod
    async def _run_auto_fix(job_id: str, site_dir: str, validation_report: str, attempt: int):
        """Exécute la correction automatique des erreurs"""
        job_manager.update_job(
            job_id, "processing", 42 + attempt * 6,
            f"🔧 Auto-correction des erreurs (tentative {attempt})..."
        )

        prompt = SiteValidatorAgent.get_fix_prompt(site_dir, validation_report, attempt)

        options = ClaudeAgentOptions(
            model=settings.agent_model,
            allowed_tools=["Write", "Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            system_prompt={"type": "preset", "preset": "claude_code"}
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    logger.info(f"Auto-Fix (Attempt {attempt}): {message}")

    @staticmethod
    async def _phase7_github_publication(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """Phase 7: Publication sur GitHub (58-75%)"""
        job_manager.update_job(job_id, "processing", 58, "📦 Phase 7: Publication GitHub...")

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

        options = ClaudeAgentOptions(
            model=settings.agent_model,
            allowed_tools=["Bash", "Read", "Edit"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"GH_TOKEN": settings.github_token or ""},
            system_prompt={"type": "preset", "preset": "claude_code"}
        )

        github_url = None
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    logger.info(f"GitHub Publisher: {message}")

                    if 'github.com' in content_str and not github_url:
                        match = re.search(r'https://github\.com/[\w-]+/[\w-]+', content_str)
                        if match:
                            github_url = match.group(0)
                            job_manager.update_job(job_id, "processing", 75, "✅ Repository GitHub créé", github_url=github_url)

                    try:
                        response_json = json.loads(content_str)
                        if response_json.get("success") and response_json.get("github_url"):
                            github_url = response_json["github_url"]
                            job_manager.update_job(job_id, "processing", 75, "✅ Repository GitHub créé", github_url=github_url)
                    except (json.JSONDecodeError, ValueError):
                        pass

        if not github_url:
            raise Exception("GitHub repository creation failed - no URL returned")

        return github_url

    @staticmethod
    async def _phase8_vercel_deployment(job_id: str, business_data: Dict[str, Any], site_slug: str, site_dir: str, github_url: str) -> str:
        """Phase 8: Déploiement sur Vercel (75-100%)"""
        job_manager.update_job(job_id, "processing", 75, "🚀 Phase 8: Déploiement Vercel...")

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

        options = ClaudeAgentOptions(
            model=settings.agent_model,
            allowed_tools=["Bash", "Read", "Edit"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"VERCEL_TOKEN": settings.vercel_token or ""},
            system_prompt={"type": "preset", "preset": "claude_code"}
        )

        vercel_url = None
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    logger.info(f"Vercel Deployer: {message}")

                    if 'vercel.app' in content_str and not vercel_url:
                        match = re.search(r'https://[\w-]+\.vercel\.app', content_str)
                        if match:
                            vercel_url = match.group(0)
                            job_manager.update_job(job_id, "processing", 95, "✅ Site déployé sur Vercel", site_url=vercel_url)

                    try:
                        response_json = json.loads(content_str)
                        if response_json.get("success") and response_json.get("vercel_url"):
                            vercel_url = response_json["vercel_url"]
                            job_manager.update_job(job_id, "processing", 95, "✅ Site déployé sur Vercel", site_url=vercel_url)
                    except (json.JSONDecodeError, ValueError):
                        pass

        if not vercel_url:
            logger.warning("Vercel deployment may have failed - no URL found")

        return vercel_url or f"https://{site_slug}.vercel.app"
