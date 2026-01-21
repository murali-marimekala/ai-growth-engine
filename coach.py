#!/usr/bin/env python3
"""
AI/ML Career Transition Coach - Main CLI Application
A comprehensive system to help senior engineering managers transition into AI/ML roles.

USAGE:
    python coach.py <command> [options]

COMMANDS:
    roadmap              Show the complete 2-year learning roadmap
    status              Show current learning progress and statistics
    log <hours> <topics>    Log a daily learning session (e.g., 'log 2.5 Python,Linear_Algebra')
    focus                Show current learning focus and upcoming tasks
    tasks                List upcoming tasks and milestones
    mark-task <task_id>   Mark a task as complete
    
    resources            Show all learning resources
    add-resource <type> <title> <url>  Add a learning resource
    resource-status <id> <status>      Mark resource status (todo/in_progress/completed)
    
    flashcards          Show flashcard statistics
    create-deck <topic>   Create a new flashcard deck
    add-card <deck_id> <question> <answer>  Add a flashcard
    review               Start a flashcard review session
    
    projects            Show GitHub portfolio projects
    add-project <name> <url> <description>  Add a portfolio project
    update-project <id> <status>            Update project status
    add-feature <id> <feature>              Mark project feature as done
    
    tips                Show this week's coaching tips
    
    progress            Show detailed progress summary
    week                Show this week's summary
    
    interview           Get AI-powered interview prep advice (requires API key)
    suggest <topic>     Get AI-powered resource suggestions (requires API key)
    
    help                Show this help message

SETUP:
    1. Create .env file in the app directory with (optional):
       OPENAI_API_KEY=sk-...
    
    2. All data is stored in data/app_state.json
"""

import sys
import json
import argparse
from typing import List, Optional
from datetime import datetime
from pathlib import Path

from models import (
    DifficultyLevel, ResourceStatus, MilestoneStatus, ProjectStatus, CardStatus
)
from persistence import StorageManager
from business_logic import (
    RoadmapManager, ProgressManager, ResourceManager, FlashcardManager,
    GitHubProjectManager, CoachingTipsManager
)
from ai_coach import AICoach


class CareerCoach:
    """Main application controller."""
    
    def __init__(self, data_dir: str = "data"):
        self.storage = StorageManager(data_dir)
        self.state = self.storage.load_state()
        
        # Initialize managers
        self.roadmap_mgr = RoadmapManager(self.state.roadmap)
        self.progress_mgr = ProgressManager(self.state.progress)
        self.resource_mgr = ResourceManager(self.state.resources)
        self.flashcard_mgr = FlashcardManager(self.state.flashcard_decks)
        self.project_mgr = GitHubProjectManager(self.state.github_projects)
        self.tips_mgr = CoachingTipsManager(self.state.weekly_tips)
        self.ai_coach = AICoach()
    
    def save(self):
        """Persist state to disk."""
        self.state.last_updated = datetime.now().isoformat()
        self.storage.save_state(self.state)
    
    def show_roadmap(self):
        """Display the complete roadmap."""
        print(self.roadmap_mgr.get_roadmap_summary())
    
    def show_status(self):
        """Display progress status."""
        print(self.progress_mgr.get_progress_summary())
        print("\n")
        print(self.ai_coach.get_status_message())
    
    def log_session(self, hours: float, topics_str: str, resources_str: str = "", notes: str = "", mood: str = None):
        """Log a daily learning session."""
        topics = [t.strip().replace("_", " ") for t in topics_str.split(",")]
        resources = [r.strip() for r in resources_str.split(",")] if resources_str else []
        
        session = self.progress_mgr.log_session(hours, topics, resources, notes, mood)
        self.save()
        
        print(f"✓ Session logged: {hours}h on {', '.join(topics)}")
        print(f"  Current streak: {self.progress_mgr.progress.current_streak} days 🔥")
        print(f"  Total hours: {self.progress_mgr.progress.total_hours:.1f}h")
    
    def show_focus(self):
        """Show current learning focus."""
        focus = self.roadmap_mgr.get_current_focus()
        
        print("=" * 60)
        print("YOUR CURRENT FOCUS")
        print("=" * 60)
        
        if "message" in focus:
            print(f"\n{focus['message']}")
        else:
            print(f"\nYear: {focus['year']}")
            print(f"Quarter: {focus['quarter']}")
            print(f"Month: {focus['month']}")
            print(f"Week: {focus['week']}")
            print(f"\nCurrent Tasks:")
            for i, task in enumerate(focus['tasks'][:5], 1):
                print(f"  {i}. {task}")
    
    def show_upcoming_tasks(self):
        """Show upcoming tasks."""
        tasks = self.roadmap_mgr.get_upcoming_tasks(7)
        
        print("=" * 60)
        print("UPCOMING TASKS")
        print("=" * 60)
        
        if not tasks:
            print("\nNo upcoming tasks. Great job! 🎉")
        else:
            for i, task in enumerate(tasks, 1):
                print(f"\n{i}. {task}")
    
    def mark_task_complete(self, task_id: str):
        """Mark a task as complete."""
        if self.roadmap_mgr.mark_task_complete(task_id):
            self.save()
            print(f"✓ Task {task_id} marked as complete!")
        else:
            print(f"✗ Task {task_id} not found")
    
    def add_resource(self, resource_type: str, title: str, url: str, difficulty: str = "beginner", topics: str = ""):
        """Add a learning resource."""
        try:
            diff = DifficultyLevel(difficulty.lower())
        except ValueError:
            print(f"Invalid difficulty. Use: beginner, intermediate, advanced")
            return
        
        topic_list = [t.strip() for t in topics.split(",")] if topics else [title]
        
        resource = self.resource_mgr.add_resource(
            title=title,
            resource_type=resource_type.lower(),
            url=url,
            difficulty=diff,
            description="",
            topics=topic_list
        )
        
        self.save()
        print(f"✓ Resource added: {resource.title}")
        print(f"  ID: {resource.resource_id}")
    
    def show_resources(self):
        """Show learning resources."""
        print(self.resource_mgr.get_resources_summary())
    
    def update_resource_status(self, resource_id: str, status: str):
        """Update resource status."""
        try:
            stat = ResourceStatus(status.lower())
        except ValueError:
            print(f"Invalid status. Use: todo, in_progress, completed")
            return
        
        if self.resource_mgr.mark_resource_status(resource_id, stat):
            self.save()
            print(f"✓ Resource {resource_id} status updated to {status}")
        else:
            print(f"✗ Resource {resource_id} not found")
    
    def create_flashcard_deck(self, topic: str, description: str = ""):
        """Create a flashcard deck."""
        deck = self.flashcard_mgr.create_deck(topic, description)
        self.save()
        print(f"✓ Flashcard deck created: {topic}")
        print(f"  ID: {deck.deck_id}")
    
    def add_flashcard(self, deck_id: str, question: str, answer: str):
        """Add a flashcard to a deck."""
        card = self.flashcard_mgr.add_card(deck_id, question, answer)
        if card:
            self.save()
            print(f"✓ Card added to deck")
            print(f"  Question: {question}")
        else:
            print(f"✗ Deck {deck_id} not found")
    
    def review_flashcards(self, num_cards: int = 10):
        """Interactive flashcard review session."""
        cards = self.flashcard_mgr.get_cards_for_review(num_cards)
        
        if not cards:
            print("No cards to review. Create some flashcard decks first!")
            return
        
        print(f"\n📚 FLASHCARD REVIEW SESSION ({len(cards)} cards)")
        print("=" * 60)
        
        for i, card in enumerate(cards, 1):
            print(f"\n[{i}/{len(cards)}] {card.topic}")
            print(f"\nQ: {card.question}")
            input("Press Enter to reveal answer...")
            print(f"A: {card.answer}")
            
            while True:
                result = input("\nHow did you do? (easy/hard/difficult/mastered): ").lower().strip()
                if result in ["easy", "hard", "difficult", "mastered"]:
                    break
                print("Invalid input. Use: easy, hard, difficult, or mastered")
            
            self.flashcard_mgr.mark_card_review(card.card_id, result)
        
        self.save()
        print(f"\n✓ Review session complete!")
        print(self.flashcard_mgr.get_flashcard_stats())
    
    def show_flashcard_stats(self):
        """Show flashcard statistics."""
        print(self.flashcard_mgr.get_flashcard_stats())
    
    def add_github_project(self, name: str, repo_url: str, description: str, skills: str = ""):
        """Add a GitHub project."""
        skill_list = [s.strip() for s in skills.split(",")] if skills else []
        
        project = self.project_mgr.add_project(name, repo_url, description, skill_list)
        self.save()
        
        print(f"✓ Project added: {name}")
        print(f"  ID: {project.project_id}")
        print(f"  URL: {repo_url}")
    
    def show_projects(self):
        """Show GitHub portfolio projects."""
        print(self.project_mgr.get_portfolio_summary())
    
    def update_project_status(self, project_id: str, status: str):
        """Update project status."""
        try:
            stat = ProjectStatus(status.lower())
        except ValueError:
            print(f"Invalid status. Use: planning, in_progress, completed")
            return
        
        if self.project_mgr.update_project_status(project_id, stat):
            self.save()
            print(f"✓ Project {project_id} status updated to {status}")
        else:
            print(f"✗ Project {project_id} not found")
    
    def add_project_feature(self, project_id: str, feature: str):
        """Mark a project feature as complete."""
        if self.project_mgr.add_project_feature(project_id, f"has_{feature}", True):
            self.save()
            print(f"✓ Project {project_id}: {feature} marked as complete")
        else:
            print(f"✗ Invalid feature or project not found")
    
    def show_tips(self):
        """Show weekly coaching tips."""
        print(self.tips_mgr.get_weekly_tips_summary())
    
    def generate_tips(self):
        """Generate this week's coaching tips."""
        current_week = (datetime.now().isocalendar()[1] % 52) + 1
        tips = self.tips_mgr.generate_weekly_tips(current_week, "AI/ML Learning")
        self.save()
        
        print(f"✓ Generated {len(tips)} coaching tips for this week")
        self.show_tips()
    
    def show_progress(self):
        """Show detailed progress summary."""
        print(self.progress_mgr.get_progress_summary())
    
    def show_week(self):
        """Show this week's summary."""
        print(self.progress_mgr.get_weekly_summary())
    
    def get_interview_prep(self):
        """Get AI-powered interview preparation."""
        if not self.ai_coach.enabled:
            print("AI Coach not enabled. Add OPENAI_API_KEY to .env file to use this feature.")
            return
        
        print("\n🎯 INTERVIEW PREPARATION GUIDE")
        print("=" * 70)
        
        advice = self.ai_coach.interview_prep()
        if advice:
            print(advice)
        else:
            print("Could not generate advice. Please check your API key.")
    
    def suggest_resources(self, topic: str, difficulty: str = "intermediate"):
        """Get AI-powered resource suggestions."""
        if not self.ai_coach.enabled:
            print("AI Coach not enabled. Add OPENAI_API_KEY to .env file to use this feature.")
            return
        
        print(f"\n💡 RESOURCE SUGGESTIONS FOR: {topic}")
        print("=" * 70)
        
        suggestions = self.ai_coach.suggest_resources(topic, difficulty)
        if suggestions:
            print(suggestions)
        else:
            print("Could not generate suggestions. Please check your API key.")
    
    def show_help(self):
        """Show help message."""
        print(__doc__)


def main():
    """Main entry point."""
    coach = CareerCoach()
    
    if len(sys.argv) == 1:
        coach.show_help()
        return
    
    command = sys.argv[1].lower()
    
    # Roadmap commands
    if command == "roadmap":
        coach.show_roadmap()
    
    elif command == "status":
        coach.show_status()
    
    elif command == "log":
        if len(sys.argv) < 4:
            print("Usage: coach.py log <hours> <topics> [resources] [notes] [mood]")
            print("Example: coach.py log 2.5 Python,Linear_Algebra")
            return
        
        hours = float(sys.argv[2])
        topics = sys.argv[3]
        resources = sys.argv[4] if len(sys.argv) > 4 else ""
        notes = sys.argv[5] if len(sys.argv) > 5 else ""
        mood = sys.argv[6] if len(sys.argv) > 6 else None
        
        coach.log_session(hours, topics, resources, notes, mood)
    
    elif command == "focus":
        coach.show_focus()
    
    elif command == "tasks":
        coach.show_upcoming_tasks()
    
    elif command == "mark-task":
        if len(sys.argv) < 3:
            print("Usage: coach.py mark-task <task_id>")
            return
        coach.mark_task_complete(sys.argv[2])
    
    # Resource commands
    elif command == "resources":
        coach.show_resources()
    
    elif command == "add-resource":
        if len(sys.argv) < 5:
            print("Usage: coach.py add-resource <type> <title> <url> [difficulty] [topics]")
            print("Example: coach.py add-resource course 'Linear Algebra' https://... intermediate 'Math,ML'")
            return
        
        rtype = sys.argv[2]
        title = sys.argv[3]
        url = sys.argv[4]
        difficulty = sys.argv[5] if len(sys.argv) > 5 else "beginner"
        topics = sys.argv[6] if len(sys.argv) > 6 else ""
        
        coach.add_resource(rtype, title, url, difficulty, topics)
    
    elif command == "resource-status":
        if len(sys.argv) < 4:
            print("Usage: coach.py resource-status <resource_id> <status>")
            return
        coach.update_resource_status(sys.argv[2], sys.argv[3])
    
    # Flashcard commands
    elif command == "flashcards":
        coach.show_flashcard_stats()
    
    elif command == "create-deck":
        if len(sys.argv) < 3:
            print("Usage: coach.py create-deck <topic> [description]")
            return
        
        topic = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        coach.create_flashcard_deck(topic, description)
    
    elif command == "add-card":
        if len(sys.argv) < 5:
            print("Usage: coach.py add-card <deck_id> <question> <answer>")
            return
        
        deck_id = sys.argv[2]
        question = sys.argv[3]
        answer = sys.argv[4]
        coach.add_flashcard(deck_id, question, answer)
    
    elif command == "review":
        num_cards = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        coach.review_flashcards(num_cards)
    
    # Project commands
    elif command == "projects":
        coach.show_projects()
    
    elif command == "add-project":
        if len(sys.argv) < 5:
            print("Usage: coach.py add-project <name> <repo_url> <description> [skills]")
            return
        
        name = sys.argv[2]
        url = sys.argv[3]
        description = sys.argv[4]
        skills = sys.argv[5] if len(sys.argv) > 5 else ""
        
        coach.add_github_project(name, url, description, skills)
    
    elif command == "update-project":
        if len(sys.argv) < 4:
            print("Usage: coach.py update-project <project_id> <status>")
            return
        coach.update_project_status(sys.argv[2], sys.argv[3])
    
    elif command == "add-feature":
        if len(sys.argv) < 4:
            print("Usage: coach.py add-feature <project_id> <feature>")
            print("Features: readme, docs, tests, demo")
            return
        coach.add_project_feature(sys.argv[2], sys.argv[3])
    
    # Coaching commands
    elif command == "tips":
        coach.show_tips()
    
    elif command == "generate-tips":
        coach.generate_tips()
    
    elif command == "progress":
        coach.show_progress()
    
    elif command == "week":
        coach.show_week()
    
    elif command == "interview":
        coach.get_interview_prep()
    
    elif command == "suggest":
        if len(sys.argv) < 3:
            print("Usage: coach.py suggest <topic> [difficulty]")
            return
        topic = sys.argv[2]
        difficulty = sys.argv[3] if len(sys.argv) > 3 else "intermediate"
        coach.suggest_resources(topic, difficulty)
    
    elif command == "help" or command == "-h" or command == "--help":
        coach.show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'coach.py help' for usage information.")


if __name__ == "__main__":
    main()
