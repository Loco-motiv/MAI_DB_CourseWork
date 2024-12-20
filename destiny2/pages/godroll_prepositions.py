import streamlit as st
import pandas as pd
import repositories.godrolls

def approve_godroll(id):
    repositories.godrolls.approve_godroll(id)

def get_godroll_prepositions():
    godroll_prepositions = repositories.godrolls.get_godroll_prepositions()

    return pd.DataFrame(godroll_prepositions)

def show_godroll_prepositions_page():
    st.title("Godroll prepositions")

    godroll_prepositions_df = get_godroll_prepositions()

    if godroll_prepositions_df.empty:
        st.warning("Nothing to show((")
        return

    name_filter = st.selectbox("Name", godroll_prepositions_df["weapon_name"].unique(), index=None, placeholder="Enter name")
    
    filtered_df = godroll_prepositions_df
    if name_filter != None:
        filtered_df = filtered_df[filtered_df["weapon_name"] == name_filter]
    
    for index, row in filtered_df.iterrows():
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
            if (row["user_id"] == st.session_state.user_id and st.session_state.role == 1):
                st.warning("You cannot approve your own submission")
            else:
                if st.button("Accept godroll", key=index, on_click=approve_godroll, args=[row["id"]]):
                    st.rerun()