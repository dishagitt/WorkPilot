from fastapi import FastAPI
from app.routers import auth, dashboard, workspace, project, member
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(workspace.router)
app.include_router(project.router)
app.include_router(member.router)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)