"""
Database Schemas for NexTier Solutions CMS

Each Pydantic model corresponds to a MongoDB collection (lowercased class name).
These models validate content edited via the lightweight admin panel.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class AdminUser(BaseModel):
    email: EmailStr
    password_hash: str
    role: str = Field(default="admin")

class HomepageContent(BaseModel):
    hero_heading: str
    hero_subheading: str
    primary_cta: str
    secondary_cta: str

class Service(BaseModel):
    key: str = Field(..., description="wps | bas | sps")
    title: str
    subtitle: Optional[str] = None
    description: str
    deliverables: List[str] = []
    benefits: List[str] = []

class CaseStudy(BaseModel):
    title: str
    industry: str
    summary: str
    metrics: List[str] = []

class Testimonial(BaseModel):
    name: str
    role: Optional[str] = None
    quote: str

class BlogPost(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    published: bool = True

class ContactSubmission(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str
    source: Optional[str] = None
    created_at: Optional[datetime] = None

# Minimal settings/organization profile for structured data
class OrganizationProfile(BaseModel):
    name: str = "NexTier Solutions"
    tagline: str = "Empowering Digital Growth, Securely."
    email: Optional[EmailStr] = "hello@nextier.solutions"
    phone: Optional[str] = "+1 (555) 010-2025"
    address: Optional[str] = "San Francisco, CA"
    website: Optional[str] = "https://nextier.solutions"
