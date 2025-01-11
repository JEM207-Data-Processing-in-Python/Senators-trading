"""
This file contains the helper code for the Streamlit app's Align Your Investment Strategy page.
"""
import streamlit as st
from Src.visualization.graphs import pie_chart_politician_page_five, pie_chart_user_page_five
from Src.visualization.tables import data_for_strategy_align_sector


def best_alignment_sector(data_general, data_user):
    # Merge data frames on 'sector'
    help_df = data_general.merge(data_user, how="left", on="sector")

    # Calculate the squared difference as a "score" (penalizing larger differences)
    help_df["score"] = (help_df["Total Invested Sector"] - help_df["Invested by User"]) ** 2

    # Calculate alignment score based on the normalized difference, clip to avoid negatives
    help_df["alignment"] = (1 - abs(help_df["Total Invested Sector"] - help_df["Invested by User"]) / help_df["Total Invested Sector"].replace(0, 1)).clip(lower=0)

    # Group by Politician and calculate the average score and alignment
    grouped_df_sector = help_df.groupby("Politician", as_index=False)["score"].mean()
    grouped_df_alignment = help_df.groupby("Politician", as_index=False)["alignment"].mean()
    grouped_df_alignment["alignment"] = grouped_df_alignment["alignment"] * 100

    # Merge the grouped data frames
    top_5_politicians = (
        grouped_df_sector
        .merge(grouped_df_alignment, how="left", on="Politician")
        .sort_values(by=["alignment", "score"], ascending=[False, True])
        .rename(columns={"score": "MSE score", "alignment": "Alignment (%)"})
        .reset_index(drop=True)
        .head(5)
    )

    top_5_politicians.index = top_5_politicians.index + 1

    return top_5_politicians


def best_alignment_instrument(data_general, data_user):
    # Merge data frames on 'type'
    help_df = data_general.merge(data_user, how="left", on="quoteType")

    # Calculate the squared difference as a "score" (penalizing larger differences)
    help_df["score"] = (help_df["Total Invested Type"] - help_df["Invested by User"]) ** 2

    # Calculate alignment score based on the normalized difference, clip to avoid negatives
    help_df["alignment"] = (1 - abs(help_df["Total Invested Type"] - help_df["Invested by User"]) / help_df["Total Invested Type"].replace(0, 1)).clip(lower=0)

    # Group by Politician and calculate the average score and alignment
    grouped_df_type = help_df.groupby("Politician", as_index=False)["score"].mean()
    grouped_df_alignment = help_df.groupby("Politician", as_index=False)["alignment"].mean()
    grouped_df_alignment["alignment"] = grouped_df_alignment["alignment"] * 100

    # Merge the grouped data frames
    top_5_politicians = (
        grouped_df_type
        .merge(grouped_df_alignment, how="left", on="Politician")
        .sort_values(by=["alignment", "score"], ascending=[False, True])
        .rename(columns={"score": "MSE score", "alignment": "Alignment (%)"})
        .reset_index(drop=True)
        .head(5)
    )

    top_5_politicians.index = top_5_politicians.index + 1

    return top_5_politicians


def equity_alignment_politician_sector(list_of_politicians, list_of_unique_sectors, data_general, data_user):
    # Merge data frames on 'sector'
    strategy_data = data_for_strategy_align_sector(data_general)

    help_df = strategy_data.merge(data_user, how="left", on="sector")

    # Calculate alignment score based on the normalized difference, clip to avoid negatives
    help_df["alignment"] = (1 - abs(help_df["Total Invested Sector"] - help_df["Invested by User"]) / help_df["Total Invested Sector"].replace(0, 1)).clip(lower=0)  # Clip the alignment score to avoid negative values

    tabs = st.tabs(list_of_politicians)
    for i, tab in enumerate(tabs):
        with tab:
            st.header(f"Comparison with {list_of_politicians[i]}")

            # Filter data for the current politician
            info_table = help_df[help_df["Politician"] == list_of_politicians[i]].sort_values(by="alignment", ascending=False)
            if not info_table.empty:
                st.write(
                    f"Your strategy is the most compatible with the strategy of {list_of_politicians[i]}. "
                    f"The biggest compliance is in the {info_table['sector'].iloc[0]} sector "
                    f"({info_table['alignment'].iloc[0] * 100:.2f}%). "
                    f"The lowest compliance is in the {info_table['sector'].iloc[-1]} sector "
                    f"({info_table['alignment'].iloc[-1] * 100:.2f}%)."
                )
            else:
                st.write(f"No data available for {list_of_politicians[i]}.")

            col_politician, col_user = st.columns(2)

            with col_politician:
                chart_pie = pie_chart_politician_page_five(
                    data_general, "Purchase", "sector", list_of_politicians[i], list_of_unique_sectors
                )

                st.plotly_chart(chart_pie, use_container_width=True, key=f"Politician_{list_of_politicians[i]}_graph")

            with col_user:
                chart_pie_2 = pie_chart_user_page_five(data_user, list_of_unique_sectors, "sector")

                st.plotly_chart(chart_pie_2, use_container_width=True, key=f"User_graph_{list_of_politicians[i]}")


def equity_alignment_politician_instrument(list_of_politicians, list_of_unique_instruments, data_general, data_user):
    tabs = st.tabs(list_of_politicians)

    for i, tab in enumerate(tabs):
        with tab:
            st.header(f"Comparison with {list_of_politicians[i]}")

            col_politician, col_user = st.columns(2)

            with col_politician:
                chart_pie = pie_chart_politician_page_five(
                    data_general, "Purchase", "quoteType",
                    list_of_politicians[i], list_of_unique_instruments
                )
                st.plotly_chart(chart_pie, use_container_width=True, key=f"Politician_{list_of_politicians[i]}_graph")

            with col_user:
                chart_pie_2 = pie_chart_user_page_five(
                    data_user, list_of_unique_instruments, "quoteType"
                )
                st.plotly_chart(chart_pie_2, use_container_width=True, key=f"User_graph_{list_of_politicians[i]}")
