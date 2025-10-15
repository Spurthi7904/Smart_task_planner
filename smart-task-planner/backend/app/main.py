import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import requests

app = FastAPI(title="Smart Task Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    estimated_hours: Optional[int] = None
    priority: str = "medium"
    status: str = "pending"

class TaskBreakdownRequest(BaseModel):
    goal: str
    timeframe: Optional[str] = None

class TaskBreakdownResponse(BaseModel):
    goal_id: str
    tasks: List[Task]
    reasoning: str
    total_estimated_hours: int

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Use ACTUAL available models from your list
        self.possible_models = [
            "gemini-2.0-flash",  # Fast and reliable
            "gemini-2.0-flash-001",
            "gemini-2.0-flash-lite", 
            "gemini-2.0-flash-lite-001",
            "gemini-pro-latest",  # This should work!
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ]
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        print("✅ AI Service initialized with correct Gemini models!")

    def break_down_goal(self, goal: str, timeframe: str = None):
        """Try different ACTUAL Gemini model endpoints"""
        
        for model_name in self.possible_models:
            try:
                result = self._try_model(model_name, goal, timeframe)
                if result:
                    print(f"✅ SUCCESS with model: {model_name}")
                    return result
            except Exception as e:
                print(f"❌ Failed with {model_name}: {str(e)[:100]}...")
                continue
        
        # If all models fail, use smart generator
        print("🚨 All Gemini models failed, using smart generator")
        return self._create_smart_tasks(goal, timeframe)

    def _try_model(self, model_name: str, goal: str, timeframe: str = None):
        """Try a specific Gemini model"""
        api_url = f"{self.base_url}/{model_name}:generateContent?key={self.api_key}"
        
        prompt = self._build_prompt(goal, timeframe)
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 800,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        print(f"🔧 Trying: {model_name}")
        response = requests.post(api_url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if "candidates" in result and result["candidates"]:
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"📝 Raw AI response received")
                return self._parse_ai_response(content, goal)
            else:
                raise Exception("No candidates in response")
        else:
            raise Exception(f"HTTP {response.status_code}")

    def _build_prompt(self, goal: str, timeframe: str) -> str:
        return f"""You are an expert project planner. Break this goal into 3-5 specific, actionable tasks with realistic time estimates.

GOAL: {goal}
{f"TIMEFRAME: {timeframe}" if timeframe else "TIMEFRAME: Flexible"}

Return ONLY valid JSON with this exact structure:
{{
    "reasoning": "Brief explanation of your approach",
    "tasks": [
        {{
            "title": "Specific, actionable task name",
            "description": "Detailed description of what needs to be done", 
            "estimated_hours": 2,
            "priority": "high"
        }}
    ]
}}

Requirements:
- Make tasks practical and sequential
- Ensure total estimated hours are appropriate for the timeframe
- Return ONLY the JSON, no other text
- Use double quotes for JSON properties"""

    def _parse_ai_response(self, content: str, goal: str):
        # Clean the response
        content = content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith('```json'):
            content = content[7:]
        elif content.startswith('```'):
            content = content[3:]
        
        if content.endswith('```'):
            content = content[:-3]
            
        content = content.strip()
        
        print(f"🧹 Cleaned content: {content}")
        
        try:
            # Parse JSON
            data = json.loads(content)
            
            # Build tasks
            tasks = []
            for i, task_data in enumerate(data.get("tasks", [])):
                tasks.append({
                    "id": str(i + 1),
                    "title": task_data["title"],
                    "description": task_data["description"],
                    "estimated_hours": task_data["estimated_hours"],
                    "priority": task_data["priority"],
                    "status": "pending"
                })
            
            total_hours = sum(task["estimated_hours"] for task in tasks)
            
            return {
                "reasoning": data["reasoning"],
                "tasks": tasks,
                "total_estimated_hours": total_hours
            }
        except json.JSONDecodeError as e:
            print(f" JSON parse error: {e}")
            print(f" Problematic content: {content}")
            raise Exception("Failed to parse AI response as JSON")

    def _create_smart_tasks(self, goal: str, timeframe: str = None):
        """Fallback smart generator"""
        total_hours = self._parse_timeframe(timeframe)
        
        return {
            "reasoning": f"Smart task breakdown for '{goal}' (Gemini API unavailable)",
            "tasks": [
                {
                    "id": "1",
                    "title": f"Research and plan {goal}",
                    "description": "Initial research and planning phase",
                    "estimated_hours": max(1, total_hours // 4),
                    "priority": "high",
                    "status": "pending"
                },
                {
                    "id": "2",
                    "title": f"Practice core skills for {goal}",
                    "description": "Hands-on practice and skill development",
                    "estimated_hours": max(1, total_hours // 2),
                    "priority": "medium",
                    "status": "pending"
                },
                {
                    "id": "3",
                    "title": f"Apply and refine {goal}",
                    "description": "Practical application and improvement",
                    "estimated_hours": max(1, total_hours // 4),
                    "priority": "medium",
                    "status": "pending"
                }
            ],
            "total_estimated_hours": total_hours
        }

    def _parse_timeframe(self, timeframe: str) -> int:
        """Convert timeframe to hours"""
        if not timeframe:
            return 8
            
        timeframe = timeframe.lower()
        numbers = [int(s) for s in timeframe.split() if s.isdigit()]
        number = numbers[0] if numbers else 1
        
        if 'minute' in timeframe:
            return max(1, number // 60)
        elif 'hour' in timeframe:
            return number
        elif 'day' in timeframe:
            return number * 8
        elif 'week' in timeframe:
            return number * 40
        elif 'month' in timeframe:
            return number * 160
        else:
            return 8

# Initialize AI service
ai_service = AIService()

@app.post("/api/v1/breakdown", response_model=TaskBreakdownResponse)
async def create_task_breakdown(request: TaskBreakdownRequest):
    """Use AI to generate task breakdown"""
    print(f"🎯 Processing goal: {request.goal}")
    breakdown = ai_service.break_down_goal(request.goal, request.timeframe)
    
    return TaskBreakdownResponse(
        goal_id="gemini-plan-123",
        tasks=breakdown["tasks"],
        reasoning=breakdown["reasoning"],
        total_estimated_hours=breakdown["total_estimated_hours"]
    )

@app.get("/")
async def root():
    return {"message": "Smart Task Planner API with Google Gemini AI!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)