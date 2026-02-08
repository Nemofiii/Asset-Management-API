from fastapi import FastAPI
from Backend.core.database import engine, Base
from Backend.api.user_routes import router
from Backend.api.admin_routes import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Asset Management API"}