#!/usr/bin/env python3
"""
Generate Month Pages Script
Creates hierarchical month pages for the learning plan
"""

import csv
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

def get_month_theme(month_name: str) -> str:
    """Get the theme for each month"""
    themes = {
        'January': 'ML Basics (Supervised/Unsupervised)',
        'February': 'Deep Learning Fundamentals',
        'March': 'Natural Language Processing',
        'April': 'Computer Vision',
        'May': 'Advanced Deep Learning',
        'June': 'Model Optimization',
        'July': 'MLOps & Deployment',
        'August': 'Reinforcement Learning',
        'September': 'Generative AI',
        'October': 'AI Ethics & Responsible AI',
        'November': 'Advanced Topics & Research',
        'December': 'Capstone Project'
    }
    return themes.get(month_name, 'Advanced AI Topics')

def get_month_navigation(month_name: str) -> tuple:
    """Get previous and next month for navigation"""
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    current_idx = months.index(month_name)
    prev_month = months[current_idx - 1] if current_idx > 0 else None
    next_month = months[current_idx + 1] if current_idx < 11 else None

    return prev_month, next_month

def generate_month_html(month_name: str, weeks_data: List[Dict]) -> str:
    """Generate HTML content for a month page"""

    theme = get_month_theme(month_name)
    prev_month, next_month = get_month_navigation(month_name)

    # Calculate starting week number for this month
    month_order = {
        'January': 1, 'February': 5, 'March': 9, 'April': 13,
        'May': 17, 'June': 21, 'July': 25, 'August': 29,
        'September': 33, 'October': 37, 'November': 41, 'December': 45
    }
    start_week = month_order[month_name]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{month_name} 2026 - AI Growth Engine</title>
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
        .month-info {{
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2em;
            margin-bottom: 30px;
        }}
        .weeks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .week-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            text-decoration: none;
            color: #495057;
            transition: all 0.3s ease;
            display: block;
        }}
        .week-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #667eea;
        }}
        .week-number {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .week-title {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .week-description {{
            font-size: 0.9em;
            color: #6c757d;
            margin-bottom: 15px;
        }}
        .week-topics {{
            font-size: 0.9em;
            color: #495057;
        }}
        .week-topics ul {{
            margin: 10px 0 0 0;
            padding-left: 20px;
        }}
        .week-topics li {{
            margin: 5px 0;
            position: relative;
        }}
        .week-topics li::marker {{
            color: #667eea;
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
        .month-progress {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>📅 {month_name} 2026</h1>
        <div class="month-info">{theme}</div>

        <div class="month-progress">
            <h3>Monthly Progress</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="monthProgress"></div>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number" id="completedWeeks">0</div>
                    <div class="stat-label">Weeks Completed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">4</div>
                    <div class="stat-label">Total Weeks</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="monthPercent">0%</div>
                    <div class="stat-label">Complete</div>
                </div>
            </div>
        </div>

        <div class="weeks-grid">
"""

    # Add week cards
    for i, week_data in enumerate(weeks_data):
        week_num = start_week + i
        html += f"""            <a href="week{week_num}/index.html" class="week-card">
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

    # Navigation buttons
    html += """        </div>

        <div class="navigation-buttons">
"""

    if prev_month:
        html += f"""            <a href="{prev_month.lower()}.html" class="nav-button">← {prev_month}</a>
"""

    html += """            <a href="index.html" class="nav-button primary">🏠 Year Overview</a>
"""

    if next_month:
        html += f"""            <a href="{next_month.lower()}.html" class="nav-button secondary">{next_month} →</a>
"""

    html += f"""        </div>
    </div>

    <script>
        // Load progress from localStorage
        window.onload = function() {{
            let completedWeeks = 0;
            for (let week = {start_week}; week < {start_week + 4}; week++) {{
                const weekProgress = localStorage.getItem(`week${{week}}_progress`);
                if (weekProgress && JSON.parse(weekProgress).percentage >= 80) {{
                    completedWeeks++;
                }}
            }}

            const monthPercent = Math.round((completedWeeks / 4) * 100);
            document.getElementById('monthProgress').style.width = monthPercent + '%';
            document.getElementById('completedWeeks').textContent = completedWeeks;
            document.getElementById('monthPercent').textContent = monthPercent + '%';
        }};
    </script>
</body>
</html>"""

    return html

def main():
    print("📅 Generating hierarchical month pages...")

    # Load yearly plan
    yearly_plan = load_yearly_plan()

    # Group weeks by month
    months_data = {}
    for week in yearly_plan:
        month = week['Month']
        if month not in months_data:
            months_data[month] = []
        months_data[month].append(week)

    learning_plan_dir = Path('learning_plan')

    # Generate month pages
    for month_name, weeks_data in months_data.items():
        print(f"📝 Generating {month_name}.html with {len(weeks_data)} weeks")

        month_html = generate_month_html(month_name, weeks_data)
        month_file = learning_plan_dir / f"{month_name.lower()}.html"
        month_file.write_text(month_html)

    print("✅ Month pages generation complete!")

if __name__ == '__main__':
    main()