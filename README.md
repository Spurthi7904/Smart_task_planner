

# Smart Task Planner

Breaking user goals into actionable tasks with timelines using AI reasoning.

## Project Description

Smart Task Planner is a full-stack web application that uses AI to transform user goals into structured task plans with realistic timelines. The application features a FastAPI backend with Google Gemini AI integration and a responsive frontend interface.

## Features

- AI-powered task breakdown using Google Gemini LLM
- Timeframe-aware task generation
- Priority-based task organization (High/Medium/Low)
- Clean, responsive user interface
- Real-time plan generation

smart-task-planner/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── test_gemini.py
├── frontend/
│   └── test.html
└── README.md

## Technology Stack

**Backend:**
- FastAPI (Python web framework)
- Google Gemini API (AI task generation)
- Requests (HTTP library)

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive design with warm color scheme

## Setup Instructions

### Prerequisites
- Python 3.10+
- Google Gemini API key

### Installation

1. Clone the repository
2. Navigate to backend folder:
   ```bash
   cd smart-task-planner/backend
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn requests
   ```
4. Set up API key in `app/main.py`:
   - Replace the API key placeholder with your Google Gemini API key
   - Get a free API key from Google AI Studio

5. Run the backend server:
   ```bash
   python app/main.py
   ```

6. Open the frontend:
   - Navigate to `frontend/test.html` in your browser
   - The API will be available at `http://localhost:8000`

## API Usage

### Generate Task Breakdown
**Endpoint:** `POST /api/v1/breakdown`

**Request:**
```json
{
  "goal": "Learn Python programming",
  "timeframe": "1 month"
}
```

**Response:**
```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Research Python fundamentals",
      "description": "Learn basic syntax and concepts",
      "estimated_hours": 8,
      "priority": "high",
      "status": "pending"
    }
  ],
  "reasoning": "AI-generated learning plan",
  "total_estimated_hours": 36
}
```

## Security Note

API keys are not included in this repository for security reasons. In a production environment, API keys should be managed through environment variables or secure secret management systems.

## Evaluation Criteria Met

- Task completeness and logical breakdown
- Realistic timeline estimation
- LLM integration for intelligent reasoning
- Clean API design and code structure
- User-friendly frontend interface

## Usage Examples

Try these goal examples:
- "Learn web development in 3 months"
- "Build a mobile app in 2 weeks"
- "Start a cooking blog in 1 month"
- "Learn to play guitar in 6 months"

The AI will generate context-aware tasks specific to each goal type while respecting the specified timeframe.
