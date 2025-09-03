# AI Agents Course - Practical Exercises

This repository contains practical exercises for the **Robot Dreams AI Agents** course. Each homework assignment is organized in its own subfolder.

## Course Information
- **Course**: Robot Dreams AI Agents
- **Type**: Practical Exercises (Praktické cvičení)
- **Language**: Python
- **Focus**: Large Language Models (LLMs), API integration, tool usage

## Homework Structure

Each homework is contained in its own subfolder:

### HW1 - First Exercise: LLM API Integration with Tools
**Link**: [HW1/](HW1/)

**Description (Zadání)**:
```
Napiš Python skript, který zavolá LLM API, použije nástroj (např. výpočetní funkci) a
vrátí odpověď zpět LLM.
```

**English Translation**:
Write a Python script that calls an LLM API, uses a tool (e.g., computational function), and returns the response back to the LLM.

**Implementation Details**:
- Uses OpenAI's GPT-4o model
- Implements custom tools for:
  - Stock price retrieval (Yahoo Finance)
  - Weather information (OpenWeatherMap with Open-Meteo fallback)
  - Web search (Tavily API)
- Demonstrates function calling capabilities
- Includes comprehensive testing suite

**Submission Format**:
The completed assignment should be submitted as source code. Ideally, upload the project to GitHub and submit the GitHub repository link. Submit the link in Google Classroom.

## Technologies Used
- Python 3.12+
- OpenAI API
- Yahoo Finance API
- OpenWeatherMap API / Open-Meteo API
- Tavily Search API
- UV (Python package manager)

## Setup Instructions
1. Clone the repository
2. Navigate to the desired homework folder
3. Install dependencies: `uv sync`
4. Set up environment variables in `.env` file
5. Run the application: `uv run python main.py`

## Future Homework Assignments
Additional homework assignments will be added as subfolders (HW2, HW3, etc.) as the course progresses.

---
*Robot Dreams AI Agents Course - Practical Exercises Repository*
