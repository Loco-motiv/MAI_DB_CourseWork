import streamlit as st
import repositories.admin
import pandas as pd
import os
from datetime import datetime

def get_users():
    return pd.DataFrame(repositories.admin.get_users())

def raise_user(user):
    repositories.admin.raise_user(user)

def denote_user(user):
    repositories.admin.denote_user(user)

def show_grant_admin_page():
    st.title("Admin page")

    users = get_users()

    denote_flag, raise_flag = False, False

    raise_columns = st.columns(spec=(3,1,6), vertical_alignment='bottom')
    with raise_columns[0]:
        user = st.selectbox("Select user", options=users["login"], index=None)
    with raise_columns[1]:
        raise_flag = st.button("Raise user", on_click=raise_user, args=[user], disabled=(user==None))     
    if raise_flag:
        st.success("Raised successfully")
    with raise_columns[2]:
        denote_flag = st.button("Denote user", on_click=denote_user, args=[user], disabled=(user==None))
    if denote_flag:
        st.success("Denoted successfully")
    
    if st.button("Make backup"):
        os.system("docker exec habr-pg-13.3 pg_dump -n public -Fc -d postgres -p 5432 -h localhost -U habrpguser > destiny2/dump/" + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".dump")
        st.success("Backup made successfully")
    
    rebuild_columns = st.columns(spec=(3,1,6), vertical_alignment='bottom')
    built_flag = False

    dir_path = (os.path.realpath("destiny2/dump/"))

    dump_files = os.listdir(dir_path)

    with rebuild_columns[0]:
        dump = st.selectbox("Select dump", options=sorted(dump_files, reverse=True), index=None)
    with rebuild_columns[1]:
        built_flag = st.button("Rebuild", disabled=(dump==None))
    if built_flag:
        os.system("docker exec -i habr-pg-13.3 pg_restore -Fc -d postgres -c -n public -p 5432 -h localhost -U habrpguser < destiny2/dump/" + str(dump))
        st.success("Rebuilt successfully")