"""
Business logic modules for the AI Coach application.
Includes: roadmap management, progress tracking, flashcards, and AI-powered features.
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from models import (
    AppState, Roadmap, ProgressState, DailySession, Resource, Flashcard, FlashcardDeck,
    GitHubProject, WeeklyTip, Year, Quarter, Month, Week, WeeklyTask,
    MilestoneStatus, ResourceStatus, DifficultyLevel, CardStatus, ProjectStatus
)


class RoadmapManager:
    """Manages roadmap navigation and milestone tracking."""
    
    def __init__(self, roadmap: Roadmap):
        self.roadmap = roadmap
    
    def get_roadmap_summary(self) -> str:
        """Get formatted roadmap summary."""
        lines = ["=" * 80, "AI/ML CAREER TRANSITION ROADMAP (2 YEARS)", "=" * 80]
        
        for year in self.roadmap.years:
            lines.append(f"\n{year.name} (Status: {year.status.value})")
            lines.append(f"  Description: {year.description}")
            lines.append(f"  Focus Areas: {', '.join(year.focus_areas)}")
            
            for quarter in year.quarters:
                completion = self._calculate_completion(quarter)
                lines.append(f"\n  └─ {quarter.name} ({completion}%)")
                lines.append(f"     Description: {quarter.description}")
                lines.append(f"     Focus: {', '.join(quarter.focus_areas)}")
                
                for month in quarter.months:
                    m_completion = self._calculate_completion(month)
                    lines.append(f"     └─ {month.name} ({m_completion}%)")
                    
                    for week in month.weeks:
                        w_completion = self._calculate_completion(week)
                        status_icon = "✓" if week.status == MilestoneStatus.COMPLETED else "→" if week.status == MilestoneStatus.IN_PROGRESS else "○"
                        lines.append(f"        {status_icon} Week {week.week_num}: {week.name} ({w_completion}%)")
        
        return "\n".join(lines)
    
    def get_current_focus(self) -> Dict[str, Any]:
        """Get current learning focus based on progress."""
        for year in self.roadmap.years:
            if year.status != MilestoneStatus.COMPLETED:
                for quarter in year.quarters:
                    if quarter.status != MilestoneStatus.COMPLETED:
                        for month in quarter.months:
                            if month.status != MilestoneStatus.COMPLETED:
                                for week in month.weeks:
                                    if week.status != MilestoneStatus.COMPLETED:
                                        return {
                                            "year": year.name,
                                            "quarter": quarter.name,
                                            "month": month.name,
                                            "week": week.name,
                                            "tasks": [t.name for t in week.tasks if t.status != MilestoneStatus.COMPLETED],
                                        }
        
        return {"year": "Completed!", "message": "Congratulations on finishing the roadmap!"}
    
    def mark_task_complete(self, task_id: str) -> bool:
        """Mark a specific task as complete."""
        for year in self.roadmap.years:
            for quarter in year.quarters:
                for month in quarter.months:
                    for week in month.weeks:
                        for task in week.tasks:
                            if task.task_id == task_id:
                                task.status = MilestoneStatus.COMPLETED
                                self._update_parent_status(week, month, quarter, year)
                                return True
        return False
    
    def _update_parent_status(self, week: Week, month: Month, quarter: Quarter, year: Year):
        """Update parent status based on child completion."""
        # Check if all tasks in week are done
        if all(t.status == MilestoneStatus.COMPLETED for t in week.tasks):
            week.status = MilestoneStatus.COMPLETED
        
        # Check if all weeks in month are done
        if all(w.status == MilestoneStatus.COMPLETED for w in month.weeks):
            month.status = MilestoneStatus.COMPLETED
        
        # Check if all months in quarter are done
        if all(m.status == MilestoneStatus.COMPLETED for m in quarter.months):
            quarter.status = MilestoneStatus.COMPLETED
        
        # Check if all quarters in year are done
        if all(q.status == MilestoneStatus.COMPLETED for q in year.quarters):
            year.status = MilestoneStatus.COMPLETED
    
    def _calculate_completion(self, obj) -> int:
        """Calculate completion percentage for any level."""
        if hasattr(obj, 'quarters'):
            items = obj.quarters
        elif hasattr(obj, 'months'):
            items = obj.months
        elif hasattr(obj, 'weeks'):
            items = obj.weeks
        elif hasattr(obj, 'tasks'):
            items = obj.tasks
        else:
            return 0
        
        if not items:
            return 0
        
        completed = sum(1 for item in items if item.status == MilestoneStatus.COMPLETED)
        return int(100 * completed / len(items))
    
    def get_upcoming_tasks(self, days_ahead: int = 7) -> List[str]:
        """Get upcoming tasks."""
        upcoming = []
        for year in self.roadmap.years:
            for quarter in year.quarters:
                for month in quarter.months:
                    for week in month.weeks:
                        for task in week.tasks:
                            if task.status != MilestoneStatus.COMPLETED:
                                upcoming.append(f"{week.name} - {task.name} ({task.description})")
                        if len(upcoming) >= 5:  # Return top 5
                            return upcoming
        return upcoming


class ProgressManager:
    """Manages daily progress tracking and statistics."""
    
    def __init__(self, progress: ProgressState):
        self.progress = progress
    
    def log_session(self, duration_hours: float, topics: List[str], resources: List[str], notes: str = "", mood: str = None) -> DailySession:
        """Log a daily learning session."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        session = DailySession(
            date=today,
            duration_hours=duration_hours,
            topics_covered=topics,
            resources_used=resources,
            notes=notes,
            mood=mood,
        )
        
        self.progress.daily_sessions.append(session)
        self.progress.total_hours += duration_hours
        self.progress.last_session_date = today
        self.progress.updated_at = datetime.now().isoformat()
        
        # Update streak
        self._update_streak()
        
        return session
    
    def _update_streak(self):
        """Update current and longest streaks."""
        if not self.progress.daily_sessions:
            self.progress.current_streak = 0
            return
        
        sessions_by_date = {s.date: s for s in self.progress.daily_sessions}
        dates = sorted(sessions_by_date.keys())
        
        current_streak = 0
        longest_streak = 0
        temp_streak = 1
        
        for i, date in enumerate(dates):
            if i == 0:
                temp_streak = 1
            else:
                prev_date = datetime.strptime(dates[i-1], "%Y-%m-%d")
                curr_date = datetime.strptime(date, "%Y-%m-%d")
                
                if (curr_date - prev_date).days == 1:
                    temp_streak += 1
                else:
                    longest_streak = max(longest_streak, temp_streak)
                    temp_streak = 1
        
        longest_streak = max(longest_streak, temp_streak)
        
        # Check if streak is still active (last session was today or yesterday)
        if dates:
            last_date = datetime.strptime(dates[-1], "%Y-%m-%d")
            today = datetime.now().date()
            days_since = (today - last_date.date()).days
            
            if days_since == 0:
                current_streak = temp_streak
            elif days_since == 1:
                current_streak = temp_streak
            else:
                current_streak = 0
        
        self.progress.current_streak = current_streak
        self.progress.longest_streak = longest_streak
    
    def get_progress_summary(self) -> str:
        """Get formatted progress summary."""
        lines = ["=" * 60, "YOUR LEARNING PROGRESS", "=" * 60]
        
        lines.append(f"\n📊 STATISTICS")
        lines.append(f"  Total Hours Logged: {self.progress.total_hours:.1f}")
        lines.append(f"  Sessions Completed: {len(self.progress.daily_sessions)}")
        lines.append(f"  Current Streak: {self.progress.current_streak} days 🔥")
        lines.append(f"  Longest Streak: {self.progress.longest_streak} days")
        
        if self.progress.daily_sessions:
            lines.append(f"\n📅 RECENT SESSIONS (Last 5)")
            for session in self.progress.daily_sessions[-5:]:
                mood_str = f" ({session.mood})" if session.mood else ""
                lines.append(f"  {session.date}: {session.duration_hours}h - {', '.join(session.topics_covered)}{mood_str}")
                if session.notes:
                    lines.append(f"    Notes: {session.notes}")
        
        return "\n".join(lines)
    
    def get_weekly_summary(self) -> str:
        """Get summary of this week's progress."""
        lines = ["=" * 60, "THIS WEEK'S SUMMARY", "=" * 60]
        
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        week_sessions = [s for s in self.progress.daily_sessions
                         if datetime.strptime(s.date, "%Y-%m-%d").date() >= week_start]
        
        total_hours = sum(s.duration_hours for s in week_sessions)
        unique_topics = set()
        for s in week_sessions:
            unique_topics.update(s.topics_covered)
        
        lines.append(f"\nWeek Starting: {week_start.strftime('%A, %B %d, %Y')}")
        lines.append(f"Sessions: {len(week_sessions)}")
        lines.append(f"Total Hours: {total_hours:.1f}")
        lines.append(f"Topics Covered: {', '.join(unique_topics) if unique_topics else 'None yet'}")
        
        if total_hours >= 15:
            lines.append(f"\n✨ Excellent week! You're on track for your 15-20 hours/week goal!")
        elif total_hours >= 10:
            lines.append(f"\n👍 Good progress! Try to add a few more hours this week.")
        else:
            lines.append(f"\n⚠️  Keep pushing! You can do {20 - total_hours:.1f} more hours this week.")
        
        return "\n".join(lines)


class ResourceManager:
    """Manages learning resources and recommendations."""
    
    def __init__(self, resources: List[Resource]):
        self.resources = resources
    
    def add_resource(self, title: str, resource_type: str, url: str, difficulty: DifficultyLevel,
                     description: str, topics: List[str]) -> Resource:
        """Add a new learning resource."""
        resource = Resource(
            resource_id=str(uuid.uuid4())[:8],
            title=title,
            resource_type=resource_type,
            url=url,
            difficulty=difficulty,
            description=description,
            mapped_topics=topics,
        )
        self.resources.append(resource)
        return resource
    
    def mark_resource_status(self, resource_id: str, status: ResourceStatus) -> bool:
        """Update resource status."""
        for resource in self.resources:
            if resource.resource_id == resource_id:
                resource.status = status
                if status == ResourceStatus.COMPLETED:
                    resource.completion_date = datetime.now().isoformat()
                return True
        return False
    
    def get_resources_by_topic(self, topic: str) -> List[Resource]:
        """Get all resources mapped to a topic."""
        return [r for r in self.resources if topic in r.mapped_topics]
    
    def get_resources_summary(self) -> str:
        """Get formatted resource summary."""
        lines = ["=" * 70, "LEARNING RESOURCES", "=" * 70]
        
        by_type = {}
        for r in self.resources:
            if r.resource_type not in by_type:
                by_type[r.resource_type] = []
            by_type[r.resource_type].append(r)
        
        for rtype, resources in sorted(by_type.items()):
            lines.append(f"\n{rtype.upper()}")
            completed = sum(1 for r in resources if r.status == ResourceStatus.COMPLETED)
            lines.append(f"  {completed}/{len(resources)} completed")
            
            for r in resources[:5]:  # Show top 5 per type
                status_icon = "✓" if r.status == ResourceStatus.COMPLETED else "→" if r.status == ResourceStatus.IN_PROGRESS else "○"
                lines.append(f"  {status_icon} {r.title} ({r.difficulty.value})")
                lines.append(f"     Topics: {', '.join(r.mapped_topics)}")
        
        return "\n".join(lines)


class FlashcardManager:
    """Manages flashcard decks and spaced repetition."""
    
    def __init__(self, decks: List[FlashcardDeck]):
        self.decks = decks
    
    def create_deck(self, topic: str, description: str) -> FlashcardDeck:
        """Create a new flashcard deck."""
        deck = FlashcardDeck(
            deck_id=str(uuid.uuid4())[:8],
            topic=topic,
            description=description,
        )
        self.decks.append(deck)
        return deck
    
    def add_card(self, deck_id: str, question: str, answer: str, difficulty: DifficultyLevel = DifficultyLevel.BEGINNER) -> Optional[Flashcard]:
        """Add a card to a deck."""
        for deck in self.decks:
            if deck.deck_id == deck_id:
                card = Flashcard(
                    card_id=str(uuid.uuid4())[:8],
                    question=question,
                    answer=answer,
                    topic=deck.topic,
                    difficulty=difficulty,
                )
                deck.cards.append(card)
                return card
        return None
    
    def get_cards_for_review(self, num_cards: int = 10) -> List[Flashcard]:
        """Get cards due for review using simple scheduling."""
        all_cards = []
        for deck in self.decks:
            all_cards.extend(deck.cards)
        
        # Sort by: new cards first, then by next_review date, then by review_count
        due_cards = []
        for card in all_cards:
            if card.status == CardStatus.NEW:
                due_cards.append((0, card))
            elif card.status == CardStatus.DIFFICULT:
                due_cards.append((1, card))
            elif card.next_review and datetime.fromisoformat(card.next_review) <= datetime.now():
                due_cards.append((2, card))
            else:
                due_cards.append((3, card))
        
        due_cards.sort(key=lambda x: (x[0], x[1].review_count))
        return [card for _, card in due_cards[:num_cards]]
    
    def mark_card_review(self, card_id: str, result: str) -> bool:
        """Mark card as reviewed with result (easy, hard, difficult, mastered)."""
        for deck in self.decks:
            for card in deck.cards:
                if card.card_id == card_id:
                    card.review_count += 1
                    card.last_reviewed = datetime.now().isoformat()
                    deck.total_reviews += 1
                    
                    # Update card status and schedule next review
                    if result == "mastered":
                        card.status = CardStatus.MASTERED
                        card.next_review = (datetime.now() + timedelta(days=30)).isoformat()
                    elif result == "easy":
                        card.status = CardStatus.REVIEWING
                        card.next_review = (datetime.now() + timedelta(days=7)).isoformat()
                    elif result == "hard":
                        card.status = CardStatus.REVIEWING
                        card.next_review = (datetime.now() + timedelta(days=1)).isoformat()
                    elif result == "difficult":
                        card.status = CardStatus.DIFFICULT
                        card.next_review = (datetime.now() + timedelta(hours=6)).isoformat()
                    
                    if card.status == CardStatus.NEW:
                        card.status = CardStatus.REVIEWING
                    
                    return True
        return False
    
    def get_flashcard_stats(self) -> str:
        """Get flashcard statistics."""
        lines = ["=" * 60, "FLASHCARD STATISTICS", "=" * 60]
        
        total_cards = 0
        total_decks = len(self.decks)
        total_reviews = 0
        
        for deck in self.decks:
            total_cards += len(deck.cards)
            total_reviews += deck.total_reviews
            
            new_count = sum(1 for c in deck.cards if c.status == CardStatus.NEW)
            mastered = sum(1 for c in deck.cards if c.status == CardStatus.MASTERED)
            
            lines.append(f"\n{deck.topic}")
            lines.append(f"  Cards: {len(deck.cards)} (New: {new_count}, Mastered: {mastered})")
            lines.append(f"  Reviews: {deck.total_reviews}")
        
        lines.insert(2, f"\nTotal Decks: {total_decks}")
        lines.insert(3, f"Total Cards: {total_cards}")
        lines.insert(4, f"Total Reviews: {total_reviews}")
        
        return "\n".join(lines)


class GitHubProjectManager:
    """Manages portfolio GitHub projects."""
    
    def __init__(self, projects: List[GitHubProject]):
        self.projects = projects
    
    def add_project(self, name: str, repo_url: str, description: str, skills: List[str]) -> GitHubProject:
        """Add a new GitHub project."""
        project = GitHubProject(
            project_id=str(uuid.uuid4())[:8],
            name=name,
            repo_url=repo_url,
            description=description,
            skills_covered=skills,
        )
        self.projects.append(project)
        return project
    
    def update_project_status(self, project_id: str, status: ProjectStatus) -> bool:
        """Update project status."""
        for project in self.projects:
            if project.project_id == project_id:
                project.status = status
                project.last_updated = datetime.now().isoformat()
                return True
        return False
    
    def add_project_feature(self, project_id: str, feature: str, value: bool) -> bool:
        """Mark a project feature as complete (readme, docs, tests, demo)."""
        valid_features = ["has_readme", "has_docs", "has_tests", "has_demo"]
        if feature not in valid_features:
            return False
        
        for project in self.projects:
            if project.project_id == project_id:
                setattr(project, feature, value)
                project.last_updated = datetime.now().isoformat()
                return True
        return False
    
    def get_portfolio_summary(self) -> str:
        """Get portfolio summary and improvement suggestions."""
        lines = ["=" * 70, "GITHUB PORTFOLIO SUMMARY", "=" * 70]
        
        if not self.projects:
            lines.append("\n📝 No projects yet! Start your first project to build your portfolio.")
            return "\n".join(lines)
        
        lines.append(f"\nProjects: {len(self.projects)}")
        
        for project in self.projects:
            lines.append(f"\n▶ {project.name} ({project.status.value})")
            lines.append(f"  URL: {project.repo_url}")
            lines.append(f"  Description: {project.description}")
            lines.append(f"  Skills: {', '.join(project.skills_covered)}")
            
            features = []
            if project.has_readme:
                features.append("✓ README")
            else:
                features.append("○ README (add this!)")
            if project.has_docs:
                features.append("✓ Docs")
            else:
                features.append("○ Docs")
            if project.has_tests:
                features.append("✓ Tests")
            else:
                features.append("○ Tests")
            if project.has_demo:
                features.append("✓ Demo")
            else:
                features.append("○ Demo")
            
            lines.append(f"  Features: {', '.join(features)}")
        
        lines.append("\n💡 PORTFOLIO IMPROVEMENT TIPS")
        lines.append("  • Ensure each project has a polished README with usage instructions")
        lines.append("  • Add test coverage (pytest for Python)")
        lines.append("  • Create a demo notebook or video walkthrough")
        lines.append("  • Write a blog post about your project or learnings")
        lines.append("  • Include architecture diagrams in documentation")
        
        return "\n".join(lines)


class CoachingTipsManager:
    """Generates weekly coaching tips and personalized advice."""
    
    TEMPLATE_TIPS = {
        "learning_strategy": [
            "Learn by doing: Don't just watch videos. Code along and build small projects.",
            "Spaced repetition: Review materials at increasing intervals (1 day, 3 days, 1 week, etc.)",
            "Active recall: Test yourself frequently with flashcards and practice problems.",
            "Mix resources: Combine courses, papers, videos, and hands-on projects for deep learning.",
            "Teach others: Explaining concepts solidifies understanding. Write blog posts or teach a friend.",
            "Deep work: Block 2-3 hour focus sessions for complex topics. Avoid context switching.",
            "Interleaving: Mix topics and problems rather than doing one thing at a time.",
        ],
        "time_management": [
            "Schedule learning like meetings: Block 1.5-2 hour sessions 4-5 times/week (15-20h total).",
            "Morning learning: Your brain is freshest in the morning. Save admin tasks for afternoon.",
            "Use a timer: Pomodoro (25min focused + 5min break) keeps energy high.",
            "Batch similar tasks: Do all flashcard reviews at once, not spread throughout the day.",
            "Track time: Log each session. Awareness helps optimize your schedule.",
            "Weekly review: Every Sunday, plan your learning topics for the upcoming week.",
            "Protect deep focus: Turn off notifications. Use 'Do Not Disturb' during learning blocks.",
        ],
        "portfolio": [
            "Start a project early: Don't wait until you're 'ready'. Imperfect action beats perfect inaction.",
            "Deploy something: A live demo (Hugging Face Spaces, GitHub Pages, Vercel) impresses more than notebooks.",
            "Document well: Great documentation > great code. Recruiters read README first.",
            "Share your learning: Tweet about insights, write Medium posts, or create YouTube videos.",
            "Contribute to open source: Shows collaboration and real-world impact.",
            "Diverse projects: Show breadth (ML basics, NLP, MLOps) and depth (specialized domain).",
            "Polish your repos: Clean code, tests, CI/CD, licenses. Shows professionalism.",
        ],
        "networking": [
            "Join communities: Participate in online forums, Discord/Slack groups, and ML communities.",
            "Attend events: Conferences, webinars, local meetups. Network with peers and senior engineers.",
            "Engage on social media: Follow experts on Twitter/LinkedIn. Share your progress thoughtfully.",
            "Find mentors: Reach out respectfully to senior engineers. Most are happy to help.",
            "Collaborate: Partner on projects with others. Strengthens skills and builds relationships.",
            "Interview prep: Practice with peers. Mock interviews reduce anxiety and improve performance.",
            "Target companies: Follow Alphabet, Meta, OpenAI job boards. Know what skills they want.",
        ],
    }
    
    def __init__(self, tips_list: List[WeeklyTip]):
        self.tips_list = tips_list
    
    def generate_weekly_tips(self, week_num: int, current_focus: str) -> List[WeeklyTip]:
        """Generate weekly tips based on roadmap progress."""
        tips = []
        categories = ["learning_strategy", "time_management", "portfolio", "networking"]
        
        for category in categories:
            template_tips = self.TEMPLATE_TIPS.get(category, [])
            selected_tip = template_tips[week_num % len(template_tips)]
            
            tip = WeeklyTip(
                tip_id=str(uuid.uuid4())[:8],
                week=week_num,
                category=category,
                title=f"{category.replace('_', ' ').title()} Tip",
                content=selected_tip,
                source="template",
            )
            tips.append(tip)
            self.tips_list.append(tip)
        
        return tips
    
    def get_weekly_tips_summary(self) -> str:
        """Get formatted weekly tips."""
        lines = ["=" * 70, "THIS WEEK'S COACHING TIPS", "=" * 70]
        
        # Get most recent tips (within last 7 days)
        recent_tips = self.tips_list[-4:] if self.tips_list else []
        
        if not recent_tips:
            lines.append("\nNo tips generated yet. Use 'coach tips' command to generate weekly guidance.")
        else:
            for tip in recent_tips:
                lines.append(f"\n{tip.category.upper().replace('_', ' ')}")
                lines.append(f"  {tip.content}")
        
        return "\n".join(lines)
