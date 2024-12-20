import pandas as pd

import streamlit as st
import repositories.weapons
import common
from math import ceil
import re

pd.options.mode.chained_assignment = None

@st.cache_data
def get_weapons() -> pd.DataFrame:
    weapons = repositories.weapons.get_weapons()

    return pd.DataFrame(weapons)

@st.cache_data
def get_first_column_perks() -> pd.DataFrame:
    weapons = repositories.weapons.get_first_column_perks()

    return pd.DataFrame(weapons)

@st.cache_data
def get_second_column_perks() -> pd.DataFrame:
    weapons = repositories.weapons.get_second_column_perks()

    return pd.DataFrame(weapons)

def filter_by_two_columns(first_column_perk_filter, second_column_perk_filter) -> pd.DataFrame:
    weapons = repositories.weapons.filter_by_two_columns(first_column_perk_filter, second_column_perk_filter)

    return pd.DataFrame(weapons)

def filter_by_first_column(first_column_perk_filter) -> pd.DataFrame:
    weapons = repositories.weapons.filter_by_first_column(first_column_perk_filter)

    return pd.DataFrame(weapons)

def filter_by_second_column(second_column_perk_filter) -> pd.DataFrame:
    weapons = repositories.weapons.filter_by_second_column(second_column_perk_filter)

    return pd.DataFrame(weapons)

@st.cache_data
def get_weapon_perks(id) -> pd.DataFrame:
    weapon_barrel_perks = pd.DataFrame(repositories.weapons.get_weapon_barrel_perks(id))
    weapon_magazine_perks = pd.DataFrame(repositories.weapons.get_weapon_magazine_perks(id))
    weapon_first_column_perks = pd.DataFrame(repositories.weapons.get_weapon_first_column_perks(id))
    weapon_second_column_perks = pd.DataFrame(repositories.weapons.get_weapon_second_column_perks(id))
    if not weapon_barrel_perks.empty : weapon_barrel_perks = weapon_barrel_perks.drop('barrel_id', axis=1)
    if not weapon_magazine_perks.empty : weapon_magazine_perks = weapon_magazine_perks.drop('magazine_id', axis=1)
    if not weapon_first_column_perks.empty : weapon_first_column_perks = weapon_first_column_perks[(weapon_first_column_perks["first_column_name"] != "Golden Tricorn Enhanced") & (weapon_first_column_perks["first_column_name"] != "Perpetual Motion Enhanced")].drop('first_column_id', axis=1)
    if not weapon_second_column_perks.empty : weapon_second_column_perks = weapon_second_column_perks[(weapon_second_column_perks["second_column_name"] != "Golden Tricorn Enhanced") & (weapon_second_column_perks["second_column_name"] != "Perpetual Motion Enhanced")].drop('second_column_id', axis=1)

    return pd.concat([weapon_barrel_perks.dropna().drop_duplicates('barrel_name', ignore_index=True),
                      weapon_magazine_perks.dropna().drop_duplicates('magazine_name', ignore_index=True),
                      weapon_first_column_perks.dropna().drop_duplicates('first_column_name', ignore_index=True),
                      weapon_second_column_perks.dropna().drop_duplicates('second_column_name', ignore_index=True)], axis=1)

df = get_weapons()
first_column_perks = get_first_column_perks()
second_column_perks = get_second_column_perks()

@st.cache_data
def get_page(dataframe, page_size, page_num):

    page_size = page_size

    if page_size is None:

        return None

    offset = page_size*(page_num-1)

    return dataframe[offset:offset + page_size]

@st.cache_data
def prepare_df(input_df):
    input_df["weapon_icon"] = input_df["weapon_icon"].apply(lambda x: "https://www.bungie.net/common/destiny2_content/icons/" + x + ".jpg")
    input_df["archetype_icon"] = input_df["archetype_icon"].apply(lambda x: "https://www.bungie.net/common/destiny2_content/icons/" + x + ".png")
    input_df["rarity_id"] = input_df["rarity_id"].apply(lambda x: common.Rarity(x).name)
    input_df["type_id"] = input_df["type_id"].apply(lambda x: re.sub(r"(\w)([A-Z])", r"\1 \2", (common.WeaponTypes(x).name)))
    input_df["element_id"] = input_df["element_id"].apply(lambda x: common.Elements(x).name)
    input_df["source"] = input_df["source"].apply(lambda x: "No source currently" if x == None else x)

    return input_df

def set_page_to_default():
    st.session_state.page = 1

def show_weapon_page():
    st.title("Weapon search")
    top_filter = st.columns(vertical_alignment='bottom', spec=(2, 1, 1, 1))
    with top_filter[0]:
        name_filter = st.selectbox("Name", df["name"].unique(), index=None, placeholder="Enter name", on_change=set_page_to_default)
    with top_filter[1]:
        element_filter = st.selectbox("Element", common.Elements._member_names_, index=None, placeholder="Enter element", on_change=set_page_to_default)
    with top_filter[2]:
        rarity_filter = st.selectbox("Rarity", common.Rarity._member_names_, index=None, placeholder="Enter rarity", on_change=set_page_to_default)
    with top_filter[3]:
        type_filter = st.selectbox("Type", [re.sub(r"(\w)([A-Z])", r"\1 \2", (item)) for item in common.WeaponTypes._member_names_], index=None, placeholder="Enter type", on_change=set_page_to_default)

    bottom_filter = st.columns(vertical_alignment='bottom', spec=(1, 1, 1, 2))
    with bottom_filter[0]:
        archetype_filter = st.selectbox("Archetype", df["archetype_name"].unique(), index=None, placeholder="Enter archetype", on_change=set_page_to_default)
    with bottom_filter[1]:
        first_column_perk_filter = st.selectbox("First column perk", first_column_perks["name"], index=None, placeholder="Enter perk", on_change=set_page_to_default)
    with bottom_filter[2]:
        second_column_perk_filter = st.selectbox("Second column perk", second_column_perks["name"], index=None, placeholder="Enter perk", on_change=set_page_to_default)
    with bottom_filter[3]:
        source_filter = st.selectbox("Source", df["source"].unique(), index=(None), placeholder="Enter source", on_change=set_page_to_default)

    if first_column_perk_filter != None:
        if second_column_perk_filter != None:
            filtered_df = filter_by_two_columns(first_column_perk_filter, second_column_perk_filter)
        else: filtered_df = filter_by_first_column(first_column_perk_filter)
    else: 
        if second_column_perk_filter != None:
            filtered_df = filter_by_second_column(second_column_perk_filter)
        else:
            filtered_df = df

    if not filtered_df.empty:
        if name_filter != None:
            filtered_df = filtered_df[filtered_df["name"] == name_filter]
        if element_filter != None:
            filtered_df = filtered_df[filtered_df["element_id"] == common.Elements[element_filter].value]
        if rarity_filter != None:
            filtered_df = filtered_df[filtered_df["rarity_id"] == common.Rarity[rarity_filter].value]
        if type_filter != None:
            filtered_df = filtered_df[filtered_df["type_id"] == common.WeaponTypes[type_filter.replace(" ", "")].value]
        if archetype_filter != None:
            filtered_df = filtered_df[filtered_df["archetype_name"] == archetype_filter]
        if source_filter != None:
            filtered_df = filtered_df[filtered_df["source"] == source_filter]

    controls = st.columns(vertical_alignment='bottom', spec=[2,2,1,1,10])

    if 'num_batches' not in st.session_state:
        st.session_state.num_batches = 0
    
    if 'page' not in st.session_state: 
        st.session_state.page = 1

    if 'page_size' not in st.session_state:
        st.session_state.page_size = 25
    
    with controls[0]:
        st.session_state.page_size = st.selectbox("Page size", (25, 50, 100), on_change=set_page_to_default, index=(25, 50, 100).index(st.session_state.page_size))
        st.session_state.num_batches = ceil(filtered_df.shape[0]/st.session_state.page_size)
        st.session_state.num_batches = 1 if st.session_state.num_batches == 0 else st.session_state.num_batches

    with controls[1]:
        st.session_state.page = st.selectbox("Page", range(1,st.session_state.num_batches+1), index=st.session_state.page - 1)
    
    def increment_page():
        if st.session_state.page < st.session_state.num_batches:
            st.session_state.page += 1

    def decrement_page():
        if st.session_state.page > 1:
            st.session_state.page -= 1

    with controls[2]:
        st.button("Prev", on_click=decrement_page, use_container_width=True)
    with controls[3]:
        st.button("Next", on_click=increment_page, use_container_width=True)
    with controls[4]:
        st.caption("Click on first column to get weapon's perks")

    if filtered_df.empty:
        st.warning("No gun with given filters")
        return

    df_page = get_page(filtered_df, st.session_state.page_size, st.session_state.page)
    df_page = prepare_df(df_page)

    if 'selected_id' not in st.session_state:
        st.session_state.selected_id = 0

    @st.dialog("Perks", width="large")
    def callback():
        if (st.session_state.df.selection.rows):
            st.session_state.selected_id = st.session_state.df.selection.rows[0]
        weapon_df = (get_weapon_perks(df_page.iloc[st.session_state.selected_id]['id']))

        weapon_df = weapon_df.fillna("")
        if "barrel_icon" in weapon_df : weapon_df["barrel_icon"] = weapon_df["barrel_icon"].apply(lambda x: "https://www.bungie.net/common/destiny2_content/icons/" + str(x) + ".png" if x != None else x)
        if "magazine_icon" in weapon_df : weapon_df["magazine_icon"] = weapon_df["magazine_icon"].apply(lambda x: "https://www.bungie.net/common/destiny2_content/icons/" + str(x) + ".png" if x != None else x)
        if "first_column_icon" in weapon_df : weapon_df["first_column_icon"] = weapon_df["first_column_icon"].apply(lambda x: "https://www.bungie.net/common/destiny2_content/icons/" + str(x) + ".png" if x != None else x)
        if "second_column_icon" in weapon_df : weapon_df["second_column_icon"] = weapon_df["second_column_icon"].apply(lambda x: "https://www.bungie.net/common/destiny2_content/icons/" + str(x) + ".png" if x != None else x)   
        st.dataframe(weapon_df, height = (weapon_df.shape[0] + 1) * 35,
                     use_container_width = True,
                     column_order=["barrel_icon", "barrel_name", "magazine_icon", "magazine_name", "first_column_icon", "first_column_name", "second_column_icon", "second_column_name"],
                     hide_index=True,
                     column_config={"barrel_icon": st.column_config.ImageColumn(label=""),
                                    "magazine_icon": st.column_config.ImageColumn(label=""),
                                    "first_column_icon": st.column_config.ImageColumn(label=""),
                                    "second_column_icon": st.column_config.ImageColumn(label=""),
                                    "barrel_name" : st.column_config.Column(width=200, label="Barrel"),
                                    "magazine_name" : st.column_config.Column(width=200, label="Magazine"),
                                    "first_column_name" : st.column_config.Column(width=200, label="First column"),
                                    "second_column_name" : st.column_config.Column(width=200, label="Second column"),})

    st.dataframe(df_page, height = (st.session_state.page_size + 1) * 35,
                 use_container_width = True,
                 column_order = ("weapon_icon", "name", "rarity_id", "type_id", "element_id", "archetype_icon", "archetype_name", "source"),
                 column_config={"weapon_icon": st.column_config.ImageColumn(label=""),
                                "name" : st.column_config.Column(width=215, label="Name"),
                                "rarity_id" : st.column_config.Column(width=90, label="Rarity"),
                                "type_id" : st.column_config.Column(width=120, label="Type"),
                                "element_id" : st.column_config.Column(width=70, label="Element"),
                                "source" : st.column_config.Column(width=400, label="Source"),
                                "archetype_name" : st.column_config.Column(width=170, label="Archetype"),
                                "archetype_icon" : st.column_config.ImageColumn(label="")},
                 on_select=callback,
                 selection_mode="single-row",
                 key="df")