import streamlit as st
from Src.visualization.graphs import pie_chart_politician_page_five, pie_chart_user_page_five

def best_alignment_sector(data_general, data_user):
    # Merge data frames on 'sector'
    help_df = data_general.merge(data_user, how="left", on="sector")

    # Calculate the squared difference as a "score" (penalizing larger differences)
    help_df["score"] = (help_df["Total Invested Sector"] - help_df["Invested by User"])**2

    # Calculate alignment score based on the normalized difference, clip to avoid negatives
    help_df["alignment"] = (
        1 - abs(help_df["Total Invested Sector"] - help_df["Invested by User"]) /
        help_df["Total Invested Sector"].replace(0, 1)  # Replace zeros with 1 to avoid division by zero
    ).clip(lower=0)  # Clip the alignment score to avoid negative values

    # Group by Politician and calculate the average score and alignment
    grouped_df_sector = help_df.groupby("Politician", as_index=False)["score"].mean()
    grouped_df_alignement = help_df.groupby("Politician", as_index=False)["alignment"].mean()
    grouped_df_alignement["alignment"] = grouped_df_alignement["alignment"]*100


    # Merge the grouped data frames
    top_5_politicans = (
        grouped_df_sector
        .merge(grouped_df_alignement, how="left", on="Politician")
        .sort_values(by=["alignment", "score"], ascending=[False, True])
        .rename(columns = {"score" : "MSE score", "alignment" : "Alignment (%)"})
        .reset_index(drop = True)
        .head(5)
    )

    top_5_politicans.index = top_5_politicans.index + 1 

    return top_5_politicans


def best_alignment_instrument(data_general, data_user):
    # Merge data frames on 'type'
    help_df = data_general.merge(data_user, how="left", on="quoteType")

    # Calculate the squared difference as a "score" (penalizing larger differences)
    help_df["score"] = (help_df["Total Invested Type"] - help_df["Invested by User"])**2

    # Calculate alignment score based on the normalized difference, clip to avoid negatives
    help_df["alignment"] = (
        1 - abs(help_df["Total Invested Type"] - help_df["Invested by User"]) /
        help_df["Total Invested Type"].replace(0, 1)  # Replace zeros with 1 to avoid division by zero
    ).clip(lower=0)  # Clip the alignment score to avoid negative values

    # Group by Politician and calculate the average score and alignment
    grouped_df_type = help_df.groupby("Politician", as_index=False)["score"].mean()
    grouped_df_alignement = help_df.groupby("Politician", as_index=False)["alignment"].mean()
    grouped_df_alignement["alignment"] = grouped_df_alignement["alignment"]*100


    # Merge the grouped data frames
    top_5_politicans = (
        grouped_df_type
        .merge(grouped_df_alignement, how="left", on="Politician")
        .sort_values(by=["alignment", "score"], ascending=[False, True])
        .rename(columns = {"score" : "MSE score", "alignment" : "Alignment (%)"})
        .reset_index(drop = True)
        .head(5)
    )

    top_5_politicans.index = top_5_politicans.index + 1 

    return top_5_politicans


def equity_alignment_politician_sector(list_of_politicians, list_of_unique_sectors, data_general, data_user):
    tabs = st.tabs(list_of_politicians)


    for i, tab in enumerate(tabs):
        with tab:
            st.header(f"Comparison with {list_of_politicians[i]}")

            col_politician, col_user = st.columns(2)
            
            with col_politician:
                chart_pie = pie_chart_politician_page_five(data_general, "Purchase", "sector", list_of_politicians[i], list_of_unique_sectors)

                st.plotly_chart(chart_pie, use_container_width=True, key = f"Politician_{list_of_politicians[i]}_graph")


            with col_user:
                chart_pie_2 = pie_chart_user_page_five(data_user, list_of_unique_sectors, "sector")

                st.plotly_chart(chart_pie_2, use_container_width=True, key = f"User_graph_{list_of_politicians[i]}")


def equity_alignment_politician_instrument(list_of_politicians, list_of_unique_instruments, data_general, data_user):
    tabs = st.tabs(list_of_politicians)


    for i, tab in enumerate(tabs):
        with tab:
            st.header(f"Comparison with {list_of_politicians[i]}")

            col_politician, col_user = st.columns(2)
            
            with col_politician:
                chart_pie = pie_chart_politician_page_five(data_general, "Purchase", "quoteType", list_of_politicians[i], list_of_unique_instruments)

                st.plotly_chart(chart_pie, use_container_width=True, key = f"Politician_{list_of_politicians[i]}_graph")


            with col_user:
                chart_pie_2 = pie_chart_user_page_five(data_user, list_of_unique_instruments, "quoteType")

                st.plotly_chart(chart_pie_2, use_container_width=True, key = f"User_graph_{list_of_politicians[i]}")
