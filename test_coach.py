"""
Test suite for the AI Growth Engine application.
Run with: python -m pytest test_coach.py -v
"""

import sys
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import (
    DifficultyLevel, MilestoneStatus, ResourceStatus, 
    CardStatus, ProjectStatus, Roadmap, ProgressState,
    Year, Quarter, Month, Week, WeeklyTask
)
from persistence import StorageManager
from business_logic import (
    RoadmapManager, ProgressManager, ResourceManager,
    FlashcardManager, GitHubProjectManager, CoachingTipsManager
)


class TestRoadmapManager:
    """Test roadmap functionality."""
    
    def setup_method(self):
        """Create fresh roadmap for each test."""
        self.roadmap = StorageManager()._create_default_roadmap()
        self.manager = RoadmapManager(self.roadmap)
    
    def test_roadmap_creation(self):
        """Test that roadmap is created correctly."""
        assert len(self.roadmap.years) == 2
        assert self.roadmap.years[0].year_num == 1
        assert self.roadmap.years[1].year_num == 2
    
    def test_roadmap_structure(self):
        """Test roadmap hierarchy."""
        year = self.roadmap.years[0]
        assert len(year.quarters) > 0
        
        quarter = year.quarters[0]
        assert len(quarter.months) > 0
        
        month = quarter.months[0]
        assert len(month.weeks) > 0
        
        week = month.weeks[0]
        assert len(week.tasks) > 0
    
    def test_get_current_focus(self):
        """Test current focus retrieval."""
        focus = self.manager.get_current_focus()
        assert "year" in focus
        assert "quarter" in focus or "message" in focus
    
    def test_mark_task_complete(self):
        """Test marking task as complete."""
        task_id = self.roadmap.years[0].quarters[0].months[0].weeks[0].tasks[0].task_id
        
        assert self.manager.mark_task_complete(task_id)
        
        # Check status updated
        task = self.roadmap.years[0].quarters[0].months[0].weeks[0].tasks[0]
        assert task.status == MilestoneStatus.COMPLETED
    
    def test_completion_percentage(self):
        """Test completion calculation."""
        # No tasks complete
        completion = self.manager._calculate_completion(self.roadmap.years[0])
        assert completion == 0
        
        # Mark one task complete
        task_id = self.roadmap.years[0].quarters[0].months[0].weeks[0].tasks[0].task_id
        self.manager.mark_task_complete(task_id)
        
        # Completion should be > 0
        completion = self.manager._calculate_completion(self.roadmap.years[0])
        assert completion > 0


class TestProgressManager:
    """Test progress tracking functionality."""
    
    def setup_method(self):
        """Create fresh progress for each test."""
        self.progress = ProgressState()
        self.manager = ProgressManager(self.progress)
    
    def test_log_session(self):
        """Test logging a learning session."""
        session = self.manager.log_session(
            duration_hours=2.5,
            topics=["Python", "Linear Algebra"],
            resources=["Video", "Article"],
            notes="Good progress",
            mood="energized"
        )
        
        assert session.duration_hours == 2.5
        assert "Python" in session.topics_covered
        assert self.manager.progress.total_hours == 2.5
    
    def test_multiple_sessions(self):
        """Test logging multiple sessions."""
        self.manager.log_session(2.0, ["Python"], ["Video"])
        self.manager.log_session(1.5, ["Math"], ["Article"])
        self.manager.log_session(2.5, ["Python"], ["Practice"])
        
        assert len(self.manager.progress.daily_sessions) == 3
        assert self.manager.progress.total_hours == 6.0
    
    def test_streak_calculation(self):
        """Test streak calculation."""
        today = datetime.now()
        
        # Log sessions for 3 consecutive days
        for i in range(3):
            session_date = (today - timedelta(days=2-i)).strftime("%Y-%m-%d")
            self.progress.daily_sessions.append(
                __import__('models').DailySession(
                    date=session_date,
                    duration_hours=1.5,
                    topics_covered=["Test"],
                    resources_used=[],
                    notes=""
                )
            )
        
        self.manager._update_streak()
        assert self.manager.progress.current_streak == 3


class TestResourceManager:
    """Test resource management."""
    
    def setup_method(self):
        """Create fresh resource manager."""
        from models import Resource
        self.resources = []
        self.manager = ResourceManager(self.resources)
    
    def test_add_resource(self):
        """Test adding a resource."""
        resource = self.manager.add_resource(
            title="Linear Algebra Course",
            resource_type="course",
            url="https://example.com",
            difficulty=DifficultyLevel.BEGINNER,
            description="Learn linear algebra",
            topics=["Math", "Linear Algebra"]
        )
        
        assert resource.title == "Linear Algebra Course"
        assert len(self.manager.resources) == 1
    
    def test_mark_resource_status(self):
        """Test updating resource status."""
        resource = self.manager.add_resource(
            title="Test Resource",
            resource_type="video",
            url="https://example.com",
            difficulty=DifficultyLevel.INTERMEDIATE,
            description="Test",
            topics=["Test"]
        )
        
        assert self.manager.mark_resource_status(resource.resource_id, ResourceStatus.IN_PROGRESS)
        assert self.manager.resources[0].status == ResourceStatus.IN_PROGRESS
    
    def test_get_resources_by_topic(self):
        """Test filtering resources by topic."""
        self.manager.add_resource(
            title="LA Course", resource_type="course", url="https://ex1.com",
            difficulty=DifficultyLevel.BEGINNER, description="", 
            topics=["Linear Algebra"]
        )
        self.manager.add_resource(
            title="Python Video", resource_type="video", url="https://ex2.com",
            difficulty=DifficultyLevel.BEGINNER, description="",
            topics=["Python"]
        )
        
        la_resources = self.manager.get_resources_by_topic("Linear Algebra")
        assert len(la_resources) == 1
        assert la_resources[0].title == "LA Course"


class TestFlashcardManager:
    """Test flashcard functionality."""
    
    def setup_method(self):
        """Create fresh flashcard manager."""
        from models import FlashcardDeck
        self.decks = []
        self.manager = FlashcardManager(self.decks)
    
    def test_create_deck(self):
        """Test creating a flashcard deck."""
        deck = self.manager.create_deck("Linear Algebra", "LA concepts")
        
        assert deck.topic == "Linear Algebra"
        assert len(self.manager.decks) == 1
    
    def test_add_card(self):
        """Test adding a flashcard."""
        deck = self.manager.create_deck("Test Topic", "")
        card = self.manager.add_card(
            deck.deck_id,
            "What is eigenvalue?",
            "A scalar value in LA"
        )
        
        assert card is not None
        assert card.question == "What is eigenvalue?"
        assert len(deck.cards) == 1
    
    def test_mark_card_review(self):
        """Test card review marking."""
        deck = self.manager.create_deck("Test", "")
        card = self.manager.add_card(deck.deck_id, "Q", "A")
        
        assert self.manager.mark_card_review(card.card_id, "easy")
        assert card.review_count == 1
        assert card.status == CardStatus.REVIEWING


class TestGitHubProjectManager:
    """Test GitHub project tracking."""
    
    def setup_method(self):
        """Create fresh project manager."""
        from models import GitHubProject
        self.projects = []
        self.manager = GitHubProjectManager(self.projects)
    
    def test_add_project(self):
        """Test adding a project."""
        project = self.manager.add_project(
            name="ML Basics",
            repo_url="https://github.com/user/ml-basics",
            description="ML implementations from scratch",
            skills=["Python", "ML"]
        )
        
        assert project.name == "ML Basics"
        assert len(self.manager.projects) == 1
    
    def test_update_status(self):
        """Test updating project status."""
        project = self.manager.add_project(
            name="Test", repo_url="https://example.com",
            description="Test", skills=[]
        )
        
        assert self.manager.update_project_status(project.project_id, ProjectStatus.IN_PROGRESS)
        assert project.status == ProjectStatus.IN_PROGRESS
    
    def test_add_feature(self):
        """Test marking project features."""
        project = self.manager.add_project(
            name="Test", repo_url="https://example.com",
            description="Test", skills=[]
        )
        
        assert self.manager.add_project_feature(project.project_id, "has_readme", True)
        assert project.has_readme == True


class TestPersistence:
    """Test storage and persistence."""
    
    def setup_method(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir)
    
    def test_save_and_load(self):
        """Test saving and loading state."""
        storage = StorageManager(self.test_dir)
        
        # Create and save state
        state = storage.load_state()
        state.progress.total_hours = 100.0
        storage.save_state(state)
        
        # Load and verify
        storage2 = StorageManager(self.test_dir)
        loaded_state = storage2.load_state()
        
        assert loaded_state.progress.total_hours == 100.0
    
    def test_default_state_creation(self):
        """Test default state is created."""
        storage = StorageManager(self.test_dir)
        state = storage.load_state()
        
        assert state is not None
        assert len(state.roadmap.years) == 2


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("AI GROWTH ENGINE - TEST SUITE")
    print("=" * 60)
    
    test_classes = [
        TestRoadmapManager,
        TestProgressManager,
        TestResourceManager,
        TestFlashcardManager,
        TestGitHubProjectManager,
        TestPersistence
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * 40)
        
        instance = test_class()
        
        # Get all test methods
        test_methods = [m for m in dir(instance) if m.startswith("test_")]
        
        for method_name in test_methods:
            try:
                # Setup
                if hasattr(instance, 'setup_method'):
                    instance.setup_method()
                
                # Run test
                method = getattr(instance, method_name)
                method()
                
                # Teardown
                if hasattr(instance, 'teardown_method'):
                    instance.teardown_method()
                
                print(f"  ✓ {method_name}")
                passed_tests += 1
            
            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
            except Exception as e:
                print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
            
            total_tests += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed_tests}/{total_tests} tests passed")
    print("=" * 60)
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
