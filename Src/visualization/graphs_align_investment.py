"""
This script contains the function that creates a line graph showing the
cumulative investment over time for a specific politician or party.
"""
import plotly.graph_objects as go
import pandas as pd


class Pie_Chart_Align_Investment:
    def __init__(self, list_of_sectors_instruments: list):
        self.colors = self.same_color_across_pie_charts(
            list_of_sectors_instruments)

    @staticmethod
    def same_color_across_pie_charts(list_of_sectors_instruments: list) -> dict:
        unique_colors = ["#%06x" % (i * 12345 % 0xFFFFFF)
                         for i in range(len(list_of_sectors_instruments))]
        return dict(zip(list_of_sectors_instruments, unique_colors))

    def create_politician_chart(self, data: pd.DataFrame, purchase: str,
                                subset: str, politician: str) -> go.Figure:
        """
        Create a pie chart showing the investment distribution of a specific
        politician.

        Parameters:
        - data (pd.DataFrame): The input DataFrame containing transaction data.
        - purchase (str): The purchase type ('Purchase' or 'Sale').
        - subset (str): The parameter to group the data by (e.g., 'Sector',
        'Instrument').
        - politician (str): The politician whose investment data is to be
        visualized.

        Returns:
        - go.Figure: A Plotly figure object containing the pie chart.
        """
        selected_dataset = data[data["Transaction"] == purchase].groupby(
            ["Politician", subset])["Invested"].sum().reset_index()
        help_df = selected_dataset[selected_dataset["Politician"] == politician]
        labels = help_df.iloc[:, 1]
        values = help_df["Invested"] if purchase == "Purchase" else -help_df["Invested"]
        default_color = "#d3d3d3"
        pie_colors = [self.colors[label] if label in self.colors else default_color
                      for label in labels]
        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker=dict(colors=pie_colors),
            )]
        )
        fig.update_layout(
            title=f"{politician}'s exposure to the EQUITY:",
            template="plotly_white"
        )

        return fig

    def create_user_chart(self, data: pd.DataFrame, what: str) -> go.Figure:
        """
        Create a pie chart showing the investment distribution of a user.

        Parameters:
        - data (pd.DataFrame): The input DataFrame containing user investment
        data.
        - what (str): The column name in the DataFrame to use as the labels for
        the pie chart (e.g., 'Sector').

        Returns:
        - go.Figure: A Plotly figure object containing the pie chart.
        """
        labels = data[what]
        values = data["Invested by User"]
        default_color = "#d3d3d3"
        pie_colors = [self.colors[label] if label in self.colors else default_color
                      for label in labels]
        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker=dict(colors=pie_colors),
            )]
        )

        # Update layout
        fig.update_layout(
            title="Your exposure to the EQUITY:",
            template="plotly_white"
        )

        return fig
