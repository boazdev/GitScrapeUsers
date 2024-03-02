from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users_router,scrape_router
from app.settings.config import get_settings

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
app.include_router(scrape_router.router)
@app.get('/health',status_code=200,response_model=str)
def health_check():
    return "github users scraper api is running"

settings_obj = get_settings()
print(f'settings url: {settings_obj}')
