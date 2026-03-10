
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.catalogos_routes import router as catalogos_router
from routes.personas_routes import router as personas_router
from routes.atenciones_routes import router as atenciones_router
from routes.roles_routes import router as roles_router



app = FastAPI()


origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    "http://localhost",
    # "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # En desarrollo, si necesitas abrir todo: ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(catalogos_router)
app.include_router(personas_router)
app.include_router(atenciones_router)
app.include_router(roles_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

