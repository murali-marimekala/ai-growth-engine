#!/usr/bin/env python3
"""
Expand Learning Plan Script
Generates missing weeks (8-48) based on 2027_AIML.txt yearly plan
"""

import csv
import os
import json
from pathlib import Path
from typing import Dict, List

def load_yearly_plan() -> List[Dict]:
    """Load the comprehensive yearly plan from 2027_AIML.txt"""
    yearly_plan = []
    with open('__pycache__/2027_AIML.txt', 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            yearly_plan.append(row)
    return yearly_plan

def get_week_number(month: str, week_in_month: int) -> int:
    """Convert month + week_in_month to global week number"""
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    month_num = month_order[month]
    return (month_num - 1) * 4 + week_in_month

def generate_week_index_html(week_data: Dict, week_num: int) -> str:
    """Generate HTML content for a week index page"""
    theme = week_data['Theme']
    topic = week_data['Topic']
    mini_project = week_data['Mini-Project']

    # Generate day topics based on the week's focus
    day_topics = generate_day_topics(topic)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Week {week_num}: {topic}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .week-info {{
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2em;
            margin-bottom: 30px;
        }}
        .days-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .day-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            text-decoration: none;
            color: #495057;
            transition: all 0.3s ease;
            display: block;
        }}
        .day-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #667eea;
        }}
        .day-number {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .day-title {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .day-description {{
            font-size: 0.9em;
            color: #6c757d;
            margin-bottom: 15px;
        }}
        .mini-project {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }}
        .mini-project h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .navigation-buttons {{
            margin-top: 30px;
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .nav-button {{
            padding: 12px 25px;
            background: #6c757d;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }}
        .nav-button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .nav-button.primary {{
            background: #007bff;
        }}
        .nav-button.secondary {{
            background: #28a745;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Week {week_num}</h1>
        <div class="week-info">
            <strong>{topic}</strong><br>
            Theme: {theme}
        </div>

        <div class="mini-project">
            <h3>🎯 Mini-Project</h3>
            <p>{mini_project}</p>
        </div>

        <div class="days-grid">
"""

    # Add day cards
    for day in range(1, 8):
        day_topic = day_topics[day-1] if day-1 < len(day_topics) else f"Day {day} Practice"
        html += f"""            <a href="day{day}/index.html" class="day-card">
                <div class="day-number">Day {day}</div>
                <div class="day-title">{day_topic}</div>
                <div class="day-description">Interactive learning module with flashcards and progress tracking</div>
            </a>
"""

    # Navigation buttons
    prev_week = week_num - 1 if week_num > 1 else None
    next_week = week_num + 1 if week_num < 48 else None

    html += """        </div>

        <div class="navigation-buttons">
"""

    if prev_week:
        html += f"""            <a href="../week{prev_week}/index.html" class="nav-button">← Week {prev_week}</a>
"""

    html += """            <a href="../index.html" class="nav-button primary">🏠 Home</a>
"""

    if next_week:
        html += f"""            <a href="../week{next_week}/index.html" class="nav-button secondary">Week {next_week} →</a>
"""

    html += """        </div>
    </div>
</body>
</html>"""

    return html

def generate_day_topics(week_topic: str) -> List[str]:
    """Generate 7 day topics based on week focus"""
    topic_mapping = {
        "Intro to ML & Data Preprocessing": [
            "ML Concepts & Terminology", "Data Loading & Exploration", "Data Cleaning & Preprocessing",
            "Feature Engineering", "Data Visualization", "Statistical Analysis", "Mini-Project Setup"
        ],
        "Linear & Logistic Regression": [
            "Linear Regression Theory", "Gradient Descent", "Logistic Regression Basics",
            "Regularization Techniques", "Model Evaluation Metrics", "Cross-Validation", "Regression Project"
        ],
        "Decision Trees & Random Forests": [
            "Decision Tree Fundamentals", "Tree Pruning & Optimization", "Random Forest Algorithm",
            "Feature Importance Analysis", "Gradient Boosting Machines", "Ensemble Evaluation", "Tree-Based Project"
        ]
    }

    # Default day structure for new weeks
    if week_topic in topic_mapping:
        return topic_mapping[week_topic]

    # Generic structure for new topics
    return [
        f"{week_topic} - Fundamentals",
        f"{week_topic} - Core Concepts",
        f"{week_topic} - Implementation",
        f"{week_topic} - Advanced Techniques",
        f"{week_topic} - Best Practices",
        f"{week_topic} - Evaluation & Metrics",
        f"{week_topic} - Mini-Project"
    ]

def generate_day_html(week_num: int, day_num: int, day_topic: str, week_topic: str) -> str:
    """Generate HTML for individual day pages"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Week {week_num} - Day {day_num}: {day_topic}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .day-subtitle {{
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2em;
            margin-bottom: 30px;
        }}
        .content-section {{
            margin: 30px 0;
        }}
        .content-section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .flashcard-container {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .flashcard {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .flashcard:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-color: #667eea;
        }}
        .flashcard.flipped {{
            background: #667eea;
            color: white;
        }}
        .flashcard-question {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        .flashcard-answer {{
            display: none;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #dee2e6;
        }}
        .flashcard.flipped .flashcard-answer {{
            display: block;
        }}
        .flashcard.flipped .flashcard-answer {{
            border-top-color: rgba(255,255,255,0.3);
        }}
        .progress-section {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            width: 0%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }}
        .navigation-buttons {{
            margin-top: 20px;
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .nav-button {{
            padding: 10px 20px;
            background: #6c757d;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }}
        .nav-button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .nav-button.next {{
            background: #007bff;
        }}
        .nav-button.home {{
            background: #6c757d;
        }}
        .nav-button.prev {{
            background: #6c757d;
        }}
        .completion-form {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .completion-form h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .checkbox-item {{
            display: flex;
            align-items: center;
            margin: 10px 0;
        }}
        .checkbox-item input {{
            margin-right: 10px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            text-align: center;
        }}
        .stat-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        .stat-number {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        @media (max-width: 768px) {{
            .navigation-buttons {{
                flex-direction: column;
                align-items: center;
            }}
            .nav-button {{
                width: 200px;
            }}
            h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Week {week_num} - Day {day_num}</h1>
        <div class="day-subtitle">{day_topic}</div>

        <div class="content-section">
            <h2>🎯 Today's Learning Objectives</h2>
            <ul>
                <li>Understanding core concepts of {day_topic.lower()}</li>
                <li>Practical implementation and examples</li>
                <li>Common pitfalls and best practices</li>
                <li>Integration with broader {week_topic.lower()} context</li>
            </ul>
        </div>

        <div class="flashcard-container">
            <h2>🃏 Key Concepts Flashcards</h2>
            <div class="flashcard" onclick="flipCard(this)">
                <div class="flashcard-question">What are the fundamental concepts of {day_topic.lower()}?</div>
                <div class="flashcard-answer">This covers the core principles and building blocks of {day_topic.lower()}. Key concepts include [specific details to be added based on topic expertise].</div>
            </div>
            <div class="flashcard" onclick="flipCard(this)">
                <div class="flashcard-question">How does {day_topic.lower()} relate to {week_topic.lower()}?</div>
                <div class="flashcard-answer">{day_topic} is a crucial component of {week_topic.lower()}. It provides [relationship explanation to be customized per topic].</div>
            </div>
            <div class="flashcard" onclick="flipCard(this)">
                <div class="flashcard-question">What are common challenges in {day_topic.lower()}?</div>
                <div class="flashcard-answer">Common challenges include [specific challenges]. Best practices involve [recommended approaches].</div>
            </div>
            <div class="flashcard" onclick="flipCard(this)">
                <div class="flashcard-question">How to evaluate {day_topic.lower()} implementations?</div>
                <div class="flashcard-answer">Evaluation metrics include [relevant metrics]. Success indicators are [key success factors].</div>
            </div>
        </div>

        <div class="progress-section">
            <h2>📊 Learning Progress</h2>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number" id="completedCards">0</div>
                    <div class="stat-label">Cards Reviewed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="totalCards">4</div>
                    <div class="stat-label">Total Cards</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="progressPercent">0%</div>
                    <div class="stat-label">Complete</div>
                </div>
            </div>
        </div>

        <div class="completion-form">
            <h3>✅ Mark Your Progress</h3>
            <form id="completionForm">
                <div class="checkbox-item">
                    <input type="checkbox" id="concept1" onchange="updateProgress()">
                        <label for="concept1">Reviewed core concepts of {day_topic.lower()}</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="concept2" onchange="updateProgress()">
                        <label for="concept2">Completed practical exercises</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="concept3" onchange="updateProgress()">
                        <label for="concept3">Understood common challenges and solutions</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="concept4" onchange="updateProgress()">
                        <label for="concept4">Applied concepts to mini-project</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="concept5" onchange="updateProgress()">
                        <label for="concept5">Reviewed and consolidated learning</label>
                </div>
            </form>
        </div>

        <div class="content-section">
            <h2>🚀 Next Steps</h2>
            <p>Great work on {day_topic}! {"Tomorrow we'll continue with " + ("Week " + str(week_num) + " concepts" if day_num < 7 else "the next week")}. </p>
            <p><strong>Log your session:</strong> <code>python coach.py log 2.5 "{day_topic}"</code></p>
        </div>

        <div class="navigation-buttons">
"""

    # Navigation logic
    if day_num > 1:
        html += f"""            <button onclick="window.location.href='../day{day_num-1}/index.html'" class="nav-button prev">← Day {day_num-1}</button>
"""
    elif week_num > 1:
        html += f"""            <button onclick="window.location.href='../../week{week_num-1}/day7/index.html'" class="nav-button prev">← Week {week_num-1} Day 7</button>
"""

    html += """            <button onclick="window.location.href='../../index.html'" class="nav-button home">🏠 Home</button>
"""

    if day_num < 7:
        html += f"""            <button onclick="window.location.href='../day{day_num+1}/index.html'" class="nav-button next">→ Day {day_num+1}</button>
"""
    elif week_num < 48:
        html += f"""            <button onclick="window.location.href='../../week{week_num+1}/day1/index.html'" class="nav-button next">→ Week {week_num+1} Day 1</button>
"""

    html += """        </div>
    </div>

    <script>
        function flipCard(card) {
            card.classList.toggle('flipped');
            updateProgress();
        }

        function updateProgress() {
            const checkboxes = document.querySelectorAll('#completionForm input[type="checkbox"]');
            const checkedCount = document.querySelectorAll('#completionForm input[type="checkbox"]:checked').length;
            const totalCount = checkboxes.length;
            const flashcards = document.querySelectorAll('.flashcard.flipped').length;
            const totalFlashcards = document.querySelectorAll('.flashcard').length;

            const progressPercent = Math.round(((checkedCount / totalCount) + (flashcards / totalFlashcards)) / 2 * 100);

            document.getElementById('progressFill').style.width = progressPercent + '%';
            document.getElementById('completedCards').textContent = flashcards;
            document.getElementById('progressPercent').textContent = progressPercent + '%';

            // Save progress to localStorage
            const progress = {{
                checkboxes: checkedCount,
                flashcards: flashcards,
                percentage: progressPercent,
                timestamp: new Date().toISOString()
            }};
            localStorage.setItem('week{week_num}_day{day_num}_progress', JSON.stringify(progress));
        }

        // Load saved progress on page load
        window.onload = function() {{
            const saved = localStorage.getItem('week{week_num}_day{day_num}_progress');
            if (saved) {{
                const progress = JSON.parse(saved);
                document.getElementById('progressFill').style.width = progress.percentage + '%';
                document.getElementById('completedCards').textContent = progress.flashcards;
                document.getElementById('progressPercent').textContent = progress.percentage + '%';
            }}
        }};
    </script>
</body>
</html>"""

    return html

def update_main_index(yearly_plan: List[Dict]) -> None:
    """Update the main index.html to show all 48 weeks organized by month"""

    # Group weeks by month
    months = {}
    for week in yearly_plan:
        month = week['Month']
        if month not in months:
            months[month] = []
        week_num = get_week_number(month, int(week['Week'].split()[-1]))
        months[month].append({
            'week_num': week_num,
            'data': week
        })

    # Generate month sections
    month_html = ""
    for month, weeks in months.items():
        month_html += f"""
        <div class="month-section">
            <h2 class="month-title">📅 {month} 2026</h2>
            <div class="month-description">{weeks[0]['data']['Theme']}</div>
            <div class="weeks-grid">
"""

        for week_info in weeks:
            week_num = week_info['week_num']
            week_data = week_info['data']
            month_html += f"""                <a href="week{week_num}/index.html" class="week-card">
                    <div class="week-number">Week {week_num}</div>
                    <div class="week-title">{week_data['Topic']}</div>
                    <div class="week-description">{week_data['Mini-Project']}</div>
                    <div class="week-topics">
                        <ul>
                            <li>Day 1-7 Interactive Modules</li>
                            <li>Flashcards & Progress Tracking</li>
                            <li>Hands-on Implementation</li>
                            <li>{week_data['Mini-Project']}</li>
                        </ul>
                    </div>
                </a>
"""

        month_html += """            </div>
        </div>
"""

    # Update the main index.html
    with open('learning_plan/index.html', 'r') as f:
        content = f.read()

    # Replace the weeks grid section
    old_weeks_section = content.split('<div class="weeks-grid">')[1].split('</div>\n\n        <div class="cta-section">')[0]
    new_content = content.replace(
        f'<div class="weeks-grid">{old_weeks_section}</div>',
        month_html
    )

    # Update progress stats
    new_content = new_content.replace(
        'Week 1 of 7 completed • 14% of yearly journey',
        'Comprehensive 48-week ML journey'
    )
    new_content = new_content.replace(
        '7',
        '48'
    )

    with open('learning_plan/index.html', 'w') as f:
        f.write(new_content)

def main():
    print("🚀 Expanding Learning Plan to match 2027_AIML.txt yearly roadmap...")

    # Load yearly plan
    yearly_plan = load_yearly_plan()
    print(f"📋 Loaded {len(yearly_plan)} weeks from yearly plan")

    # Generate missing weeks (8-48)
    learning_plan_dir = Path('learning_plan')

    for week_data in yearly_plan:
        month = week_data['Month']
        week_in_month = int(week_data['Week'].split()[-1])
        week_num = get_week_number(month, week_in_month)

        # Skip weeks 1-7 (already exist)
        if week_num <= 7:
            continue

        print(f"📝 Generating Week {week_num}: {week_data['Topic']}")

        # Create week directory
        week_dir = learning_plan_dir / f'week{week_num}'
        week_dir.mkdir(exist_ok=True)

        # Generate week index.html
        week_html = generate_week_index_html(week_data, week_num)
        (week_dir / 'index.html').write_text(week_html)

        # Generate day pages
        day_topics = generate_day_topics(week_data['Topic'])
        for day_num in range(1, 8):
            day_dir = week_dir / f'day{day_num}'
            day_dir.mkdir(exist_ok=True)

            day_topic = day_topics[day_num-1] if day_num-1 < len(day_topics) else f"Day {day_num} Practice"
            day_html = generate_day_html(week_num, day_num, day_topic, week_data['Topic'])

            (day_dir / 'index.html').write_text(day_html)

    print("📊 Updating main index.html to show all weeks...")
    update_main_index(yearly_plan)

    print("✅ Learning plan expansion complete!")
    print(f"📈 Now have {len(yearly_plan)} weeks total (was 7, now {len(yearly_plan)})")
    print("🌐 Start the web server: cd learning_plan && python3 -m http.server 8000")

if __name__ == '__main__':
    main()