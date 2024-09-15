from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, leads, campaigns, analytics

app = FastAPI(title="SaaS Lead Finder API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(leads.router, prefix="/leads", tags=["leads"])
app.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {"message": "Welcome to SaaS Lead Finder API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)