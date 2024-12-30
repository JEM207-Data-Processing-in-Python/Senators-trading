"""
This script contains the function that creates a line graph showing the cumulative investment over time for a specific politician or party.
"""
import plotly.graph_objects as go
from Src.scraping.scraper import load_senators_trading, load_financial_instruments
from Src.visualization.graphs_utils import get_the_color

# TODO error handling, tests, class
def pie_chart_chamber():
    """
    Create a pie chart showing the number of politicians in each chamber.
    """
    data = load_senators_trading()
    help_df = data.groupby("Chamber")["Politician"].nunique().reset_index()

    labels = help_df["Chamber"]
    values = help_df["Politician"]

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Update layout (title)
    fig.update_layout(
        title="Number of Politicians by Chamber",
        template="plotly_white"
    )

    return fig


# TODO error handling, tests, class
def pie_chart_party_invested(data):
    """
    Create a pie chart showing the total investment by each party.
    """
    help_df = data[data["Transaction"] == "Purchase"].groupby("Party")["Invested"].sum().reset_index()

    labels = help_df["Party"]
    values = help_df["Invested"]

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Update layout (title)
    fig.update_layout(
        title="Total Investment by Party",
        template="plotly_white"
    )

    return fig


# TODO error handling, tests, class
def pie_chart_party(data):
    """
    Create a pie chart showing the number of politicians in each chamber.
    """
    help_df = data.groupby("Party")["Politician"].nunique().reset_index()

    labels = help_df["Party"]
    values = help_df["Politician"]

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Update layout (title)
    fig.update_layout(
        title="Number of Politicians by Party",
        template="plotly_white"
    )

    return fig


# TODO error handling, tests, class
def grouping_for_graph(grouping_parametrs, politician, data):
    """
    Allows to group the data by the specified parameters and create a line graph showing the cumulative investment over time for a specific politician or party.
    """
    data_trading_in_time = data[[grouping_parametrs, "Traded", "Invested"]]

    # Group by the specified columns and sum
    data_trading_in_time = data_trading_in_time.groupby([grouping_parametrs, "Traded"]).sum()

    # Reset index after grouping
    data_trading_in_time.reset_index(inplace=True)

    # Calculate the cumulative sum
    data_trading_in_time["cumulative_invested"] = (
        data_trading_in_time.sort_values(by=[grouping_parametrs, "Traded"])
        .groupby(grouping_parametrs)
        .apply(lambda group: group["Invested"].cumsum())
        .reset_index(drop=True)
    )

    # Filter the data based on the politician or party
    help_df = data_trading_in_time[data_trading_in_time[grouping_parametrs] == politician]

    # Set 'Traded' column as the index
    help_df = help_df.set_index("Traded")

    # Get the color for the graph (you may need to implement this function)
    color_of_graph = get_the_color(politician, data)

    # Create the Plotly figure
    fig = go.Figure()

    # Add trace (line graph for cumulative invested)
    fig.add_trace(go.Scatter(x=help_df.index,
                             y=help_df['cumulative_invested'],
                             mode='lines',
                             name=politician,
                             line=dict(color=color_of_graph)))

    # Update layout (labels and title)
    fig.update_layout(
        title=f"Cumulative Investment over Time ({politician})",
        xaxis_title="Time (Traded)",
        yaxis_title="Cumulative Invested",
        xaxis=dict(tickmode='array', tickvals=[help_df.index[0], help_df.index[-1]]),
        template="plotly_white"
    )

    # Show the plot
    return fig


# TODO error handling, tests, class
def pie_chart(data, politician):
    """
    Create a pie chart showing the average investment of a specific politician by the specified parameter.
    """
    help_df = data[data["Politician"] == politician]
    labels = help_df.iloc[:, 1]
    values = help_df['avg_invested']
    title = help_df.columns[1]

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Update layout (title)
    fig.update_layout(
        title=f"Average Investment of {politician} by {title}",
        template="plotly_white"
    )

    # Show the plot
    return fig


# TODO error handling, tests, class
def pie_chart_advanced(data, purchase, subset, politician):
    """
    Create an advanced pie chart showing the average investment of a specific politician by the specified parameter and purchase type.
    """
    selected_dataset = data[data["Transaction"] == purchase].groupby(["Politician", subset])["Invested"].sum().reset_index()

    help_df = selected_dataset[selected_dataset["Politician"] == politician]

    labels = help_df.iloc[:, 1]
    values = help_df['Invested']
    title = help_df.columns[1]

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Update layout (title)
    fig.update_layout(
        title=f"Average Investment of {politician} by {title} ({purchase})",
        template="plotly_white"
    )

    # Show the plot
    return fig

# # Example usage:
# from scraping.scraper import load_senators_trading

# # Load the data
# data = load_senators_trading()

# # Call the function with the loaded data
# grouping_for_graph("Politician", "Cory A. Booker", data)