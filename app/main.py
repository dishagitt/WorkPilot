from fastapi import FastAPI
from app.routers import auth, dashboard, workspace, project
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(workspace.router)
app.include_router(project.router)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)