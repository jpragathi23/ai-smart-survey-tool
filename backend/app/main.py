# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import survey_routes, voice_routes, analytics_routes, response_routes

app = FastAPI(title="AI Smart Survey Tool")

# CORS config for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Survey Tool API is running!"}

# Include routers
app.include_router(survey_routes.router, prefix="/api/surveys", tags=["Surveys"])
app.include_router(voice_routes.router, prefix="/api/voice", tags=["Voice"])
app.include_router(analytics_routes.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(response_routes.router, prefix="/api/responses", tags=["Responses"])
from app.database import Base, engine
from app.models import survey, question, response  # ✅ import all models

print("📌 Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
