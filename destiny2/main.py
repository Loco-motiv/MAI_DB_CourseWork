import streamlit as st
import common

st.set_page_config(layout="wide")

import pages.weapon_search
import pages.armor_search
import pages.godroll_prepositions
import pages.godrolls
import pages.admin
import pages.submit_roll
import pages.auth

def main():
    if 'entered' not in st.session_state:
        st.session_state.entered = False
    if 'role' not in st.session_state:
        st.session_state.role = common.Roles.User.value
    if 'user_id' not in st.session_state:
        st.session_state.user_id = -1

    available_pages = ["Weapons", "Armor", "Godrolls"]

    if st.session_state.entered:
        available_pages.append("Submit roll")
    if st.session_state.role > common.Roles.User.value:
        available_pages.append("Review prepositions")
    if st.session_state.role > common.Roles.Moderator.value:
        available_pages.append("Admin page")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        available_pages,
    )
    if page == "Weapons":
        pages.weapon_search.show_weapon_page()
    elif page == "Armor":
        pages.armor_search.show_armor_page()
    elif page == "Godrolls":
        pages.godrolls.show_godrolls_page()
    elif page == "Submit roll":
        pages.submit_roll.show_submit_roll_page()
    elif page == "Review prepositions":
        pages.godroll_prepositions.show_godroll_prepositions_page()
    elif page == "Admin page":
        pages.admin.show_grant_admin_page()
    if not st.session_state.entered:
        if st.sidebar.button("Sign in"):
            pages.auth.show_auth_page()
        st.sidebar.caption("Sign in to propose god rolls")
    elif st.sidebar.button("Exit"):
        st.session_state.entered = False
        st.session_state.role = common.Roles.User.value
        st.session_state.user_id = -1
        st.rerun()
        

if __name__ == "__main__":
    main()