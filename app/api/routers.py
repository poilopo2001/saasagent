"""
API Routers - Tous les endpoints FastAPI
"""
import os
import json
import logging
import anthropic
from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.api.schemas import (
    BusinessData,
    SiteGenerationRequest,
    JobResponse,
    PrefillResponse
)
from app.core.config import get_settings
from app.services.job_manager import job_manager

# Ancien système monolithique (commenté mais disponible si besoin de rollback)
# from app.services.generator import GeneratorService

# Nouveau système modulaire (5 phases) - ACTIF
from app.services.generator_modular import GeneratorServiceModular as GeneratorService

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()


@router.post("/prefill", response_model=PrefillResponse)
async def prefill_form(data: BusinessData):
    """
    Analyse la description d'entreprise avec Claude et pré-remplit le formulaire

    Args:
        data: Description de l'entreprise

    Returns:
        Données extraites pour pré-remplir le formulaire
    """
    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        prompt = f"""Analyse cette description d'entreprise et extrais UNIQUEMENT les informations concrètes mentionnées. Si une information n'est PAS explicitement mentionnée, utilise null.

Description: {data.description}

Réponds UNIQUEMENT avec un JSON valide dans ce format exact (sans markdown, sans texte avant ou après):
{{
  "name": "nom exact de l'entreprise ou null",
  "location": "ville/pays ou null",
  "phone": "numéro de téléphone exact ou null",
  "email": "email exact ou null",
  "year": année de création (nombre) ou null,
  "services": "liste des services mentionnés ou null",
  "positioning": "phrase de positionnement ou USP ou null",
  "street": "adresse rue si mentionnée ou null",
  "postal_code": "code postal si mentionné ou null",
  "city": "ville si mentionnée ou null"
}}

IMPORTANT:
- Ne déduis rien, n'invente rien
- Copie les informations EXACTEMENT comme données
- Utilise null si une info n'est pas dans la description"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Nettoyer le markdown si présent
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        parsed_data = json.loads(response_text)

        # Convertir null en chaînes vides pour Pydantic
        for key in parsed_data:
            if parsed_data[key] is None:
                parsed_data[key] = ""

        return PrefillResponse(success=True, data=parsed_data)

    except json.JSONDecodeError as e:
        logger.error(f"Erreur parsing JSON: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur parsing JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Erreur prefill: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.post("/generate", response_model=JobResponse)
async def generate_site(request: SiteGenerationRequest, background_tasks: BackgroundTasks):
    """
    Lance la génération d'un site avec agents spécialisés pour GitHub et Vercel

    Args:
        request: Données complètes de l'entreprise
        background_tasks: Gestionnaire de tâches asynchrones FastAPI

    Returns:
        Informations du job créé
    """
    site_slug = f"{request.name.lower().replace(' ', '-')}-{request.city.lower()}"

    # Créer le job
    job_id = job_manager.create_job(site_slug)

    # Lancer la génération en arrière-plan
    business_dict = request.model_dump()
    background_tasks.add_task(
        GeneratorService.run_generation_workflow,
        job_id,
        business_dict,
        site_slug
    )

    return JobResponse(
        job_id=job_id,
        status="pending",
        message="Génération démarrée avec agents spécialisés"
    )


@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """
    Récupère le statut d'un job de génération

    Args:
        job_id: ID du job

    Returns:
        Statut complet du job
    """
    job = job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} introuvable")

    return job


@router.get("/jobs")
async def list_all_jobs():
    """
    Liste tous les jobs de génération

    Returns:
        Liste de tous les jobs triés par date
    """
    jobs = job_manager.get_all_jobs()
    return {"jobs": jobs}


@router.get("/health")
async def health_check():
    """
    Endpoint de santé pour vérifier que l'API fonctionne

    Returns:
        Statut de santé de l'API
    """
    return {
        "status": "healthy",
        "version": settings.app_version,
        "anthropic_api_configured": bool(settings.anthropic_api_key),
        "github_token_configured": bool(settings.github_token),
        "vercel_token_configured": bool(settings.vercel_token)
    }
