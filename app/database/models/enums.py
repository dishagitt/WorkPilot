from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    MEMBER = "member"


class ProjectMemberRole(Enum):
    PROJECT_MANAGER = "project_manager"
    DEVELOPER = "developer"
    QA = "qa"
    DESIGNER = "designer"


class TaskPhase(Enum):
    TO_DO = "to_do"
    IN_DEVELOPMENT = "in_development"
    IN_QA = "in_qa"
    DONE = "done"


class TaskPriority(Enum):
    CRITICAL ="critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskType(Enum):
    TASK = "task"
    STORY = "story"
    BUG = "bug"


class ActivityAction(Enum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_ASSIGNED = "task_assigned"
    TASK_DELETED = "task_deleted"

    COMMENT_ADDED = "comment_added"
    COMMENT_UPDATED = "comment_updated"

    PHASE_CHANGED = "phase_changed"
    PRIORITY_CHANGED = "priority_changed"
    DUE_DATE_CHANGED = "due_date_changed"

    ATTACHMENT_ADDED = "attachment_added"
    ATTACHMENT_REMOVED = "attachment_removed"
