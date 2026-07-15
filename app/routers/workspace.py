from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from fastapi.templating import Jinja2Templates
from app.database.schemas.workspace import WorkspaceCreate,  WorkspaceResponse, WorkspaceListResponse, WorkspaceUpdate
from app.services.workspace_service import (
    create_workspace_service, 
    all_workspaces_list,
    delete_workspace_service,
    update_workspace_service,
    get_workspace_by_id
)
from fastapi.responses import RedirectResponse
from fastapi import UploadFile, File
from app.utils.file_upload import save_file, delete_file
from app.database.models.workspace import WorkspaceMember, Workspace
from app.database.models.enums import UserRole


templates = Jinja2Templates(directory="app/templates")



router = APIRouter(tags=["workspace"], prefix="/workspaces")



# all workspace manage (create) page render
# @router.get("/create", response_class=HTMLResponse)
# def workspaces_page(request: Request):
#     return templates.TemplateResponse(
#         request= request,
#         name = "all_workspace_manage.html",
#         context={
#             "request":request,
#              "workspace": None
#         }
#     )


# create workspace
# @router.post("/create")
@router.post("/create", response_model=WorkspaceResponse)
def create_workspace(data: WorkspaceCreate = Depends(WorkspaceCreate.as_form),
                      logo: UploadFile = File(None), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    logo_url = "/static/workspace_logos/default-workspace.png"

    if logo and logo.filename:
        logo_url = save_file(
            upload=logo,
            folder="app/static/workspace_logos"
        )

    return create_workspace_service(db, data, current_user.id, logo_url)
    # WorkspaceResponse.model_validate(
    #     create_workspace_service(db, data, current_user.id, logo_url)
    # )

    # return RedirectResponse(
    #     url="/workspaces",
    #     status_code=303
    # )




@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: int, db: Session = Depends(get_db)):
    return get_workspace_by_id(db, workspace_id)



# all workspaces page
@router.get("", 
            # response_class=HTMLResponse
            )
def workspace_list(request: Request, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    workspaces = [
        WorkspaceListResponse.model_validate(workspace)
            for workspace in all_workspaces_list(db, current_user.id)
    ]
    
    workspace_data = []

    for workspace in workspaces:
        workspace_data.append({
            "workspace": workspace,
            "is_owner": workspace.created_by == current_user.id
        })

    # return templates.TemplateResponse(
    #     request= request,
    #     name = "all_workspaces.html",
    #     context={
    #         "request": request,
    #         "workspaces": workspace_data,
    #         "user": current_user
    #     }
    # )
    return workspace_data



# render edit workspace page
# @router.get("/edit/{workspace_id}", response_class=HTMLResponse)
# def edit_workspace_page(workspace_id: int, request: Request, db: Session = Depends(get_db)):
#     workspace = get_workspace_by_id(db, workspace_id)
    
#     return templates.TemplateResponse(
#         request= request,
#         name = "all_workspace_manage.html",
#         context={
#             "request":request,
#             "workspace": workspace
#         }
#     )


# @router.patch("/edit/{workspace_id}")
@router.patch("/edit/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(workspace_id: int, data: WorkspaceUpdate = Depends(WorkspaceUpdate.as_form), 
                     logo: UploadFile = File(None), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )
    new_logo_url = None

    if logo and logo.filename:
        old_logo = workspace.logo_url

        new_logo_url = save_file(
            upload=logo,
            folder="app/static/workspace_logos"
        )

        delete_file(old_logo)
        
    # workspace = WorkspaceResponse.model_validate(
    #     update_workspace_service(workspace_id, db, current_user.id, data, logo_url=new_logo_url)
    # )

    # return RedirectResponse(
    #     url="/workspaces",
    #     status_code=303
    # )

    return update_workspace_service(workspace_id, db, current_user.id, data, logo_url=new_logo_url)



@router.delete("/delete/{workspace_id}")
def delete_workspace(workspace_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_workspace_service(workspace_id, db, current_user.id)
    
    # return RedirectResponse(
    # url="/workspaces",
    # status_code=303
    # )