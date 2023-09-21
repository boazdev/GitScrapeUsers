from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users_router


app = FastAPI()
#models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router.router)