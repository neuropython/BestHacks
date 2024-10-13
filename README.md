# Brain Bridge

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
