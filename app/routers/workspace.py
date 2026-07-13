from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from fastapi.templating import Jinja2Templates
from app.database.schemas.workspace import WorkspaceCreate,  WorkspaceResponse, WorkspaceListResponse
from app.services.workspace_service import (
    create_workspace_service, 
    all_workspaces_list,
    delete_workspace_service
)
from fastapi.responses import RedirectResponse
from fastapi import UploadFile, File
from app.utils.file_upload import save_file
from app.database.models.workspace import WorkspaceMember
from app.database.models.enums import WorkspaceMemberRole


templates = Jinja2Templates(directory="app/templates")



router = APIRouter(tags=["workspace"], prefix="/workspaces")


# all workspaces page
@router.get("", response_class=HTMLResponse)
def workspaces_list(request: Request, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    workspaces = [
        WorkspaceListResponse.model_validate(workspace)
            for workspace in all_workspaces_list(db)
    ]
    
    workspace_data = []

    for workspace in workspaces:
        membership = (
            db.query(WorkspaceMember)
            .filter(
                WorkspaceMember.workspace_id == workspace.id,
                WorkspaceMember.user_id == current_user.id,
                WorkspaceMember.is_active == True
            )
            .first()
        )

        workspace_data.append({
            "workspace": workspace,
            "is_owner": (
                membership is not None and 
                membership.role == WorkspaceMemberRole.OWNER
            )
        })

    return templates.TemplateResponse(
        request= request,
        name = "all_workspaces.html",
        context={
            "request": request,
            "workspaces": workspace_data,
            "user": current_user
        }
    )



# all workspace manage (create) page render
@router.get("/create", response_class=HTMLResponse)
def workspaces_page(request: Request):
    return templates.TemplateResponse(
        request= request,
        name = "all_workspace_manage.html",
        context={"request":request}
    )


# create workspace
@router.post("/create")
def create_workspace(data: WorkspaceCreate = Depends(WorkspaceCreate.as_form), logo: UploadFile = File(None), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    logo_url = "/static/workspace_logos/default-workspace.jpg"

    if logo and logo.filename:
        logo_url = save_file(
            upload=logo,
            folder="app/static/workspace_logos"
        )

    WorkspaceResponse.model_validate(
        create_workspace_service(db, data, current_user.id, logo_url)
    )

    return RedirectResponse(
        url="/workspaces",
        status_code=303
    )


@router.delete("/delete/{workspace_id}")
def delete_project(workspace_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    delete_workspace_service(workspace_id, db, current_user.id)
    
    return RedirectResponse(
    url="/workspaces",
    status_code=303
    )