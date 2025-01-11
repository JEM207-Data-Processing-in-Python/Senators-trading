"""
This script contains the function that creates a line graph showing the cumulative investment over time for a specific politician or party.
"""
import pandas as pd
import plotly.graph_objects as go

from Src.visualization.graphs_utils import get_the_color
from Src.streamlit.politician_finder_3 import five_days


class Politician_Data_Visualizer:
    def __init__(self, data: pd.DataFrame):
        """
        Initializes the PoliticianDataVisualizer with the provided dataset.

        :param data: pd.DataFrame - The trading data to be processed.
        """
        self.data = data

    def grouping_for_graph(self, grouping_parametrs: str, politician: str) -> go.Figure:
        """
        Create a line graph showing the cumulative investment over time for a specific politician or party.

        :param grouping_parametrs: str - The parameter to group by (e.g., "Politician" or "Party").
        :param politician: str - The name of the politician for whom the graph should be created.

        :return: go.Figure - A Plotly figure containing the line graph.
        """
        data_trading_in_time = self.data[[grouping_parametrs, "Traded", "Invested"]]
        data_trading_in_time = data_trading_in_time.groupby([grouping_parametrs, "Traded"]).sum()
        data_trading_in_time.reset_index(inplace=True)

        data_trading_in_time["cumulative_invested"] = (
            data_trading_in_time.sort_values(by=[grouping_parametrs, "Traded"])
            .groupby(grouping_parametrs)
            .apply(lambda group: group["Invested"].cumsum())
            .reset_index(drop=True)
        )

        help_df = data_trading_in_time[data_trading_in_time[grouping_parametrs] == politician]
        help_df = help_df.set_index("Traded")

        color_of_graph = get_the_color(politician, self.data)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=help_df.index,
            y=help_df['cumulative_invested'],
            mode='lines',
            name=politician,
            line=dict(color=color_of_graph, shape='hv')
        ))

        fig.update_layout(
            title=f"Cumulative Investment over Time of {politician}",
            xaxis_title="Time (Traded)",
            yaxis_title="Cumulative Invested",
            xaxis=dict(tickmode='array', tickvals=[help_df.index[0], help_df.index[-1]]),
            template="plotly_white"
        )

        return fig

    def grouping_for_barchart(self, grouping_parametrs: str, politician: str) -> go.Figure:
        """
        Create a bar chart showing the total investment over months for a specific politician or party.

        :param grouping_parametrs: str - The parameter to group by (e.g., "Politician" or "Party").
        :param politician: str - The name of the politician for whom the bar chart should be created.

        :return: go.Figure - A Plotly figure containing the bar chart.
        """
        data_trading_in_time = self.data[[grouping_parametrs, "Traded", "Invested", "Transaction"]].copy()
        data_trading_in_time["Traded"] = pd.to_datetime(data_trading_in_time["Traded"])
        data_trading_in_time["Month"] = data_trading_in_time["Traded"].dt.strftime('%Y-%m')

        monthly_investment = data_trading_in_time.groupby([grouping_parametrs, "Month"])["Invested"].sum().reset_index()
        help_df = monthly_investment[monthly_investment[grouping_parametrs] == politician].copy()

        colors = help_df["Invested"].apply(lambda x: "green" if x > 0 else "red")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=help_df["Month"],
            y=help_df["Invested"],
            name=politician,
            marker=dict(color=colors)
        ))

        fig.update_layout(
            title=f"Total Investment per Month of {politician}",
            xaxis_title="Month",
            yaxis_title="Total Invested",
            template="plotly_white",
            barmode='relative',
            xaxis=dict(
                tickmode="array",
                tickvals=help_df["Month"],
                tickformat="%b %Y",
            ),
        )

        return fig

    def pie_chart_advanced(self, purchase: str, subset: str, politician: str) -> go.Figure:
        """
        Create an advanced pie chart showing the total investment of a specific politician by a subset (e.g., sectors/instruments)
        for a specific purchase type (e.g., 'Purchase' or 'Sale').

        :param purchase: str - The purchase type ('Purchase' or 'Sale').
        :param subset: str - The parameter to group the data by (e.g., 'Sector', 'Instrument').
        :param politician: str - The politician whose data is to be plotted.

        :return: go.Figure - A Plotly figure containing the pie chart.
        """
        selected_dataset = self.data[self.data["Transaction"] == purchase].groupby(
            ["Politician", subset])["Invested"].sum().reset_index()

        help_df = selected_dataset[selected_dataset["Politician"] == politician]
        labels = help_df.iloc[:, 1]
        values = help_df['Invested'] if purchase == "Purchase" else -help_df['Invested']
        title = help_df.columns[1]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

        fig.update_layout(
            title=f"Average Investment of \n {politician} by {title} - {purchase}",
            template="plotly_white"
        )

        return fig

    def five_days_graph(self, selected_politician: str) -> go.Figure:
        """
        Create a bar graph showing the trading volume over the top 5 days for a specific politician.

        :param selected_politician: str - The politician whose trading volume is to be visualized.

        :return: go.Figure - A Plotly figure containing the bar chart.
        """
        help_df = five_days(self.data, selected_politician)
        help_df_sorted = help_df.sort_values(by="Invested", ascending=False)

        colors = help_df_sorted["Invested"].apply(lambda x: "green" if x > 0 else "red")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=help_df_sorted["Traded"],
            y=help_df_sorted["Invested"],
            name=selected_politician,
            marker=dict(color=colors)
        ))

        fig.update_layout(
            title=f"Days with the biggest trading volume of {selected_politician}",
            xaxis_title="Day",
            yaxis_title="Volume",
            template="plotly_white",
            barmode='relative',
            xaxis=dict(
                type="category",
                tickmode="array",
                tickvals=help_df_sorted["Traded"],
            ),
        )

        return fig
