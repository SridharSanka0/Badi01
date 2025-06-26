import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.title("🏸 Badminton Score Tracker & Ranking App")

# Upload Excel template
uploaded_file = st.file_uploader("Upload Excel Template", type=["xlsx"])
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    template_df = xls.parse("template")
    
    # Detect group start and extract player data
    player_start_row = template_df[template_df.iloc[:, 0] == 'Player Name'].index[0] + 1
    player_df = template_df.iloc[player_start_row:, 0:7]
    player_df.columns = ['Player', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6']
    player_df = player_df.dropna(subset=['Player'])

    st.subheader("Enter Scores")
    edited_df = st.data_editor(player_df, num_rows="dynamic", key="scores_editor")

    if st.button("Calculate Rankings"):
        scores_cols = ['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6']
        edited_df['Total'] = edited_df[scores_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1)
        edited_df['Wins'] = edited_df[scores_cols].apply(lambda row: sum([1 if s == 21 else 0 for s in row if pd.notna(s)]), axis=1)

        # Ranking within group
        edited_df['Rank'] = edited_df.sort_values(
            by=['Total', 'Wins', 'Player'],
            ascending=[False, False, True]
        ).reset_index().index + 1

        st.subheader("Group Ranking Results")
        st.dataframe(edited_df[['Player', 'Total', 'Wins', 'Rank']])

        # Final overall ranking logic can be implemented here if multiple groups are combined

        st.success("Ranking calculation complete!")

