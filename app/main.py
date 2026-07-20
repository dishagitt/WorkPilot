from fastapi import FastAPI
from app.routers import auth, dashboard, workspace, project, member, task, user, board, comment
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dashboard.router)
app.include_router(workspace.router)
app.include_router(project.router)
app.include_router(member.router)
app.include_router(task.router)
app.include_router(board.router)
app.include_router(comment.router)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)