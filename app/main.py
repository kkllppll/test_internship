# entry point of application
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, users, articles

#create all tables in the database
Base.metadata.create_all(bind=engine)

#initialize the fastapi app with metadata for swagger docs
app = FastAPI(
    title="Internship Tech Task",
    description="REST API endpoints for managing users and articles",
    version="1.0.0"
)

#connect all routers to the app
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(articles.router)

#liveness endpoint to check if the service is running
@app.get("/status", tags=["status"])
def health_check():
    return {"status": "ok"}