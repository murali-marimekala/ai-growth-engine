"""
Data models for the AI/ML Career Coach application.
Defines core entities: Roadmap, Progress, Flashcards, Resources, and GitHub Projects.
"""

from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MilestoneStatus(Enum):
    """Status of a roadmap milestone."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ResourceStatus(Enum):
    """Status of a learning resource."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class DifficultyLevel(Enum):
    """Difficulty level of resources and topics."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CardStatus(Enum):
    """Status of a flashcard."""
    NEW = "new"
    REVIEWING = "reviewing"
    DIFFICULT = "difficult"
    MASTERED = "mastered"


class ProjectStatus(Enum):
    """Status of a GitHub project."""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class WeeklyTask:
    """A single task/milestone within a week."""
    task_id: str
    name: str
    description: str
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED
    priority: int = 1  # 1=high, 2=medium, 3=low


@dataclass
class Week:
    """A week of learning tasks."""
    week_num: int
    name: str
    description: str
    tasks: List[WeeklyTask] = field(default_factory=list)
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED


@dataclass
class Month:
    """A month containing weeks."""
    month_num: int
    name: str
    description: str
    weeks: List[Week] = field(default_factory=list)
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED


@dataclass
class Quarter:
    """A quarter containing months."""
    quarter_num: int
    name: str
    description: str
    focus_areas: List[str] = field(default_factory=list)
    months: List[Month] = field(default_factory=list)
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED


@dataclass
class Year:
    """A year-long roadmap with quarters."""
    year_num: int
    name: str
    description: str
    focus_areas: List[str] = field(default_factory=list)
    quarters: List[Quarter] = field(default_factory=list)
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED


@dataclass
class Roadmap:
    """Complete 2-year AI/ML career transition roadmap."""
    years: List[Year] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DailySession:
    """Log of a single day's learning/work."""
    date: str  # YYYY-MM-DD
    duration_hours: float
    topics_covered: List[str]
    resources_used: List[str]
    notes: str
    mood: Optional[str] = None  # e.g., "energized", "tired", "focused"
    session_id: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ProgressState:
    """Overall progress tracking across the journey."""
    daily_sessions: List[DailySession] = field(default_factory=list)
    current_streak: int = 0
    longest_streak: int = 0
    last_session_date: Optional[str] = None
    total_hours: float = 0.0
    completed_milestones: int = 0
    total_milestones: int = 0
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Resource:
    """A learning resource (course, article, video, etc.)."""
    resource_id: str
    title: str
    resource_type: str  # "course", "article", "video", "repo", "paper"
    url: str
    difficulty: DifficultyLevel
    description: str
    mapped_topics: List[str]  # e.g., ["Linear Algebra", "Python Basics"]
    status: ResourceStatus = ResourceStatus.TODO
    added_date: str = field(default_factory=lambda: datetime.now().isoformat())
    completion_date: Optional[str] = None
    notes: str = ""


@dataclass
class Flashcard:
    """A single flashcard."""
    card_id: str
    question: str
    answer: str
    topic: str
    status: CardStatus = CardStatus.NEW
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    review_count: int = 0
    last_reviewed: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    next_review: Optional[str] = None


@dataclass
class FlashcardDeck:
    """A collection of flashcards by topic."""
    deck_id: str
    topic: str
    description: str
    cards: List[Flashcard] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    total_reviews: int = 0


@dataclass
class GitHubProject:
    """A GitHub project in the user's portfolio."""
    project_id: str
    name: str
    repo_url: str
    description: str
    skills_covered: List[str]
    status: ProjectStatus = ProjectStatus.PLANNING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""
    has_readme: bool = False
    has_docs: bool = False
    has_tests: bool = False
    has_demo: bool = False
    blog_post_url: Optional[str] = None


@dataclass
class WeeklyTip:
    """A weekly coaching tip."""
    tip_id: str
    week: int
    category: str  # "learning_strategy", "time_management", "portfolio", "networking"
    title: str
    content: str
    source: str  # "template" or "openai"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AppState:
    """Root application state - top-level container."""
    roadmap: Roadmap
    progress: ProgressState
    resources: List[Resource] = field(default_factory=list)
    flashcard_decks: List[FlashcardDeck] = field(default_factory=list)
    github_projects: List[GitHubProject] = field(default_factory=list)
    weekly_tips: List[WeeklyTip] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
