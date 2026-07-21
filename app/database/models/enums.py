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
    # Task
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"

    # Assignment
    TASK_ASSIGNED = "task_assigned"

    # Phase
    PHASE_CHANGED = "status_changed"

    # Priority
    PRIORITY_CHANGED = "priority_changed"

    # Due Date
    DUE_DATE_CHANGED = "due_date_changed"

    # Comments
    COMMENT_ADDED = "comment_added"
    COMMENT_UPDATED = "comment_updated"

    # Task Attachments
    TASK_ATTACHMENT_ADDED = "task_attachment_added"
    COMMENT_ATTACHMENT_ADDED = "comment_attachment_added"
    ATTACHMENT_REMOVED = "task_attachment_removed"



class ProjectStatus(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"