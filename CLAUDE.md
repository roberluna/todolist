# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Backend (FastAPI)
```bash
# Run backend server (from project root)
cd backend
python main.py

# OR using uvicorn directly with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Backend runs on http://localhost:8000

### Frontend (Streamlit)
```bash
# Run frontend app (from project root)
cd frontend
streamlit run main.py
```
Frontend runs on http://localhost:8501

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Architecture Overview

This is a **two-tier application** with separate backend (FastAPI REST API) and frontend (Streamlit web UI) communicating via HTTP.

### Backend Structure (FastAPI)
**Entry point**: `backend/main.py` - Initializes FastAPI app and includes routers

**Routers**:
- `api_user.py` - Authentication endpoints (register, login, profile) with JWT tokens
- `api_todo.py` - Todo CRUD endpoints with user authorization

**Key patterns**:
- Both routers duplicate `load_db()`/`save_db()` utilities for JSON file access
- Database path: `../db/db.json` (relative to backend directory)
- `verify_token` dependency (from api_user) used across todo endpoints for auth
- User lookup pattern: email → user_id conversion happens in every endpoint

**Authentication flow**:
1. User registers/logs in → JWT created with email as subject
2. Protected endpoints use `verify_token` dependency → extracts email from JWT
3. Email used to find user_id from database → validates todo ownership

### Frontend Structure (Streamlit)
**Entry point**: `frontend/main.py` - Navigation and session state initialization

**Screen modules** (imported and called based on navigation):
- `auth_screen.py` - Login/register tabbed interface
- `todo_screen.py` - Todo list CRUD operations
- `profile_screen.py` - User statistics and profile display
- `api_client.py` - HTTP client with automatic JWT header injection

**Session state keys** (critical for navigation logic):
- `authenticated` - Boolean, controls which screen to show
- `token` - JWT access token string, stored after login
- `user_email` - Current user's email address

**Navigation pattern**: `main.py` checks `authenticated` state → shows auth screen OR sidebar navigation between todo/profile screens

### API Client Pattern
`api_client.py` provides helper functions that:
1. Auto-inject JWT from `st.session_state.token` via `get_headers()`
2. Handle connection errors uniformly
3. Return (success: bool, message: str) tuples for UI feedback

### Database Schema
Single JSON file at `db/db.json`:
```json
{
  "users": {
    "user_id_uuid": {
      "id": "uuid",
      "name": "string",
      "email": "string",
      "password": "bcrypt_hash"
    }
  },
  "todos": {
    "todo_id_uuid": {
      "id": "uuid",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "user_id": "uuid",
      "created_at": "iso_datetime"
    }
  }
}
```

### Security & Password Handling
- **Bcrypt limitation**: Passwords are truncated to 72 bytes before hashing (see `get_password_hash()` and `verify_password()` in api_user.py)
- **JWT tokens**: Expire after 30 minutes, use hardcoded SECRET_KEY (not production-ready)
- **Authorization**: All todo endpoints verify JWT + check `todo["user_id"]` matches current user
- **Password validation**: Minimum 5 characters enforced in Pydantic model and frontend

## Important Implementation Details

- **Port configuration**: Backend (8000), Frontend (8501) - both hardcoded
- **Database path issue**: Backend uses `../db/db.json` but there's also `backend/db.json` (unused duplicate)
- **No database migrations**: JSON file created on first access if missing
- **Streamlit refresh pattern**: Uses `st.rerun()` after state changes (login/logout)
- **Error handling**: Frontend catches `RequestException` and shows generic "Connection error" message
- **User lookup inefficiency**: Every endpoint iterates through all users to find user_id by email