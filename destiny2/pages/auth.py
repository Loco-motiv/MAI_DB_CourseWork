import bcrypt
import streamlit as st
import repositories.auth

@st.dialog("Please login to continue", width="large")
def callback():
    if "sign_in" not in st.session_state:
        st.session_state.sign_in = True
    if "sign_up" not in st.session_state:
        st.session_state.sign_up = False
    left, right = st.columns(2)
    if left.button("Sign in", use_container_width=True, key='left'):
        st.session_state.sign_in = True
        st.session_state.sign_up = False
    if right.button("Sign up", use_container_width=True, key='right'):
        st.session_state.sign_up = True
        st.session_state.sign_in = False
    if st.session_state.sign_in:
        st.subheader("Sign in")
        login = st.text_input("login", key='login_sign_in')
        password = st.text_input("password", key='password_sign_in')
        if (st.button("Sign in", key='final')):
            if login == "":
                st.error("Please enter login")
            elif password == "":
                st.error("Please enter password")
            else:
                user_id, hashed_password, role = repositories.auth.user_data(login)
                if user_id == -1:
                    st.error("No such login/password")
                else:
                    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode('utf-8')):
                        st.session_state.entered = True
                        st.session_state.role = role
                        st.session_state.user_id = user_id
                        st.rerun()
                    else:
                        st.error("No such login/password")

    if st.session_state.sign_up:
        st.subheader("Sign up")
        login = st.text_input("login", key='login_sign_up')
        password = st.text_input("password", key='password_sign_up')
        if (st.button("Sign up", key='final')):
            if login == "":
                st.error("Please enter login")
            elif password == "":
                st.error("Please enter password")
            else:
                user_id, hashed_password, role = repositories.auth.user_data(login)
                if user_id == -1:
                    repositories.auth.register_user(login, bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8'))
                    st.success("Successfully registered. Please sign in")
                else:
                    st.error("Login is already taken")

def show_auth_page():
    callback()