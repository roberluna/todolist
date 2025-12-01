import streamlit as st
from api_client import get_user_profile, get_todos

def profile_screen():
    st.title("👤 User Profile")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        profile_data = get_user_profile()
        display_name = profile_data['name'] if profile_data else st.session_state.user_email
        st.write(f"Welcome to your profile, {display_name}!")
    with col2:
        if st.button("Logout", key="profile_logout"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.user_email = None
            st.rerun()
    
    st.divider()
    
    profile_data = get_user_profile()
    if profile_data:
        st.subheader("Profile Information")
        st.write(f"**Name:** {profile_data['name']}")
        st.write(f"**Email:** {profile_data['email']}")
        st.write(f"**Age:** {profile_data['age']}")
        st.write(f"**User ID:** {profile_data['id']}")
    else:
        st.error("Failed to load profile information")
    
    st.divider()
    
    todos = get_todos()
    st.subheader("Todo Statistics")
    
    if todos:
        total_todos = len(todos)
        completed_todos = sum(1 for todo in todos if todo["completed"])
        pending_todos = total_todos - completed_todos
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Todos", total_todos)
        with col2:
            st.metric("Completed", completed_todos)
        with col3:
            st.metric("Pending", pending_todos)
        
        if total_todos > 0:
            completion_rate = (completed_todos / total_todos) * 100
            st.progress(completion_rate / 100)
            st.write(f"Completion Rate: {completion_rate:.1f}%")
    else:
        st.info("No todos to analyze yet.")