from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.services.dashboard_service import DashboardService



router = APIRouter(tags=["Dashboard"], prefix="/dashboard")

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return DashboardService.get_dashboard_summary(db, current_user.id)


@router.get("/my-tasks/{project_id}")
def dashboard_my_tasks(project_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return DashboardService.get_my_tasks(project_id, db, current_user.id)


@router.get("/my-projects")
def dashboard_my_projects(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return DashboardService.get_my_projects(db, current_user.id)


@router.get("/recent-activities")
def dashboard_activities(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return DashboardService.get_recent_activities(db, current_user.id)


@router.get("/deadlines")
def dashboard_deadlines(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return DashboardService.get_deadlines(db, current_user.id)
