import streamlit as st
from api_client import login_user, register_user

def login_register_screen():
    st.title("📝 Todo List App")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if email and password:
                    success, message = login_user(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter both email and password")
    
    with tab2:
        st.header("Register")
        with st.form("register_form"):
            reg_name = st.text_input("Name", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_age = st.number_input("Age", min_value=1, max_value=150, step=1, key="reg_age")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Register")

            if register_button:
                if reg_name and reg_email and reg_age and reg_password and reg_password_confirm:
                    if len(reg_password) < 5:
                        st.error("Password must be at least 5 characters long")
                    elif reg_password == reg_password_confirm:
                        success, message = register_user(reg_name, reg_email, reg_age, reg_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")