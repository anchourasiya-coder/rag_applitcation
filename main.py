
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# from services.adminDataIngestion.adminDataLoader import router as ingest_router
# from services.queryExtraction.queryHandler import router as query_router

from routes.ingestion_routes import router as ingest_router
from routes.query_extraction_routes import router as query_router
from core.loginAuth import login, LoginRequest, LoginResponse
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

@app.get("/")
def health_check():
    return {"status": "RAG backend running!"}

@app.post("/login")
async def admin_login(credentials: LoginRequest) -> LoginResponse:
  
    return login(credentials)
