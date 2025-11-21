import os
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from database import db, create_document, get_documents
from schemas import (
    HomepageContent, Service, CaseStudy, Testimonial,
    BlogPost, ContactSubmission, OrganizationProfile
)

app = FastAPI(title="NexTier Solutions API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"name": "NexTier Solutions API", "status": "ok"}


# Public content endpoints
@app.get("/api/content/home", response_model=HomepageContent)
def get_home_content():
    docs = get_documents("homepagecontent", {}, limit=1)
    if docs:
        d = docs[0]
        return HomepageContent(
            hero_heading=d.get("hero_heading"),
            hero_subheading=d.get("hero_subheading"),
            primary_cta=d.get("primary_cta"),
            secondary_cta=d.get("secondary_cta"),
        )
    return HomepageContent(
        hero_heading="Modern Websites, Smart Automation & Secure Digital Solutions.",
        hero_subheading="We help businesses go digital with clean websites, automated workflows, and secure online systems.",
        primary_cta="Book Free Consultation",
        secondary_cta="View Services",
    )


@app.get("/api/content/services", response_model=List[Service])
def get_services():
    docs = get_documents("service", {})
    if docs:
        out = []
        for d in docs:
            out.append(Service(
                key=d.get("key"), title=d.get("title"), subtitle=d.get("subtitle"),
                description=d.get("description"), deliverables=d.get("deliverables", []),
                benefits=d.get("benefits", []),
            ))
        return out
    # defaults
    return [
        Service(
            key="wps",
            title="Website Presence System (WPS)",
            description="Launch a clean, fast, mobile-first website with the essentials baked in.",
            deliverables=[
                "Home / About / Services / Contact",
                "Mobile-first design",
                "Booking & WhatsApp CTAs",
                "Google Maps + contact form",
                "Google Business Profile setup",
                "Basic SEO + analytics",
                "Fast hosting + CDN",
            ],
            benefits=[
                "Clear online presence",
                "Faster discovery",
                "Higher trust",
                "Performance-focused",
            ],
        ),
        Service(
            key="bas",
            title="Business Automation System (BAS)",
            description="Automate lead capture, routing, scheduling, payments and reporting.",
            deliverables=[
                "Zapier/Make integrations",
                "CRM setup (HubSpot/Zoho/Airtable)",
                "Appointment workflows",
                "Payment notifications",
                "Email nurture sequences",
                "Review & feedback automation",
                "Dashboard reporting",
            ],
            benefits=[
                "Save hours weekly",
                "Less manual work",
                "More consistent follow-ups",
            ],
        ),
        Service(
            key="sps",
            title="Security Protection System (SPS)",
            subtitle="Includes Digital Forensics",
            description="Security-first execution across your stack with ongoing protection.",
            deliverables=[
                "HTTPS/SSL",
                "Cloudflare WAF + DDoS",
                "Malware removal & hardening",
                "Backups (daily/weekly)",
                "VAPT-lite scans",
                "Email spoofing protection",
                "Incident recovery support",
                "Uptime & vulnerability monitoring",
                "Digital Forensics (log review, compromise analysis, threat tracing)",
            ],
            benefits=[
                "Reduced risk",
                "Faster recovery",
                "Stronger trust",
            ],
        ),
    ]


@app.get("/api/content/case-studies", response_model=List[CaseStudy])
def get_case_studies():
    docs = get_documents("casestudy", {})
    if docs:
        return [CaseStudy(**{k: d.get(k) for k in ["title", "industry", "summary", "metrics"]}) for d in docs]
    return [
        CaseStudy(
            title="Neighborhood Bistro",
            industry="Restaurant",
            summary="Website revamp with online booking and WhatsApp ordering.",
            metrics=["+37% bookings", "50% faster response time"],
        ),
        CaseStudy(
            title="Harborview Clinic",
            industry="Clinic",
            summary="Appointment system, CRM routing, and autoresponders.",
            metrics=["7 hours/week saved", "+22% show-up rate"],
        ),
        CaseStudy(
            title="Northstar Coaching",
            industry="Coaching",
            summary="Lead capture pages with email automation and dashboards.",
            metrics=["3x lead-to-call rate", "+18% revenue in 90 days"],
        ),
    ]


@app.get("/api/content/testimonials", response_model=List[Testimonial])
def get_testimonials():
    docs = get_documents("testimonial", {})
    if docs:
        return [Testimonial(name=d.get("name"), role=d.get("role"), quote=d.get("quote")) for d in docs]
    return [
        Testimonial(name="Maya R.", role="Clinic Manager", quote="We finally run on one system. Patients book faster and our team gets time back."),
        Testimonial(name="Andre C.", role="Cafe Owner", quote="Clean site, WhatsApp orders, and analytics that actually help. Simple and solid."),
        Testimonial(name="Sofia K.", role="Founder, SaaS", quote="They automate the boring parts and take security seriously. It just works."),
    ]


class ContactIn(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str
    source: Optional[str] = "website"


@app.post("/api/contact")
def submit_contact(payload: ContactIn):
    data = payload.model_dump()
    data["created_at"] = datetime.now(timezone.utc)
    create_document("contactsubmission", data)
    return {"ok": True}


@app.get("/api/settings/org", response_model=OrganizationProfile)
def get_org_profile():
    docs = get_documents("organizationprofile", {}, limit=1)
    if docs:
        d = docs[0]
        return OrganizationProfile(
            name=d.get("name"), tagline=d.get("tagline"), email=d.get("email"),
            phone=d.get("phone"), address=d.get("address"), website=d.get("website"),
        )
    return OrganizationProfile()


# Lightweight Admin (demo)
class AdminLogin(BaseModel):
    email: EmailStr
    password: str


@app.post("/api/admin/login")
def admin_login(_: AdminLogin):
    return {"token": "demo-token"}


@app.get("/api/admin/dashboard")
def admin_dashboard():
    counts = {
        "services": len(get_documents("service", {})),
        "case_studies": len(get_documents("casestudy", {})),
        "blog_posts": len(get_documents("blogpost", {})),
        "contacts": len(get_documents("contactsubmission", {})),
    }
    return {"ok": True, "counts": counts}


# Simple content creation endpoints (no auth for demo)
@app.post("/api/admin/content/home")
def create_home_content(payload: HomepageContent):
    create_document("homepagecontent", payload)
    return {"ok": True}


@app.post("/api/admin/content/service")
def create_service(payload: Service):
    create_document("service", payload)
    return {"ok": True}


@app.post("/api/admin/content/case-study")
def create_case_study(payload: CaseStudy):
    create_document("casestudy", payload)
    return {"ok": True}


@app.post("/api/admin/content/blog")
def create_blog(payload: BlogPost):
    create_document("blogpost", payload)
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
