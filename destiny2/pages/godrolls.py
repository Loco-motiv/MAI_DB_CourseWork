import streamlit as st
import pandas as pd
from math import ceil
import repositories.godrolls

def get_godrolls():
    godrolls = repositories.godrolls.get_godrolls()

    return pd.DataFrame(godrolls)

@st.cache_data
def get_page(dataframe, page_size, page_num):

    page_size = page_size

    if page_size is None:

        return None

    offset = page_size*(page_num-1)

    return dataframe[offset:offset + page_size]

def set_page_to_default():
    st.session_state.page_gr = 1

def show_godrolls_page():
    st.title("Godrolls")

    godrolls_df = get_godrolls()

    if godrolls_df.empty:
        st.warning("Nothing to show((")
        return

    name_filter = st.selectbox("Name", godrolls_df["weapon_name"].unique(), index=None, placeholder="Enter name", on_change=set_page_to_default)
    
    controls = st.columns(vertical_alignment='bottom', spec=[2,2,1,1,10])

    if 'num_batches_gr' not in st.session_state:
        st.session_state.num_batches_gr = 0
    
    if 'page_gr' not in st.session_state: 
        st.session_state.page_gr = 1

    if 'page_size_gr' not in st.session_state:
        st.session_state.page_size_gr = 25
    
    filtered_df = godrolls_df
    if name_filter != None:
        filtered_df = filtered_df[filtered_df["weapon_name"] == name_filter]

    with controls[0]:
        st.session_state.page_size_gr = st.selectbox("Page size", (25, 50, 100), on_change=set_page_to_default, index=(25, 50, 100).index(st.session_state.page_size_gr))
        st.session_state.num_batches_gr = ceil(filtered_df.shape[0]/st.session_state.page_size_gr)
        st.session_state.num_batches_gr = 1 if st.session_state.num_batches_gr == 0 else st.session_state.num_batches_gr

    with controls[1]:
        st.session_state.page_gr = st.selectbox("Page", range(1,st.session_state.num_batches_gr+1), index=st.session_state.page_gr - 1)
    
    def increment_page():
        if st.session_state.page_gr < st.session_state.num_batches_gr:
            st.session_state.page_gr += 1

    def decrement_page():
        if st.session_state.page_gr > 1:
            st.session_state.page_gr -= 1

    with controls[2]:
        st.button("Prev", on_click=decrement_page, use_container_width=True)
    with controls[3]:
        st.button("Next", on_click=increment_page, use_container_width=True)

    df_page = get_page(filtered_df, st.session_state.page_size_gr, st.session_state.page_gr)
    
    for index, row in df_page.iterrows():
        with st.expander(label=(row['weapon_name'] + " by " + row['author'])):
            st.write(row["description"])
            perks = st.columns(spec=[1,1,1,1,1,10])

            with perks[0]:
                st.image("https://www.bungie.net/common/destiny2_content/icons/" + row["weapon_icon"] + ".jpg")
            with perks[1]:
                st.image("https://www.bungie.net/common/destiny2_content/icons/" + row["barrel_icon"] + ".png", caption=row["barrel_name"])
            with perks[2]:
                st.image("https://www.bungie.net/common/destiny2_content/icons/" + row["magazine_icon"] + ".png", caption=row["magazine_name"])
            with perks[3]:
                st.image("https://www.bungie.net/common/destiny2_content/icons/" + row["first_column_icon"] + ".png", caption=row["first_column_name"])
            with perks[4]:
                st.image("https://www.bungie.net/common/destiny2_content/icons/" + row["second_column_icon"] + ".png", caption=row["second_column_name"])