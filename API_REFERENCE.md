"""
API REFERENCE - AI Growth Engine Modules
Complete documentation of all classes and methods.
"""

# ============================================================================
# MODELS (models.py)
# ============================================================================

"""
Data models representing core entities:

Classes:
--------

MilestoneStatus (Enum)
  Values: NOT_STARTED, IN_PROGRESS, COMPLETED

ResourceStatus (Enum)
  Values: TODO, IN_PROGRESS, COMPLETED

DifficultyLevel (Enum)
  Values: BEGINNER, INTERMEDIATE, ADVANCED

CardStatus (Enum)
  Values: NEW, REVIEWING, DIFFICULT, MASTERED

ProjectStatus (Enum)
  Values: PLANNING, IN_PROGRESS, COMPLETED

Year
  year_num: int
  name: str
  description: str
  focus_areas: List[str]
  quarters: List[Quarter]
  status: MilestoneStatus

Quarter
  quarter_num: int
  name: str
  description: str
  focus_areas: List[str]
  months: List[Month]
  status: MilestoneStatus

Month
  month_num: int
  name: str
  description: str
  weeks: List[Week]
  status: MilestoneStatus

Week
  week_num: int
  name: str
  description: str
  tasks: List[WeeklyTask]
  status: MilestoneStatus

WeeklyTask
  task_id: str
  name: str
  description: str
  status: MilestoneStatus
  priority: int (1=high, 2=medium, 3=low)

Roadmap
  years: List[Year]
  created_at: str (ISO datetime)
  last_updated: str (ISO datetime)

DailySession
  date: str (YYYY-MM-DD)
  duration_hours: float
  topics_covered: List[str]
  resources_used: List[str]
  notes: str
  mood: Optional[str]

ProgressState
  daily_sessions: List[DailySession]
  current_streak: int
  longest_streak: int
  last_session_date: Optional[str]
  total_hours: float
  completed_milestones: int
  total_milestones: int

Resource
  resource_id: str
  title: str
  resource_type: str (course, article, video, repo, paper)
  url: str
  difficulty: DifficultyLevel
  description: str
  mapped_topics: List[str]
  status: ResourceStatus
  added_date: str (ISO datetime)
  completion_date: Optional[str]
  notes: str

Flashcard
  card_id: str
  question: str
  answer: str
  topic: str
  status: CardStatus
  difficulty: DifficultyLevel
  review_count: int
  last_reviewed: Optional[str] (ISO datetime)
  created_at: str (ISO datetime)
  next_review: Optional[str] (ISO datetime)

FlashcardDeck
  deck_id: str
  topic: str
  description: str
  cards: List[Flashcard]
  created_at: str (ISO datetime)
  total_reviews: int

GitHubProject
  project_id: str
  name: str
  repo_url: str
  description: str
  skills_covered: List[str]
  status: ProjectStatus
  created_at: str (ISO datetime)
  last_updated: str (ISO datetime)
  notes: str
  has_readme: bool
  has_docs: bool
  has_tests: bool
  has_demo: bool
  blog_post_url: Optional[str]

WeeklyTip
  tip_id: str
  week: int
  category: str (learning_strategy, time_management, portfolio, networking)
  title: str
  content: str
  source: str (template or openai)
  created_at: str (ISO datetime)

AppState
  roadmap: Roadmap
  progress: ProgressState
  resources: List[Resource]
  flashcard_decks: List[FlashcardDeck]
  github_projects: List[GitHubProject]
  weekly_tips: List[WeeklyTip]
  last_updated: str (ISO datetime)
"""

# ============================================================================
# PERSISTENCE (persistence.py)
# ============================================================================

"""
StorageManager
--------------

Methods:

load_state() -> AppState
  Load application state from data/app_state.json
  Returns fresh state if file doesn't exist
  
save_state(state: AppState) -> None
  Save current state to JSON
  Updates last_updated timestamp

Example Usage:
  storage = StorageManager("data")
  state = storage.load_state()
  # Modify state...
  storage.save_state(state)
"""

# ============================================================================
# BUSINESS LOGIC (business_logic.py)
# ============================================================================

"""
RoadmapManager
--------------
Manages roadmap navigation and milestone tracking.

Methods:

get_roadmap_summary() -> str
  Return formatted string of entire roadmap
  
get_current_focus() -> Dict[str, Any]
  Return current learning phase:
    {
      "year": str,
      "quarter": str,
      "month": str,
      "week": str,
      "tasks": List[str]
    }
  
mark_task_complete(task_id: str) -> bool
  Mark a task as complete
  Automatically updates parent completion status
  Returns True if successful
  
get_upcoming_tasks(days_ahead: int = 7) -> List[str]
  Return list of next 5 upcoming tasks


ProgressManager
---------------
Tracks daily learning progress.

Methods:

log_session(
  duration_hours: float,
  topics: List[str],
  resources: List[str],
  notes: str = "",
  mood: str = None
) -> DailySession
  Log a learning session
  Auto-updates streak and total hours
  
get_progress_summary() -> str
  Return formatted progress summary
  Shows stats, recent sessions, streaks
  
get_weekly_summary() -> str
  Return this week's summary
  Shows session count, hours, topics


ResourceManager
---------------
Manages learning resources.

Methods:

add_resource(
  title: str,
  resource_type: str,
  url: str,
  difficulty: DifficultyLevel,
  description: str,
  topics: List[str]
) -> Resource
  Create and add new resource
  
mark_resource_status(
  resource_id: str,
  status: ResourceStatus
) -> bool
  Update resource status
  
get_resources_by_topic(topic: str) -> List[Resource]
  Return all resources for a topic
  
get_resources_summary() -> str
  Return formatted resources overview


FlashcardManager
----------------
Manages flashcard learning.

Methods:

create_deck(topic: str, description: str) -> FlashcardDeck
  Create new flashcard deck
  
add_card(
  deck_id: str,
  question: str,
  answer: str,
  difficulty: DifficultyLevel = BEGINNER
) -> Optional[Flashcard]
  Add card to deck
  Returns None if deck not found
  
get_cards_for_review(num_cards: int = 10) -> List[Flashcard]
  Get cards due for review
  Uses spaced repetition scheduling
  
mark_card_review(card_id: str, result: str) -> bool
  Mark card as reviewed
  result: "easy", "hard", "difficult", or "mastered"
  Schedules next review based on result
  
get_flashcard_stats() -> str
  Return formatted flashcard statistics


GitHubProjectManager
---------------------
Manages portfolio projects.

Methods:

add_project(
  name: str,
  repo_url: str,
  description: str,
  skills: List[str]
) -> GitHubProject
  Create and add new project
  
update_project_status(
  project_id: str,
  status: ProjectStatus
) -> bool
  Update project status
  
add_project_feature(
  project_id: str,
  feature: str,
  value: bool
) -> bool
  Mark feature complete
  Features: "has_readme", "has_docs", "has_tests", "has_demo"
  
get_portfolio_summary() -> str
  Return formatted portfolio overview
  Shows projects and improvement suggestions


CoachingTipsManager
--------------------
Generates coaching advice.

Methods:

generate_weekly_tips(
  week_num: int,
  current_focus: str
) -> List[WeeklyTip]
  Generate weekly tips for 4 categories:
  - learning_strategy
  - time_management
  - portfolio
  - networking
  
get_weekly_tips_summary() -> str
  Return formatted weekly tips
"""

# ============================================================================
# AI COACH (ai_coach.py)
# ============================================================================

"""
AICoach
-------
Optional OpenAI-powered personalization.

Methods:

__init__()
  Initialize AI Coach
  Reads OPENAI_API_KEY from .env
  Sets enabled=True if key found
  
analyze_progress(
  sessions_summary: str,
  current_focus: str
) -> Optional[str]
  Analyze progress and provide insights
  Returns None if API not available
  
generate_personalized_tips(
  progress_data: Dict
) -> Optional[str]
  Generate personalized tips based on data
  
suggest_resources(
  topic: str,
  difficulty: str,
  learning_style: str = "mixed"
) -> Optional[str]
  Suggest free/low-cost resources
  
generate_flashcards(
  topic: str,
  num_cards: int = 5
) -> Optional[List[Dict[str, str]]]
  Auto-generate flashcard questions/answers
  Returns list of {question, answer} dicts
  
interview_prep(
  role_level: str = "mid-level",
  company: str = "top-tier"
) -> Optional[str]
  Generate interview preparation advice
  
get_status_message() -> str
  Return status: enabled or disabled with reason
"""

# ============================================================================
# CLI (coach.py)
# ============================================================================

"""
CareerCoach (Main Application)
-------------------------------

Usage:
  python coach.py <command> [options]

Core Commands:

ROADMAP & PROGRESS:
  roadmap                    Show 2-year learning roadmap
  status                     Show current progress stats
  focus                      Show current learning focus
  tasks                      Show upcoming tasks
  mark-task <task_id>        Mark task as complete
  progress                   Detailed progress summary
  week                       This week's summary

SESSIONS:
  log <hours> <topics>       Log learning session
    Example: log 2.5 "Python,Linear_Algebra"

RESOURCES:
  resources                  Show all resources
  add-resource <type> <title> <url> [difficulty] [topics]
    Types: course, video, article, paper, repo
  resource-status <id> <status>
    Status: todo, in_progress, completed

FLASHCARDS:
  flashcards                 Show flashcard stats
  create-deck <topic> [description]  Create deck
  add-card <deck_id> <q> <a>          Add card
  review [num_cards]         Review cards (interactive)

PROJECTS:
  projects                   Show portfolio
  add-project <name> <url> <desc> [skills]
  update-project <id> <status>
    Status: planning, in_progress, completed
  add-feature <id> <feature>
    Features: readme, docs, tests, demo

COACHING:
  tips                       Show weekly tips
  generate-tips              Generate tips
  interview                  Interview prep (AI)
  suggest <topic> [difficulty]  Resources (AI)

OTHER:
  help                       Show this help
"""

# ============================================================================
# QUICK REFERENCE - COMMON WORKFLOWS
# ============================================================================

"""
DAILY WORKFLOW:
===============

1. Check current focus:
   python coach.py focus

2. Do flashcard review:
   python coach.py review 10

3. Log learning session:
   python coach.py log 1.5 "Python,ML"

4. Update progress:
   python coach.py progress


WEEKLY WORKFLOW:
================

1. View week summary:
   python coach.py week

2. Generate tips:
   python coach.py generate-tips

3. Review/update resources:
   python coach.py resources

4. Check upcoming:
   python coach.py tasks


PROJECT WORKFLOW:
=================

1. Add new project:
   python coach.py add-project "Name" "URL" "Desc" "Skills"

2. Mark status:
   python coach.py update-project <id> in_progress

3. Add features:
   python coach.py add-feature <id> readme
   python coach.py add-feature <id> tests
   python coach.py add-feature <id> demo

4. Complete:
   python coach.py update-project <id> completed


FLASHCARD WORKFLOW:
===================

1. Create deck:
   python coach.py create-deck "Topic" "Description"

2. Add cards:
   python coach.py add-card <deck_id> "Question?" "Answer"

3. Review (interactive):
   python coach.py review 15

4. Check stats:
   python coach.py flashcards
"""

# ============================================================================
# CONFIGURATION
# ============================================================================

"""
Environment Variables (.env file):
===================================

OPENAI_API_KEY=sk-...
  Optional. Required for AI-powered features.
  Get from: https://platform.openai.com/api-keys

Data Files (data/ directory):
=============================

app_state.json
  Contains all application state:
  - Roadmap with all milestones
  - Progress tracking
  - Resources
  - Flashcards
  - Projects
  - Tips

Structure is automatically created. No manual setup needed.
"""

# ============================================================================
# ERROR HANDLING
# ============================================================================

"""
Common Issues:
==============

ModuleNotFoundError: No module named 'models'
  → Make sure you're in the project directory
  → python coach.py (from project root)

OpenAI API errors
  → Check OPENAI_API_KEY in .env
  → Verify API key format (starts with sk-)
  → Check account has credits

Data not persisting
  → Verify data/ directory has write permissions
  → Check app_state.json exists
  → Try: python -c "from persistence import StorageManager; s = StorageManager(); print(s.state_file)"

Streak not updating
  → Ensure you log session with today's date
  → Check system date/time is correct
  → Use: python coach.py progress to verify

Task ID not found
  → Get task ID from: python coach.py focus or python coach.py tasks
  → Copy exact task_id value
  → Try: python coach.py mark-task w1_t1
"""

print("✓ API Reference loaded. See docstring for complete reference.")
