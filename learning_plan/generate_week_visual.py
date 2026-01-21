# generate_week_visual.py
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env")
    sys.exit(1)

from openai import OpenAI
client = OpenAI(api_key=api_key)

def generate_week_visual(week_num):
    # Assume week data from roadmap (hardcoded for weeks 1-3; in real use, import from coach)
    weeks = {
        1: {"name": "Intro to ML & Data Preprocessing", "description": "Intro to ML & Data Preprocessing"},
        2: {"name": "Linear & Logistic Regression", "description": "Linear & Logistic Regression"},
        3: {"name": "Decision Trees & Random Forests", "description": "Decision Trees & Random Forests"}
    }
    if week_num not in weeks:
        print(f"Week {week_num} not defined.")
        return

    week = weeks[week_num]
    week_dir = Path(f"learning_plan/week{week_num}")
    week_dir.mkdir(exist_ok=True)

    # Generate text roadmap using GPT
    prompt_text = f"Create a concise text roadmap for Week {week_num}: {week['name']} - {week['description']}. Include 3-5 key steps."
    response_text = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=200
    )
    roadmap_text = response_text.choices[0].message.content.strip()

    # Generate image using DALL-E
    prompt_image = f"Create a visual roadmap illustration for AI/ML learning week: {week['name']} - {week['description']}. Style: clean, modern infographic."
    response_image = client.images.generate(
        model="dall-e-3",
        prompt=prompt_image,
        size="1024x1024",
        n=1
    )
    image_url = response_image.data[0].url
    # Download and save image (using requests; add to requirements if needed)
    import requests
    img_data = requests.get(image_url).content
    with open(week_dir / "roadmap.png", "wb") as f:
        f.write(img_data)

    # Generate HTML snippet with animation
    html_snippet = f"""
    <div class="roadmap-container">
      <h2>Week {week_num} Roadmap</h2>
      <img src="roadmap.png" alt="Roadmap for Week {week_num}" class="animated-roadmap">
      <p>{roadmap_text}</p>
    </div>
    <style>
      .animated-roadmap {{
        animation: fadeIn 2s ease-in;
      }}
      @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
      }}
    </style>
    """
    with open(week_dir / "roadmap_snippet.html", "w") as f:
        f.write(html_snippet)

    print(f"Generated visual for week {week_num}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python learning_plan/generate_week_visual.py <week_num>")
        sys.exit(1)
    generate_week_visual(int(sys.argv[1]))