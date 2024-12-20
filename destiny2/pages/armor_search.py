import pandas as pd

import streamlit as st
import repositories.armor
import common
from math import ceil
import re

pd.options.mode.chained_assignment = None

@st.cache_data
def get_armor() -> pd.DataFrame:
    weapons = repositories.armor.get_armor()

    return pd.DataFrame(weapons)

df = get_armor()

@st.cache_data
def get_page(dataframe, page_size, page_num):

    page_size = page_size

    if page_size is None:

        return None

    offset = page_size*(page_num-1)

    return dataframe[offset:offset + page_size]

@st.cache_data
def prepare_df(input_df):
    input_df["armor_icon"] = input_df["armor_icon"].apply(lambda x: "https://www.bungie.net/common/destiny2_content/icons/" + x + ".jpg")
    input_df["rarity_id"] = input_df["rarity_id"].apply(lambda x: common.Rarity(x).name)
    input_df["type_id"] = input_df["type_id"].apply(lambda x: re.sub(r"(\w)([A-Z])", r"\1 \2", (common.ArmorTypes(x).name)))
    input_df["class_id"] = input_df["class_id"].apply(lambda x: common.Classes(x).name)
    input_df["source"] = input_df["source"].apply(lambda x: "No source currently" if x == None else x)

    return input_df

def set_page_to_default():
    st.session_state.a_page = 1

def show_armor_page():
    st.title("Armor search")
    top_filter = st.columns(vertical_alignment='bottom', spec=(2, 1, 1, 1))
    with top_filter[0]:
        name_filter = st.selectbox("Name", df["name"].unique(), index=None, placeholder="Enter name", on_change=set_page_to_default, key="a_name_filter")
    with top_filter[1]:
        class_filter = st.selectbox("Class", common.Classes._member_names_, index=None, placeholder="Enter class", on_change=set_page_to_default, key="a_class_filter")
    with top_filter[2]:
        rarity_filter = st.selectbox("Rarity", common.Rarity._member_names_, index=None, placeholder="Enter rarity", on_change=set_page_to_default, key="a_rarity_filter")
    with top_filter[3]:
        type_filter = st.selectbox("Type", [re.sub(r"(\w)([A-Z])", r"\1 \2", (item)) for item in common.ArmorTypes._member_names_], index=None, placeholder="Enter type", on_change=set_page_to_default, key="a_type_filter")

    bottom_filter = st.columns(vertical_alignment='bottom', spec=(1, 1, 1, 2))
    with bottom_filter[3]:
        source_filter = st.selectbox("Source", df["source"].unique(), index=None, placeholder="Enter source", on_change=set_page_to_default, key="a_source_filter")

    filtered_df = df

    if name_filter != None:
        filtered_df = filtered_df[filtered_df["name"] == name_filter]
    if class_filter != None:
        filtered_df = filtered_df[filtered_df["class_id"] == common.Classes[class_filter].value]
    if rarity_filter != None:
        filtered_df = filtered_df[filtered_df["rarity_id"] == common.Rarity[rarity_filter].value]
    if type_filter != None:
        filtered_df = filtered_df[filtered_df["type_id"] == common.ArmorTypes[type_filter.replace(" ", "")].value]
    if source_filter != None:
        filtered_df = filtered_df[filtered_df["source"] == source_filter]

    controls = st.columns(vertical_alignment='bottom', spec=[2,2,1,1,10])

    if 'a_num_batches' not in st.session_state:
        st.session_state.a_num_batches = 0
    
    if 'a_page' not in st.session_state: 
        st.session_state.a_page = 1

    if 'a_page_size' not in st.session_state:
        st.session_state.a_page_size = 25
    
    with controls[0]:
        st.session_state.a_page_size = st.selectbox("Page size", (25, 50, 100), on_change=set_page_to_default, index=(25, 50, 100).index(st.session_state.a_page_size))
        st.session_state.a_num_batches = ceil(filtered_df.shape[0]/st.session_state.a_page_size)
        st.session_state.a_num_batches = 1 if st.session_state.a_num_batches == 0 else st.session_state.a_num_batches

    with controls[1]:
        st.session_state.a_page = st.selectbox("Page", range(1,st.session_state.a_num_batches+1), index=st.session_state.a_page - 1)
    
    def increment_page():
        if st.session_state.a_page < st.session_state.a_num_batches:
            st.session_state.a_page += 1

    def decrement_page():
        if st.session_state.a_page > 1:
            st.session_state.a_page -= 1

    with controls[2]:
        st.button("Prev", on_click=decrement_page, use_container_width=True)
    with controls[3]:
        st.button("Next", on_click=increment_page, use_container_width=True)

    if filtered_df.empty:
        st.warning("No gun with given filters")
        return

    df_page = get_page(filtered_df, st.session_state.a_page_size, st.session_state.a_page)
    df_page = prepare_df(df_page)

    st.dataframe(df_page, height = (st.session_state.a_page_size + 1) * 35,
                 use_container_width = True,
                 column_order = ("armor_icon", "name", "class_id", "rarity_id", "type_id", "source"),
                 column_config={"armor_icon": st.column_config.ImageColumn(label=""),
                                "name" : st.column_config.Column(width=215, label="Name"),
                                "rarity_id" : st.column_config.Column(width=90, label="Rarity"),
                                "type_id" : st.column_config.Column(width=120, label="Type"),
                                "class_id" : st.column_config.Column(width=70, label="Class"),
                                "source" : st.column_config.Column(width=400, label="Source")},
                 key="df")