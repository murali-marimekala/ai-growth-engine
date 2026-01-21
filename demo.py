#!/usr/bin/env python3
"""
DEMO - AI Growth Engine in action
Run this to see the system working and understand the data flow.
"""

import sys
import os
from datetime import datetime, timedelta
import tempfile
import shutil

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import DifficultyLevel, ResourceStatus, ProjectStatus
from persistence import StorageManager
from business_logic import (
    RoadmapManager, ProgressManager, ResourceManager,
    FlashcardManager, GitHubProjectManager
)


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo():
    """Run demonstration of the AI Growth Engine."""
    
    print_header("AI/ML CAREER TRANSITION COACH - INTERACTIVE DEMO")
    
    # Create temporary storage for demo
    demo_dir = tempfile.mktemp(prefix="ai_coach_demo_")
    print(f"📁 Using temporary storage: {demo_dir}\n")
    
    storage = StorageManager(demo_dir)
    state = storage.load_state()
    
    # Initialize managers
    roadmap_mgr = RoadmapManager(state.roadmap)
    progress_mgr = ProgressManager(state.progress)
    resource_mgr = ResourceManager(state.resources)
    flashcard_mgr = FlashcardManager(state.flashcard_decks)
    project_mgr = GitHubProjectManager(state.github_projects)
    
    # =====================================================================
    # DEMO 1: View Roadmap
    # =====================================================================
    print_header("DEMO 1: VIEWING THE ROADMAP")
    print("Let's see the 2-year learning path...\n")
    
    print(roadmap_mgr.get_roadmap_summary()[:500] + "...\n")
    print("[Truncated for demo - full roadmap has 100+ milestones]")
    
    input("Press Enter to continue...")
    
    # =====================================================================
    # DEMO 2: Log Learning Sessions
    # =====================================================================
    print_header("DEMO 2: LOGGING LEARNING SESSIONS")
    print("Let's simulate a week of learning...\n")
    
    topics_per_day = [
        (2.0, ["Python Basics", "Setup"]),
        (1.5, ["Python OOP", "Practice"]),
        (2.0, ["Linear Algebra", "Vectors"]),
        (2.5, ["Python", "Linear Algebra"]),
        (1.5, ["Deep Learning Basics"]),
    ]
    
    for day, (hours, topics) in enumerate(topics_per_day, 1):
        session = progress_mgr.log_session(
            duration_hours=hours,
            topics=topics,
            resources=["Video", "Practice"],
            notes=f"Day {day} of learning",
            mood="focused"
        )
        print(f"Day {day}: Logged {hours}h on {', '.join(topics)}")
    
    storage.save_state(state)
    
    input("\nPress Enter to see your progress...")
    
    # =====================================================================
    # DEMO 3: Progress Summary
    # =====================================================================
    print_header("DEMO 3: PROGRESS SUMMARY")
    print(progress_mgr.get_progress_summary())
    
    input("\nPress Enter to continue...")
    
    # =====================================================================
    # DEMO 4: Create and Use Flashcards
    # =====================================================================
    print_header("DEMO 4: FLASHCARD SYSTEM")
    print("Creating a flashcard deck for Linear Algebra...\n")
    
    deck = flashcard_mgr.create_deck(
        "Linear Algebra Fundamentals",
        "Essential concepts for ML"
    )
    print(f"✓ Created deck: {deck.topic}")
    
    # Add some cards
    cards_data = [
        ("What is a vector?", "A 1D array of numbers representing magnitude and direction"),
        ("What is matrix multiplication?", "Combining two matrices where columns of first match rows of second"),
        ("What are eigenvalues?", "Scalar values that scale eigenvectors in linear transformations"),
        ("What is singular value decomposition?", "Factorization of matrix into U, Σ, V^T components"),
    ]
    
    for question, answer in cards_data:
        card = flashcard_mgr.add_card(deck.deck_id, question, answer)
        print(f"  ✓ Added: {question[:50]}...")
    
    print(f"\n✓ Created deck with {len(deck.cards)} flashcards")
    storage.save_state(state)
    
    input("\nPress Enter to continue...")
    
    # =====================================================================
    # DEMO 5: Manage Learning Resources
    # =====================================================================
    print_header("DEMO 5: RESOURCE MANAGEMENT")
    print("Adding curated learning resources...\n")
    
    resources_data = [
        ("3Blue1Brown - Essence of Linear Algebra", "video", "https://youtu.be/fNk_zzaMoSY",
         DifficultyLevel.BEGINNER, ["Linear Algebra", "Math"]),
        ("Linear Algebra MIT OpenCourseWare", "course", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
         DifficultyLevel.BEGINNER, ["Linear Algebra", "Math"]),
        ("Pattern Recognition and Machine Learning", "book", "https://www.springer.com/",
         DifficultyLevel.INTERMEDIATE, ["ML", "Theory"]),
        ("Fast.ai Practical Deep Learning", "course", "https://www.fast.ai/",
         DifficultyLevel.INTERMEDIATE, ["Deep Learning", "Python"]),
    ]
    
    for title, rtype, url, difficulty, topics in resources_data:
        resource = resource_mgr.add_resource(title, rtype, url, difficulty, "", topics)
        print(f"  ✓ {title} ({rtype})")
    
    print(f"\n✓ Added {len(resource_mgr.resources)} learning resources")
    storage.save_state(state)
    
    input("\nPress Enter to see resources...")
    
    # =====================================================================
    # DEMO 6: Track Projects
    # =====================================================================
    print_header("DEMO 6: GITHUB PORTFOLIO TRACKING")
    print("Adding AI/ML projects to your portfolio...\n")
    
    projects_data = [
        ("ML-Basics-From-Scratch", "https://github.com/user/ml-basics",
         "Linear regression, decision trees, and KNN implementations from scratch",
         ["Python", "ML", "Algorithms"]),
        ("NLP-Sentiment-Analysis", "https://github.com/user/sentiment-nlp",
         "End-to-end sentiment analysis pipeline with ML and neural networks",
         ["Python", "NLP", "Deep Learning"]),
        ("MLOps-Pipeline-Demo", "https://github.com/user/mlops-pipeline",
         "Production ML pipeline with CI/CD, monitoring, and model serving",
         ["MLOps", "Python", "Docker"]),
    ]
    
    for name, url, description, skills in projects_data:
        project = project_mgr.add_project(name, url, description, skills)
        # Mark some features as complete
        if name == "ML-Basics-From-Scratch":
            project_mgr.add_project_feature(project.project_id, "has_readme", True)
            project_mgr.add_project_feature(project.project_id, "has_tests", True)
        print(f"  ✓ {name}")
    
    print(f"\n✓ Added {len(project_mgr.projects)} portfolio projects")
    storage.save_state(state)
    
    input("\nPress Enter to see portfolio summary...")
    
    # =====================================================================
    # DEMO 7: Portfolio Summary
    # =====================================================================
    print_header("DEMO 7: PORTFOLIO SUMMARY")
    print(project_mgr.get_portfolio_summary())
    
    input("\nPress Enter to continue...")
    
    # =====================================================================
    # DEMO 8: Current Focus
    # =====================================================================
    print_header("DEMO 8: YOUR CURRENT LEARNING FOCUS")
    
    focus = roadmap_mgr.get_current_focus()
    
    print(f"Year: {focus.get('year', 'N/A')}")
    print(f"Quarter: {focus.get('quarter', 'N/A')}")
    print(f"Month: {focus.get('month', 'N/A')}")
    print(f"Week: {focus.get('week', 'N/A')}")
    
    if 'tasks' in focus:
        print(f"\n📋 Current Tasks ({len(focus['tasks'])} active):")
        for task in focus['tasks'][:5]:
            print(f"  • {task}")
    
    input("\nPress Enter for key insights...")
    
    # =====================================================================
    # DEMO 9: Key Statistics
    # =====================================================================
    print_header("DEMO 9: YOUR LEARNING STATISTICS")
    
    print(f"📊 KEY METRICS")
    print(f"  Total Hours Logged: {progress_mgr.progress.total_hours:.1f}h")
    print(f"  Sessions Completed: {len(progress_mgr.progress.daily_sessions)}")
    print(f"  Current Streak: {progress_mgr.progress.current_streak} days 🔥")
    
    print(f"\n📚 FLASHCARD DECKS")
    print(f"  Total Decks: {len(flashcard_mgr.decks)}")
    for deck in flashcard_mgr.decks:
        print(f"  • {deck.topic}: {len(deck.cards)} cards")
    
    print(f"\n📖 LEARNING RESOURCES")
    print(f"  Total Resources: {len(resource_mgr.resources)}")
    by_status = {}
    for r in resource_mgr.resources:
        status = r.status.value
        by_status[status] = by_status.get(status, 0) + 1
    for status, count in by_status.items():
        print(f"  • {status}: {count}")
    
    print(f"\n🚀 PORTFOLIO PROJECTS")
    print(f"  Total Projects: {len(project_mgr.projects)}")
    for project in project_mgr.projects:
        features = sum([project.has_readme, project.has_docs, project.has_tests, project.has_demo])
        print(f"  • {project.name}: {features}/4 features complete")
    
    input("\nPress Enter for final thoughts...")
    
    # =====================================================================
    # DEMO 10: Advice
    # =====================================================================
    print_header("TIPS FOR SUCCESS")
    
    print("""
✓ CONSISTENCY IS KEY
  • Aim for 4-5 learning sessions per week
  • Even 1.5-2 hours per session is valuable
  • Your streak is your best motivation

✓ USE MULTIPLE LEARNING MODALITIES
  • Videos for visual learners
  • Books/papers for deep understanding
  • Hands-on practice for retention
  • Flashcards for quick review

✓ BUILD REAL PROJECTS
  • Don't just watch - CODE
  • Create portfolio projects early
  • Deploy something live
  • Write about your learnings

✓ TRACK YOUR PROGRESS
  • Log every session (5 min max)
  • Update resources as you complete them
  • Mark tasks complete
  • Review weekly summaries

✓ STAY FOCUSED
  • Master Year 1 foundations before Year 2
  • One quarter at a time
  • Quality depth > breadth
  • Breadth comes after mastery

✓ YOUR ADVANTAGE
  • 20+ years of leadership = discipline
  • Know how to learn at scale
  • Can mentor others on your journey
  • Management skills will help in senior roles
""")
    
    input("\nPress Enter for next steps...")
    
    # =====================================================================
    # Demo Complete
    # =====================================================================
    print_header("DEMO COMPLETE! 🎉")
    
    print("""
You've seen how the AI Growth Engine works:

1. ✓ View your structured 2-year roadmap
2. ✓ Log daily learning sessions
3. ✓ Create and review flashcards
4. ✓ Track learning resources
5. ✓ Manage your portfolio projects
6. ✓ Get progress summaries
7. ✓ Receive coaching guidance

NEXT STEPS:
===========

1. Install the system:
   pip install -r requirements.txt

2. Start your learning journey:
   python coach.py status
   python coach.py focus
   python coach.py log 2.5 "Python,Setup"

3. Set up your learning system:
   python coach.py create-deck "Week 1 Topics"
   python coach.py add-resource course "Title" "URL" beginner "topics"

4. Log daily:
   python coach.py log <hours> "<topics>"
   python coach.py review

5. Track progress:
   python coach.py week
   python coach.py progress

6. (Optional) Enable AI coaching:
   - Get OpenAI API key
   - Add to .env file
   - Use: python coach.py interview

REMEMBER:
=========
You've built 20+ years of discipline and leadership.
Channel that into mastering AI/ML.
Focus on daily progress. Trust the process.

The results will compound.

You've got this! 🚀
""")
    
    # Cleanup
    print("\n📁 Cleaning up demo storage...")
    shutil.rmtree(demo_dir, ignore_errors=True)
    print("✓ Demo complete!\n")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for watching!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
