from fastapi import FastAPI
from app.routers import auth, dashboard, workspace
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(workspace.router)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)