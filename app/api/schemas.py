"""
Modèles Pydantic pour la validation des données d'API
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class BusinessData(BaseModel):
    """Données de description d'entreprise pour l'AI prefill"""
    description: str = Field(..., min_length=10, description="Description de l'entreprise")


class SiteGenerationRequest(BaseModel):
    """Requête complète pour générer un site web"""
    name: str = Field(..., min_length=2, description="Nom de l'entreprise")
    location: str = Field(..., description="Ville/Pays")
    phone: str = Field(..., description="Numéro de téléphone")
    email: EmailStr = Field(..., description="Email de contact")
    year: int = Field(..., ge=1900, le=2100, description="Année de création")
    services: str = Field(..., description="Services offerts (séparés par virgules)")
    positioning: str = Field(..., description="Positionnement unique de l'entreprise")
    street: str = Field(..., description="Adresse rue")
    postal_code: str = Field(..., description="Code postal")
    city: str = Field(..., description="Ville")
    country: str = Field(default="Luxembourg", description="Pays")
    hours: str = Field(default="Lundi-Vendredi 8h-18h", description="Horaires d'ouverture")
    primary_color: str = Field(default="#1a5490", description="Couleur primaire (hex)")
    secondary_color: str = Field(default="#ff8c42", description="Couleur secondaire (hex)")
    domain_url: Optional[str] = Field(default=None, description="URL du domaine")


class JobStatus(BaseModel):
    """Statut d'un job de génération"""
    job_id: str
    status: str  # "pending", "in_progress", "completed", "failed"
    progress: int = Field(ge=0, le=100, description="Progression en %")
    message: str = Field(default="", description="Message de statut")
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = Field(default=None, description="Résultat final")
    error: Optional[str] = Field(default=None, description="Message d'erreur si échec")


class JobResponse(BaseModel):
    """Réponse lors de la création d'un job"""
    job_id: str
    status: str
    message: str


class PrefillResponse(BaseModel):
    """Réponse du service de prefill AI"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
