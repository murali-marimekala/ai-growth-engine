"""
Persistence layer for the AI Coach application.
Handles JSON serialization/deserialization of application state.
"""

import json
import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from models import (
    AppState, Roadmap, ProgressState, Resource, Flashcard, FlashcardDeck,
    GitHubProject, WeeklyTip, DailySession, Year, Quarter, Month, Week, WeeklyTask,
    MilestoneStatus, ResourceStatus, DifficultyLevel, CardStatus, ProjectStatus
)


class StorageManager:
    """Manages persistence of application state to JSON files."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.state_file = self.data_dir / "app_state.json"
    
    def load_state(self) -> AppState:
        """Load application state from disk. Return empty state if not found."""
        if not self.state_file.exists():
            return self._create_default_state()
        
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
            return self._deserialize_state(data)
        except Exception as e:
            print(f"Error loading state: {e}. Creating fresh state.")
            return self._create_default_state()
    
    def save_state(self, state: AppState) -> None:
        """Save application state to disk."""
        try:
            data = self._serialize_state(state)
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def _create_default_state(self) -> AppState:
        """Create a fresh application state with default roadmap."""
        return AppState(
            roadmap=self._create_default_roadmap(),
            progress=ProgressState(),
            resources=[],
            flashcard_decks=[],
            github_projects=[],
            weekly_tips=[]
        )
    
    def _create_default_roadmap(self) -> Roadmap:
        """Create a comprehensive 2-year AI/ML roadmap."""
        roadmap = Roadmap()
        
        # YEAR 1: FOUNDATIONS
        year1 = Year(
            year_num=1,
            name="Year 1: AI/ML Foundations",
            description="Master fundamentals: Python, Math, Classical ML, Basic Deep Learning",
            focus_areas=["Python Programming", "Mathematics for ML", "Classical ML", "Deep Learning Basics", "Portfolio Start"],
        )
        
        # Q1: Python & Math Foundations
        q1 = Quarter(
            quarter_num=1,
            name="Q1: Python & Math Foundations",
            description="Build solid programming and mathematical foundation",
            focus_areas=["Python", "Linear Algebra", "Calculus", "Probability & Statistics"]
        )
        
        # Q1 Months
        m1_1 = Month(month_num=1, name="Python Essentials", description="Master Python for ML")
        m1_1.weeks = [
            Week(1, "Setup & Basics", "Environment setup, syntax, OOP concepts", [
                WeeklyTask("w1_t1", "Install Python & tools", "Set up environment, Jupyter, git"),
                WeeklyTask("w1_t2", "Python basics", "Variables, control flow, functions"),
                WeeklyTask("w1_t3", "OOP fundamentals", "Classes, inheritance, polymorphism"),
            ]),
            Week(2, "Libraries & Data", "NumPy, Pandas fundamentals", [
                WeeklyTask("w2_t1", "NumPy fundamentals", "Arrays, operations, broadcasting"),
                WeeklyTask("w2_t2", "Pandas basics", "DataFrames, indexing, groupby"),
                WeeklyTask("w2_t3", "Data visualization", "Matplotlib, Seaborn basics"),
            ]),
            Week(3, "Advanced Python", "Functional programming, testing", [
                WeeklyTask("w3_t1", "Functional programming", "Lambda, map, filter, comprehensions"),
                WeeklyTask("w3_t2", "Testing & debugging", "Unit tests with pytest"),
                WeeklyTask("w3_t3", "Code quality", "Linting, formatting, documentation"),
            ]),
            Week(4, "Python Project", "Small project exercise", [
                WeeklyTask("w4_t1", "Project planning", "Design simple data tool"),
                WeeklyTask("w4_t2", "Implementation", "Build & test"),
                WeeklyTask("w4_t3", "Documentation", "README, comments, examples"),
            ]),
        ]
        
        m1_2 = Month(month_num=2, name="Linear Algebra", description="Mathematical foundation for ML")
        m1_2.weeks = [
            Week(1, "Vectors & Matrices", "Core concepts", [
                WeeklyTask("v1_t1", "Vector operations", "Dot product, norms, angles"),
                WeeklyTask("v1_t2", "Matrix operations", "Multiplication, transpose, rank"),
            ]),
            Week(2, "Decompositions", "Eigenvalues, SVD", [
                WeeklyTask("v2_t1", "Eigenvalues/eigenvectors", "Understanding spectral decomposition"),
                WeeklyTask("v2_t2", "SVD & applications", "Dimensionality reduction"),
            ]),
            Week(3, "Advanced Topics", "Norms, distances, projections", [
                WeeklyTask("v3_t1", "Norms & distances", "L1, L2, Euclidean"),
                WeeklyTask("v3_t2", "Linear transformations", "Projections and rotations"),
            ]),
            Week(4, "LA for ML", "Practical applications", [
                WeeklyTask("v4_t1", "LA in ML", "Covariance, PCA concepts"),
            ]),
        ]
        
        m1_3 = Month(month_num=3, name="Calculus & Probability", description="Optimization and uncertainty")
        m1_3.weeks = [
            Week(1, "Single Variable Calculus", "Derivatives, optimization", [
                WeeklyTask("c1_t1", "Derivatives", "Limits, definition, rules"),
                WeeklyTask("c1_t2", "Optimization", "Critical points, gradients"),
            ]),
            Week(2, "Multivariable Calculus", "Gradients, Hessians", [
                WeeklyTask("c2_t1", "Partial derivatives", "Multivariable chain rule"),
                WeeklyTask("c2_t2", "Optimization", "Gradient descent intuition"),
            ]),
            Week(3, "Probability Fundamentals", "Distributions, independence", [
                WeeklyTask("c3_t1", "Basic probability", "Rules, conditional probability"),
                WeeklyTask("c3_t2", "Distributions", "Normal, exponential, Poisson"),
            ]),
            Week(4, "Statistics Essentials", "Hypothesis testing, estimation", [
                WeeklyTask("c4_t1", "Descriptive statistics", "Mean, variance, correlation"),
                WeeklyTask("c4_t2", "Inference basics", "Hypothesis testing concepts"),
            ]),
        ]
        
        q1.months = [m1_1, m1_2, m1_3]
        
        # Q2: Classical ML Fundamentals
        q2 = Quarter(
            quarter_num=2,
            name="Q2: Classical ML Fundamentals",
            description="Regression, classification, and evaluation",
            focus_areas=["Regression", "Classification", "Evaluation Metrics", "Feature Engineering"]
        )
        
        m2_1 = Month(month_num=1, name="Regression & Linear Models", description="Linear & logistic regression")
        m2_1.weeks = [
            Week(1, "Linear Regression", "Theory and practice", [
                WeeklyTask("lr1", "Linear regression theory", "OLS, assumptions, diagnostics"),
                WeeklyTask("lr2", "Scikit-learn usage", "Fit, predict, evaluate"),
                WeeklyTask("lr3", "Regularization", "Ridge, Lasso, ElasticNet"),
            ]),
            Week(2, "Logistic Regression", "Binary and multiclass", [
                WeeklyTask("log1", "Logistic regression", "Sigmoid, cross-entropy loss"),
                WeeklyTask("log2", "Binary classification", "Decision boundaries"),
                WeeklyTask("log3", "Multiclass methods", "One-vs-Rest, multinomial"),
            ]),
            Week(3, "Feature Engineering", "Preprocessing and selection", [
                WeeklyTask("fe1", "Feature scaling", "Normalization, standardization"),
                WeeklyTask("fe2", "Feature selection", "Univariate, recursive, model-based"),
                WeeklyTask("fe3", "Handling missing data", "Imputation strategies"),
            ]),
            Week(4, "Evaluation Metrics", "Measuring model performance", [
                WeeklyTask("em1", "Regression metrics", "MSE, R², MAE"),
                WeeklyTask("em2", "Classification metrics", "Accuracy, precision, recall, F1, AUC"),
            ]),
        ]
        q2.months = [m2_1]  # Simplified for brevity
        
        # Q3-Q4 simplified structure
        q3 = Quarter(
            quarter_num=3,
            name="Q3: Advanced Classical ML",
            description="Tree-based methods, ensembles, clustering",
            focus_areas=["Decision Trees", "Ensemble Methods", "Clustering", "Dimensionality Reduction"]
        )
        
        q4 = Quarter(
            quarter_num=4,
            name="Q4: Deep Learning Basics & Portfolio",
            description="Neural networks and first major project",
            focus_areas=["Neural Network Basics", "CNNs", "RNNs", "First Portfolio Project"]
        )
        
        year1.quarters = [q1, q2, q3, q4]
        
        # YEAR 2: ADVANCED AI/ML
        year2 = Year(
            year_num=2,
            name="Year 2: Advanced AI/ML & Specialization",
            description="LLMs, GenAI, MLOps, System Design, Specialization",
            focus_areas=["Transformers & LLMs", "MLOps & Deployment", "System Design", "Specialization Domains", "Advanced Portfolio"],
        )
        
        q5 = Quarter(
            quarter_num=1,
            name="Q1: Transformers & LLMs",
            description="Attention, transformers, and large language models",
            focus_areas=["Attention Mechanism", "Transformer Architecture", "Pre-trained LLMs", "Fine-tuning"]
        )
        
        q6 = Quarter(
            quarter_num=2,
            name="Q2: GenAI & RAG",
            description="Generative AI, prompt engineering, RAG systems",
            focus_areas=["Prompt Engineering", "RAG Systems", "Vector Databases", "GenAI Applications"]
        )
        
        q7 = Quarter(
            quarter_num=3,
            name="Q3: MLOps & System Design",
            description="Production ML, deployment, and system design",
            focus_areas=["ML Pipeline Design", "Model Serving", "Monitoring", "Scalability"]
        )
        
        q8 = Quarter(
            quarter_num=4,
            name="Q4: Interview Prep & Portfolio Polish",
            description="Final preparation for target roles",
            focus_areas=["System Design Interviews", "ML Design Questions", "Portfolio Review", "Networking"]
        )
        
        year2.quarters = [q5, q6, q7, q8]
        
        roadmap.years = [year1, year2]
        return roadmap
    
    @staticmethod
    def _serialize_state(state: AppState) -> dict:
        """Convert AppState to serializable dict."""
        return {
            "roadmap": StorageManager._serialize_roadmap(state.roadmap),
            "progress": StorageManager._serialize_progress(state.progress),
            "resources": [StorageManager._serialize_resource(r) for r in state.resources],
            "flashcard_decks": [StorageManager._serialize_deck(d) for d in state.flashcard_decks],
            "github_projects": [StorageManager._serialize_project(p) for p in state.github_projects],
            "weekly_tips": [StorageManager._serialize_tip(t) for t in state.weekly_tips],
            "last_updated": state.last_updated,
        }
    
    @staticmethod
    def _serialize_roadmap(roadmap: Roadmap) -> dict:
        """Serialize roadmap structure."""
        return {
            "years": [{
                "year_num": y.year_num,
                "name": y.name,
                "description": y.description,
                "focus_areas": y.focus_areas,
                "status": y.status.value,
                "quarters": [{
                    "quarter_num": q.quarter_num,
                    "name": q.name,
                    "description": q.description,
                    "focus_areas": q.focus_areas,
                    "status": q.status.value,
                    "months": [{
                        "month_num": m.month_num,
                        "name": m.name,
                        "description": m.description,
                        "status": m.status.value,
                        "weeks": [{
                            "week_num": w.week_num,
                            "name": w.name,
                            "description": w.description,
                            "status": w.status.value,
                            "tasks": [{
                                "task_id": t.task_id,
                                "name": t.name,
                                "description": t.description,
                                "status": t.status.value,
                                "priority": t.priority,
                            } for t in w.tasks]
                        } for w in m.weeks]
                    } for m in q.months]
                } for q in y.quarters]
            } for y in roadmap.years],
            "created_at": roadmap.created_at,
            "last_updated": roadmap.last_updated,
        }
    
    @staticmethod
    def _serialize_progress(progress: ProgressState) -> dict:
        """Serialize progress state."""
        return {
            "daily_sessions": [{
                "date": s.date,
                "duration_hours": s.duration_hours,
                "topics_covered": s.topics_covered,
                "resources_used": s.resources_used,
                "notes": s.notes,
                "mood": s.mood,
                "session_id": s.session_id,
            } for s in progress.daily_sessions],
            "current_streak": progress.current_streak,
            "longest_streak": progress.longest_streak,
            "last_session_date": progress.last_session_date,
            "total_hours": progress.total_hours,
            "completed_milestones": progress.completed_milestones,
            "total_milestones": progress.total_milestones,
            "updated_at": progress.updated_at,
        }
    
    @staticmethod
    def _serialize_resource(resource: Resource) -> dict:
        """Serialize a learning resource."""
        return {
            "resource_id": resource.resource_id,
            "title": resource.title,
            "resource_type": resource.resource_type,
            "url": resource.url,
            "difficulty": resource.difficulty.value,
            "description": resource.description,
            "mapped_topics": resource.mapped_topics,
            "status": resource.status.value,
            "added_date": resource.added_date,
            "completion_date": resource.completion_date,
            "notes": resource.notes,
        }
    
    @staticmethod
    def _serialize_deck(deck: FlashcardDeck) -> dict:
        """Serialize a flashcard deck."""
        return {
            "deck_id": deck.deck_id,
            "topic": deck.topic,
            "description": deck.description,
            "cards": [{
                "card_id": c.card_id,
                "question": c.question,
                "answer": c.answer,
                "topic": c.topic,
                "status": c.status.value,
                "difficulty": c.difficulty.value,
                "review_count": c.review_count,
                "last_reviewed": c.last_reviewed,
                "created_at": c.created_at,
                "next_review": c.next_review,
            } for c in deck.cards],
            "created_at": deck.created_at,
            "total_reviews": deck.total_reviews,
        }
    
    @staticmethod
    def _serialize_project(project: GitHubProject) -> dict:
        """Serialize a GitHub project."""
        return {
            "project_id": project.project_id,
            "name": project.name,
            "repo_url": project.repo_url,
            "description": project.description,
            "skills_covered": project.skills_covered,
            "status": project.status.value,
            "created_at": project.created_at,
            "last_updated": project.last_updated,
            "notes": project.notes,
            "has_readme": project.has_readme,
            "has_docs": project.has_docs,
            "has_tests": project.has_tests,
            "has_demo": project.has_demo,
            "blog_post_url": project.blog_post_url,
        }
    
    @staticmethod
    def _serialize_tip(tip: WeeklyTip) -> dict:
        """Serialize a weekly tip."""
        return {
            "tip_id": tip.tip_id,
            "week": tip.week,
            "category": tip.category,
            "title": tip.title,
            "content": tip.content,
            "source": tip.source,
            "created_at": tip.created_at,
        }
    
    @staticmethod
    def _deserialize_state(data: dict) -> AppState:
        """Convert dict back to AppState."""
        roadmap = StorageManager._deserialize_roadmap(data.get("roadmap", {}))
        progress = StorageManager._deserialize_progress(data.get("progress", {}))
        resources = [StorageManager._deserialize_resource(r) for r in data.get("resources", [])]
        decks = [StorageManager._deserialize_deck(d) for d in data.get("flashcard_decks", [])]
        projects = [StorageManager._deserialize_project(p) for p in data.get("github_projects", [])]
        tips = [StorageManager._deserialize_tip(t) for t in data.get("weekly_tips", [])]
        
        return AppState(
            roadmap=roadmap,
            progress=progress,
            resources=resources,
            flashcard_decks=decks,
            github_projects=projects,
            weekly_tips=tips,
            last_updated=data.get("last_updated", datetime.now().isoformat()),
        )
    
    @staticmethod
    def _deserialize_roadmap(data: dict) -> Roadmap:
        """Deserialize roadmap structure."""
        years = []
        for y_data in data.get("years", []):
            quarters = []
            for q_data in y_data.get("quarters", []):
                months = []
                for m_data in q_data.get("months", []):
                    weeks = []
                    for w_data in m_data.get("weeks", []):
                        tasks = [
                            WeeklyTask(
                                task_id=t["task_id"],
                                name=t["name"],
                                description=t["description"],
                                status=MilestoneStatus(t.get("status", "not_started")),
                                priority=t.get("priority", 1),
                            )
                            for t in w_data.get("tasks", [])
                        ]
                        weeks.append(Week(
                            week_num=w_data["week_num"],
                            name=w_data["name"],
                            description=w_data["description"],
                            tasks=tasks,
                            status=MilestoneStatus(w_data.get("status", "not_started")),
                        ))
                    months.append(Month(
                        month_num=m_data["month_num"],
                        name=m_data["name"],
                        description=m_data["description"],
                        weeks=weeks,
                        status=MilestoneStatus(m_data.get("status", "not_started")),
                    ))
                quarters.append(Quarter(
                    quarter_num=q_data["quarter_num"],
                    name=q_data["name"],
                    description=q_data["description"],
                    focus_areas=q_data.get("focus_areas", []),
                    months=months,
                    status=MilestoneStatus(q_data.get("status", "not_started")),
                ))
            years.append(Year(
                year_num=y_data["year_num"],
                name=y_data["name"],
                description=y_data["description"],
                focus_areas=y_data.get("focus_areas", []),
                quarters=quarters,
                status=MilestoneStatus(y_data.get("status", "not_started")),
            ))
        
        return Roadmap(
            years=years,
            created_at=data.get("created_at", datetime.now().isoformat()),
            last_updated=data.get("last_updated", datetime.now().isoformat()),
        )
    
    @staticmethod
    def _deserialize_progress(data: dict) -> ProgressState:
        """Deserialize progress state."""
        sessions = [
            DailySession(
                date=s["date"],
                duration_hours=s["duration_hours"],
                topics_covered=s["topics_covered"],
                resources_used=s["resources_used"],
                notes=s["notes"],
                mood=s.get("mood"),
                session_id=s.get("session_id", datetime.now().isoformat()),
            )
            for s in data.get("daily_sessions", [])
        ]
        
        return ProgressState(
            daily_sessions=sessions,
            current_streak=data.get("current_streak", 0),
            longest_streak=data.get("longest_streak", 0),
            last_session_date=data.get("last_session_date"),
            total_hours=data.get("total_hours", 0.0),
            completed_milestones=data.get("completed_milestones", 0),
            total_milestones=data.get("total_milestones", 0),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
        )
    
    @staticmethod
    def _deserialize_resource(data: dict) -> Resource:
        """Deserialize a learning resource."""
        return Resource(
            resource_id=data["resource_id"],
            title=data["title"],
            resource_type=data["resource_type"],
            url=data["url"],
            difficulty=DifficultyLevel(data["difficulty"]),
            description=data["description"],
            mapped_topics=data["mapped_topics"],
            status=ResourceStatus(data.get("status", "todo")),
            added_date=data.get("added_date", datetime.now().isoformat()),
            completion_date=data.get("completion_date"),
            notes=data.get("notes", ""),
        )
    
    @staticmethod
    def _deserialize_deck(data: dict) -> FlashcardDeck:
        """Deserialize a flashcard deck."""
        cards = [
            Flashcard(
                card_id=c["card_id"],
                question=c["question"],
                answer=c["answer"],
                topic=c["topic"],
                status=CardStatus(c.get("status", "new")),
                difficulty=DifficultyLevel(c.get("difficulty", "beginner")),
                review_count=c.get("review_count", 0),
                last_reviewed=c.get("last_reviewed"),
                created_at=c.get("created_at", datetime.now().isoformat()),
                next_review=c.get("next_review"),
            )
            for c in data.get("cards", [])
        ]
        
        return FlashcardDeck(
            deck_id=data["deck_id"],
            topic=data["topic"],
            description=data["description"],
            cards=cards,
            created_at=data.get("created_at", datetime.now().isoformat()),
            total_reviews=data.get("total_reviews", 0),
        )
    
    @staticmethod
    def _deserialize_project(data: dict) -> GitHubProject:
        """Deserialize a GitHub project."""
        return GitHubProject(
            project_id=data["project_id"],
            name=data["name"],
            repo_url=data["repo_url"],
            description=data["description"],
            skills_covered=data["skills_covered"],
            status=ProjectStatus(data.get("status", "planning")),
            created_at=data.get("created_at", datetime.now().isoformat()),
            last_updated=data.get("last_updated", datetime.now().isoformat()),
            notes=data.get("notes", ""),
            has_readme=data.get("has_readme", False),
            has_docs=data.get("has_docs", False),
            has_tests=data.get("has_tests", False),
            has_demo=data.get("has_demo", False),
            blog_post_url=data.get("blog_post_url"),
        )
    
    @staticmethod
    def _deserialize_tip(data: dict) -> WeeklyTip:
        """Deserialize a weekly tip."""
        return WeeklyTip(
            tip_id=data["tip_id"],
            week=data["week"],
            category=data["category"],
            title=data["title"],
            content=data["content"],
            source=data.get("source", "template"),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )
