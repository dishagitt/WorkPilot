from sqlalchemy.orm import Session
from datetime import date
from app.database.models.project import ProjectMember, Project
from app.database.models.task import Task
from app.database.models.enums import TaskPhase
from app.database.schemas.dashboard import (
    DashboardSummaryResponse, 
    DashboardTaskResponse, 
    DashboardActivityResponse, 
    DashboardProjectResponse,
    DashboardDeadlineResponse,
    DeadlineTaskResponse
)
from app.database.models.activity import Activity


class DashboardService:

    @staticmethod
    def get_dashboard_summary(db: Session, current_user_id: int):

        total_projects = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.user_id == current_user_id,
                ProjectMember.is_deleted == False
            )
            .count()
        )

        total_tasks = (
            db.query(Task)
            .filter(
                Task.assigned_to == current_user_id,
                Task.is_deleted == False
            )
            .count()
        )

        completed_tasks = (
            db.query(Task)
            .filter(
                Task.assigned_to == current_user_id,
                Task.phase == TaskPhase.DONE,
                Task.is_deleted == False
            )
            .count()
        )

        pending_tasks = (
            db.query(Task)
            .filter(
                Task.assigned_to == current_user_id,
                Task.phase != TaskPhase.DONE,
                Task.is_deleted == False
            )
            .count()
        )

        overdue_tasks = (
            db.query(Task)
            .filter(
                Task.assigned_to == current_user_id,
                Task.phase != TaskPhase.DONE,
                Task.due_date < date.today(),
                Task.is_deleted == False
            )
            .count()
        )

        return DashboardSummaryResponse(
            total_projects=total_projects,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            overdue_tasks=overdue_tasks
        )


    @staticmethod
    def get_my_tasks(project_id: int, db: Session, current_user_id: int):

        tasks = (
            db.query(Task)
            .join(Project)
            .filter(
                Task.project_id == project_id,
                Task.assigned_to == current_user_id,
                Task.is_deleted == False
            )
            .all()
        )

        return [
            DashboardTaskResponse(
                id=task.id,
                task_number=task.task_number,
                title=task.title,
                project_name=task.project.name,
                priority=task.priority,
                phase=task.phase,
                due_date=task.due_date
            )
            for task in tasks
        ]



    @staticmethod
    def get_my_projects(db: Session, current_user_id: int):

        projects = (
            db.query(Project)
            .join(ProjectMember)
            .filter(
                ProjectMember.user_id == current_user_id,
                ProjectMember.is_deleted == False,
                Project.is_deleted == False
            )
            .all()
        )

        response = []

        for project in projects:

            task_count = (
                db.query(Task)
                .filter(
                    Task.project_id == project.id,
                    Task.is_deleted == False
                )
                .count()
            )

        response.append(
            DashboardProjectResponse(
                id=project.id,
                project_name=project.name,
                total_tasks=task_count
            )
        )



    @staticmethod
    def get_recent_activities(db: Session, current_user_id: int):

        activities = (
            db.query(Activity)
            .join(Task)
            .filter(Activity.user_id == current_user_id)
            .order_by(Activity.created_at.desc())
            .limit(10)
            .all()
        )

        return [
            DashboardActivityResponse(
                id=activity.id,
                task_number=activity.task.task_number,
                action=activity.action,
                created_at=activity.created_at
            )
            for activity in activities
        ]


    @staticmethod
    def get_deadlines(db: Session, current_user_id: int):

        today = date.today()

        due_today_tasks = (
            db.query(Task)
            .filter(
                Task.assigned_to == current_user_id,
                Task.phase != TaskPhase.DONE,
                Task.due_date == today,
                Task.is_deleted == False
            )
            .all()
        )

        overdue_tasks = (
            db.query(Task)
            .filter(
                Task.assigned_to == current_user_id,
                Task.phase != TaskPhase.DONE,
                Task.due_date < today,
                Task.is_deleted == False
            )
            .all()
        )

        return DashboardDeadlineResponse(
            due_today=[
                DeadlineTaskResponse(
                    id=task.id,
                    task_number=task.task_number,
                    title=task.title,
                    due_date=task.due_date,
                    priority=task.priority
                )
                for task in due_today_tasks
            ],
            overdue=[
                DeadlineTaskResponse(
                    id=task.id,
                    task_number=task.task_number,
                    title=task.title,
                    due_date=task.due_date,
                    priority=task.priority
                )
                for task in overdue_tasks
            ]
        )


    






