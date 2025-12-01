import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

def get_headers():
    if 'token' in st.session_state and st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def login_user(email, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.user_email = email
            st.session_state.authenticated = True
            return True, "Login successful!"
        else:
            return False, "Invalid credentials"
    except requests.exceptions.RequestException:
        return False, "Connection error. Make sure the API is running."

def register_user(name, email, age, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/register",
            json={"name": name, "email": email, "age": age, "password": password}
        )
        if response.status_code == 200:
            return True, "Registration successful! Please login."
        else:
            error_data = response.json()
            return False, error_data.get("detail", "Registration failed")
    except requests.exceptions.RequestException:
        return False, "Connection error. Make sure the API is running."

def get_todos():
    try:
        response = requests.get(f"{API_BASE_URL}/todos", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException:
        st.error("Error fetching todos")
        return []

def create_todo(title, description=""):
    try:
        response = requests.post(
            f"{API_BASE_URL}/todos",
            json={"title": title, "description": description, "completed": False},
            headers=get_headers()
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def update_todo(todo_id, title, description, completed):
    try:
        response = requests.put(
            f"{API_BASE_URL}/todos/{todo_id}",
            json={"title": title, "description": description, "completed": completed},
            headers=get_headers()
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def delete_todo(todo_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/todos/{todo_id}", headers=get_headers())
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_user_profile():
    try:
        response = requests.get(f"{API_BASE_URL}/profile", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None