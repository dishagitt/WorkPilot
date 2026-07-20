from fastapi import APIRouter, Depends
from app.database.schemas.task import BoardListResponse, TaskPhase
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.board_service import BoardService

router = APIRouter(tags=["Board"])


@router.get("/project/{project_id}/board", response_model=BoardListResponse)
def project_board(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BoardService.project_board(project_id, db, current_user.id)
