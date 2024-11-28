from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Configure o CORS para permitir o acesso do front-end
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(router)
