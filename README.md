<h1 align="center">
  Brain Bridge
</h1>

## Overview
This FastAPI application provides API endpoints for managing users, notes, and announcements, with search functionalities and AI-based project selection. It utilizes middleware for CORS, connects to a database, and integrates an AI model to answer user questions based on project titles stored in a file.

## Features
- User creation and authentication
- Announcement management
- Note sending and retrieval
- Search functionality using various search engines
- AI-powered project title suggestion based on user input

## Requirements
- **Python 3.7+**
- **FastAPI** - A modern web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Pydantic** - For data validation and settings management using Python type annotations.
- **Ollama** - For integrating and querying the LLaMA AI model.
- **CORS Middleware** - To allow cross-origin resource sharing.
  
Install the required dependencies:
```bash
pip install fastapi uvicorn pydantic
```

## Project Structure
- **`db.py`** - Handles database operations for users, notes, and announcements.
- **`models/`** - Contains the data models for `User`, `Note`, and `Announcement`.
- **`search_engines.py`** - Contains the search engine logic and filters.
- **`ollama.py`** - Integration with the LLaMA model for AI-powered suggestions.
- **`annoucement_data.txt`** - A text file that contains project titles used by the AI to answer user queries.

## How to Run
1. Clone the repository and install dependencies.
2. Run the FastAPI app using Uvicorn:

```bash
uvicorn main:app --reload
