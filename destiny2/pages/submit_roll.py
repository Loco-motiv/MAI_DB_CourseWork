import streamlit as st
import pages.weapon_search
import repositories.godrolls
import pandas as pd

@st.cache_data
def get_weapon_perks(id) -> pd.DataFrame:
    weapon_barrel_perks = pd.DataFrame(repositories.weapons.get_weapon_barrel_perks(id))
    weapon_magazine_perks = pd.DataFrame(repositories.weapons.get_weapon_magazine_perks(id))
    weapon_first_column_perks = pd.DataFrame(repositories.weapons.get_weapon_first_column_perks(id))
    weapon_second_column_perks = pd.DataFrame(repositories.weapons.get_weapon_second_column_perks(id))

    if not weapon_first_column_perks.empty : weapon_first_column_perks = weapon_first_column_perks[(weapon_first_column_perks["first_column_name"] != "Golden Tricorn Enhanced") & (weapon_first_column_perks["first_column_name"] != "Perpetual Motion Enhanced")]
    if not weapon_second_column_perks.empty : weapon_second_column_perks = weapon_second_column_perks[(weapon_second_column_perks["second_column_name"] != "Golden Tricorn Enhanced") & (weapon_second_column_perks["second_column_name"] != "Perpetual Motion Enhanced")]

    return pd.concat([weapon_barrel_perks.dropna().drop_duplicates('barrel_name', ignore_index=True),
                      weapon_magazine_perks.dropna().drop_duplicates('magazine_name', ignore_index=True),
                      weapon_first_column_perks.dropna().drop_duplicates('first_column_name', ignore_index=True),
                      weapon_second_column_perks.dropna().drop_duplicates('second_column_name', ignore_index=True)], axis=1)

def submit_roll(id, user_id, author, description, barrel, magazine, first_column_perk, second_column_perk):
    repositories.godrolls.insert_godroll(id, user_id, author, description, barrel, magazine, first_column_perk, second_column_perk)

def show_submit_roll_page():
    st.title("Submit roll")
    top_filter = st.columns(vertical_alignment='bottom', spec=(3, 1))
    
    with top_filter[0]:
        name_filter = st.selectbox("Name", pages.weapon_search.df["name"].unique(), index=None, placeholder="Enter name")
    perks = pd.DataFrame(columns=("barrel_name", "magazine_name", "first_column_name", "second_column_name"))
    variant = None
    if name_filter is not None:
        with top_filter[1]:
            variant = st.selectbox("Variant", pages.weapon_search.df[pages.weapon_search.df['name'] == name_filter]["id"], index=None, placeholder="Select variant")
        if variant is not None:
            perks = get_weapon_perks(pages.weapon_search.df[pages.weapon_search.df['id'] == variant]["id"].item())

    perks_copy = perks.copy()

    if "barrel_name" not in perks:
        perks["barrel_name"] = None
    if "magazine_name" not in perks:
        perks["magazine_name"] = None
    if "first_column_name" not in perks:
        perks["first_column_name"] = None
    if "second_column_name" not in perks:
        perks["second_column_name"] = None
        

    bottom_perks = st.columns(vertical_alignment='bottom', spec=(1, 1, 1, 1))
    with bottom_perks[0]:
        barrel = st.selectbox("Barrel perk", perks["barrel_name"].dropna(), index=None, placeholder="Enter barrel perk")
    with bottom_perks[1]:
        magazine = st.selectbox("Magazine perk", perks["magazine_name"].dropna(), index=None, placeholder="Enter magazine perk")
    with bottom_perks[2]:
        first_column_perk = st.selectbox("First column perk", perks["first_column_name"].dropna(), index=None, placeholder="Enter first column perk")
    with bottom_perks[3]:
        second_column_perk = st.selectbox("Second column perk", perks["second_column_name"].dropna(), index=None, placeholder="Enter second column perk")

    if "barrel_name" not in perks_copy:
        barrel = -1
    if "magazine_name" not in perks_copy:
        magazine = -1
    if "first_column_name" not in perks_copy:
        first_column_perk = -1
    if "second_column_name" not in perks_copy:
        second_column_perk = -1

    author = st.text_input("Write author")
    description = st.text_input("Write description")

    god_roll_info = (variant, author, description, barrel, magazine, first_column_perk, second_column_perk)

    if all(item is not None for item in god_roll_info) and author != "" and description != "":
        god_roll_info = (variant,
                         st.session_state.user_id,
                         author,
                         description,
                         perks.loc[perks["barrel_name"] == barrel, 'barrel_id'].item() if barrel != -1 else None,
                         perks.loc[perks["magazine_name"] == magazine, 'magazine_id'].item() if magazine != -1 else None,
                         perks.loc[perks["first_column_name"] == first_column_perk, 'first_column_id'].item() if first_column_perk != -1 else None,
                         perks.loc[perks["second_column_name"] == second_column_perk, 'second_column_id'].item() if second_column_perk != -1 else None)
        if st.button("Submit", disabled=False, on_click=submit_roll, args=god_roll_info):
            st.success("Your submission is sent!")
    else:
        st.button("Submit", disabled=True)
