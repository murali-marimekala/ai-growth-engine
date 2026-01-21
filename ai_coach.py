"""
OpenAI integration for personalized AI coaching.
Optional module - works when OPENAI_API_KEY is provided in .env
"""

import os
from typing import Optional, List, Dict
from dotenv import load_dotenv


class AICoach:
    """Optional AI mentor powered by OpenAI API."""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.enabled = self.api_key is not None
        self.client = None
        
        if self.enabled:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️  OpenAI package not installed. Install with: pip install openai")
                self.enabled = False
    
    def analyze_progress(self, sessions_summary: str, current_focus: str) -> Optional[str]:
        """Analyze user progress and provide personalized insights."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""
You are an expert AI/ML career coach helping someone transition from engineering management to AI/ML roles at top companies (Alphabet, Meta, OpenAI, Tesla, Netflix).

Current Learning Status:
{sessions_summary}

Current Focus Area: {current_focus}

Based on this progress, provide:
1. Specific strengths to build on
2. Areas to focus more on
3. 2-3 concrete next steps for this week
4. One resource recommendation

Keep it concise (< 150 words), actionable, and encouraging.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI/ML career coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def generate_personalized_tips(self, progress_data: Dict) -> Optional[str]:
        """Generate personalized learning tips based on progress patterns."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""
You are an AI/ML career coach. Analyze this progress data and generate 3 personalized tips for the next week:

Progress Summary:
- Current Streak: {progress_data.get('current_streak', 0)} days
- Total Hours: {progress_data.get('total_hours', 0):.1f}
- Recent Topics: {', '.join(progress_data.get('recent_topics', []))}
- Current Learning Phase: {progress_data.get('current_phase', 'Foundations')}

Generate 3 specific, actionable tips that build on their momentum and address potential challenges.
Format as a numbered list. Keep it motivational but realistic.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI/ML career coach focused on practical, actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.8,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def suggest_resources(self, topic: str, difficulty: str, learning_style: str = "mixed") -> Optional[str]:
        """Suggest resources for a specific topic."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""
You are an expert in ML/AI education. Suggest 3-4 FREE or low-cost resources for learning: {topic}

Requirements:
- Difficulty level: {difficulty}
- Learning style: {learning_style} (e.g., video, article, interactive, project-based)
- Mostly free resources (MIT OpenCourseWare, ArXiv papers, GitHub repos, YouTube)
- Include direct links where possible

Format:
1. [Title] (type) - description with direct link

Focus on high-quality, well-reviewed resources.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert ML educator recommending free, high-quality learning resources."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def generate_flashcards(self, topic: str, num_cards: int = 5) -> Optional[List[Dict[str, str]]]:
        """Generate flashcard suggestions for a topic."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""
Generate {num_cards} flashcard questions and answers for the topic: {topic}

Requirements:
- Questions should be clear and specific
- Answers should be concise but complete (2-3 sentences max)
- Include both conceptual and practical knowledge
- Avoid yes/no questions

Format as JSON list: [{{\"question\": \"...\", \"answer\": \"...\"}}]

Return ONLY the JSON, no other text.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Generate flashcard content. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7,
            )
            
            import json
            response_text = response.choices[0].message.content
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return None
    
    def interview_prep(self, role_level: str = "mid-level", company: str = "top-tier") -> Optional[str]:
        """Generate interview preparation advice."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""
Generate interview prep advice for someone transitioning to {role_level} AI/ML roles at {company} companies like Alphabet, Meta, OpenAI, Tesla.

Include:
1. Top 5 system design topics to practice (with brief explanation)
2. 3 common ML design interview questions they might face
3. How to approach portfolio projects to strengthen interview candidacy
4. Communication tips for discussing past experience in engineering management context

Keep it practical and specific. Total ~300 words.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI/ML recruiting coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating interview prep: {e}")
            return None
    
    def get_status_message(self) -> str:
        """Check if AI Coach is enabled."""
        if self.enabled:
            return "✓ AI Coach enabled! Advanced personalization available."
        else:
            return "○ AI Coach disabled. Add OPENAI_API_KEY to .env to enable personalized coaching."
