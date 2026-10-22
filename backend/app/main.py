from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import PROJECT_NAME, PROJECT_VERSION, API_PREFIX, CORS_ORIGINS
from .database import init_db
from .api import health, profile, scenarios, purchases, emi, installments

# Initialize database schema
init_db()

app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description="Deterministic Multi-Timeline Financial Future Simulation & Affordability Decision Platform",
    docs_url=f"{API_PREFIX}/docs",
    openapi_url=f"{API_PREFIX}/openapi.json"
)

# CORS Middleware for local frontend & Streamlit integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health.router, prefix=API_PREFIX)
app.include_router(profile.router, prefix=API_PREFIX)
app.include_router(scenarios.router, prefix=API_PREFIX)
app.include_router(purchases.router, prefix=API_PREFIX)
app.include_router(emi.router, prefix=API_PREFIX)
app.include_router(installments.router, prefix=API_PREFIX)

@app.get("/")
def read_root():
    return {
        "product": PROJECT_NAME,
        "tagline": "Explore your financial futures before making a decision.",
        "documentation": f"{API_PREFIX}/docs",
        "api_endpoints": [
            f"{API_PREFIX}/health",
            f"{API_PREFIX}/profile",
            f"{API_PREFIX}/scenarios/simulate",
            f"{API_PREFIX}/purchases/evaluate",
            f"{API_PREFIX}/emi/calculate",
            f"{API_PREFIX}/installments"
        ]
    }
