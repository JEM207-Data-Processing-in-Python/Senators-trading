"""
This file contains the graphs for the Instrument Finder page.
"""
import pandas as pd
import plotly.graph_objects as go


class PoliticianGraph:
    def __init__(self, politician_data, selected_instrument):
        self.politician_data = politician_data
        self.selected_instrument = selected_instrument

    def generate_graph(self):
        """
        Generate a price graph for the selected instrument and the politician's trades.

        Returns:
        - fig (plotly.graph_objects.Figure): The figure object to be displayed in Streamlit.
        """
        graph_data = pd.DataFrame(self.politician_data.loc[0]).T
        date_columns = [col for col in graph_data.columns if '-' in col]
        graph_values = graph_data[date_columns].T.reset_index()
        graph_values.columns = ['Date', 'Price']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=graph_values['Date'], y=graph_values['Price'], mode='lines', name='Price'))

        for traded_date in self.politician_data['Traded']:
            fig.add_vline(
                x=traded_date,
                line=dict(color='red', dash='longdash', width=1),
            )

        fig.update_layout(
            title=f"{self.selected_instrument} - Price graph",
            xaxis_title="Date",
            yaxis_title="Price",
        )

        return fig
