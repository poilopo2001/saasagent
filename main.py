"""
SaaS Generator v3 - Refactored Architecture
Point d'entrée FastAPI avec architecture modulaire propre
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routers import router

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('saas_generator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestion du cycle de vie de l'application
    Exécuté au démarrage et à l'arrêt
    """
    # Startup
    logger.info(f"🚀 Démarrage de {settings.app_title} v{settings.app_version}")
    logger.info(f"📁 Répertoire de sortie: {settings.output_dir}")
    logger.info(f"🤖 Modèle d'agent: {settings.agent_model}")
    logger.info(f"🔑 Anthropic API: {'✅ Configurée' if settings.anthropic_api_key else '❌ Manquante'}")
    logger.info(f"🔑 GitHub Token: {'✅ Configuré' if settings.github_token else '❌ Manquant'}")
    logger.info(f"🔑 Vercel Token: {'✅ Configuré' if settings.vercel_token else '❌ Manquant'}")

    yield

    # Shutdown
    logger.info(f"🛑 Arrêt de {settings.app_title}")


# Créer l'application FastAPI
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    lifespan=lifespan
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routers
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Endpoint racine avec informations sur l'API"""
    return {
        "name": settings.app_title,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "prefill": "/api/prefill",
            "generate": "/api/generate",
            "job_status": "/api/status/{job_id}",
            "list_jobs": "/api/jobs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
