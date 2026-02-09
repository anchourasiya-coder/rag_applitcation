
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from services.adminDataIngestion.adminDataLoader import router as ingest_router
# from services.queryExtraction.queryHandler import router as query_router

# app = FastAPI(
#     title="RAG Ingestion Backend",
#     description="Backend service for sitemap ingestion and vector DB storage",
#     version="1.0.0"
# )

from routes.dataIngestionRoutes import router as ingest_router
from routes.queryExtractionRoutes import router as query_router
app = FastAPI(title="RAG Backend MVC")

# Include the routers you defined in the routes/ folder
app.include_router(ingest_router)
app.include_router(query_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(ingest_router, prefix="/ingest", tags=["Ingestion"]) 

# app.include_router(query_router, prefix="/query", tags=["Retrieval"])      

@app.get("/")
def health_check():
    return {"status": "RAG backend running!"}
