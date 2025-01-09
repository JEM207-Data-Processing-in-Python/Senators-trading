"""
This script contains the function that creates a line graph showing the cumulative investment over time for a specific politician or party.
"""
import plotly.graph_objects as go
import pandas as pd
from Src.visualization.graphs_utils import get_the_color, same_color_across_pie_charts
from Src.streamlit.page_1_data_gather import five_days


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
def grouping_for_barchart(grouping_parametrs, politician, data):
    """
    Allows to group the data by the specified parameters and create a bar chart showing the total investment
    over months for a specific politician or party.
    """
    # Extract relevant columns
    data_trading_in_time = data[[
        grouping_parametrs, "Traded", "Invested", "Transaction"
    ]]

    # Ensure that the "Traded" column is in datetime format
    data_trading_in_time["Traded"] = pd.to_datetime(data_trading_in_time["Traded"])

    # Add a new column for the month and year (using 'strftime' to get "YYYY-MM" format)
    data_trading_in_time["Month"] = data_trading_in_time["Traded"].dt.strftime('%Y-%m')

    # Group by the specified parameter (politician or party) and by Month, summing the Invested amounts
    monthly_investment = data_trading_in_time.groupby(
        [grouping_parametrs, "Month"])["Invested"].sum().reset_index()

    # Filter the data based on the politician or party
    help_df = monthly_investment[monthly_investment[grouping_parametrs] == politician]

    # Determine the bar colors (green for positive, red for negative)
    colors = help_df["Invested"].apply(lambda x: "green" if x > 0 else "red")

    # Create the Plotly bar chart
    fig = go.Figure()

    # Add bar trace for the investment per month
    fig.add_trace(go.Bar(
        x=help_df["Month"],
        y=help_df["Invested"],
        name=politician,
        marker=dict(color=colors)
    ))

    # Update layout (labels and title)
    fig.update_layout(
        title=f"Total Investment per Month ({politician})",
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
    selected_dataset = data[data["Transaction"] == purchase].groupby(
        ["Politician", subset])["Invested"].sum().reset_index()

    help_df = selected_dataset[selected_dataset["Politician"] == politician]

    labels = help_df.iloc[:, 1]
    if purchase == "Purchase":
        values = help_df['Invested']
    else:
        values = -help_df['Invested']
    title = help_df.columns[1]

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    # Update layout (title)
    fig.update_layout(
        title=(f"Average Investment of \n {politician} by {title} \n ({purchase})"),
        template="plotly_white"
    )

    # Show the plot
    return fig


def pie_chart_politician_page_five(data, purchase, subset, politician, list_of_sectors_instruments):
    """
    Create an advanced pie chart showing the average investment of a specific politician by the specified parameter and purchase type.
    """
    # Get consistent colors for the list_of_sectors_instruments
    colors = same_color_across_pie_charts(list_of_sectors_instruments)

    # Filter and aggregate data
    selected_dataset = data[data["Transaction"] == purchase].groupby(
        ["Politician", subset])["Invested"].sum().reset_index()
    help_df = selected_dataset[selected_dataset["Politician"] == politician]

    # Prepare data for the pie chart
    labels = help_df.iloc[:, 1]  # Subset column
    if purchase == "Purchase":
        values = help_df['Invested']
    else:
        values = -help_df['Invested']

    # Match colors to labels
    default_color = "#d3d3d3"
    pie_colors = [colors[label] if label in colors else default_color for label in labels]

    # Create the Plotly pie chart
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            marker=dict(colors=pie_colors),  # Assign custom colors
        )]
    )

    # Update layout (title and style)
    fig.update_layout(
        title=f"{politician}'s exposure to the EQUITY:",
        template="plotly_white"
    )

    # Return the plot
    return fig


def pie_chart_user_page_five(data, list_of_sectors_instruments, what):
    """
    Create a pie chart showing the average investment of a user by list_of_sectors_instruments with consistent colors.
    """
    # Dynamically create consistent color mapping
    colors = same_color_across_pie_charts(list_of_sectors_instruments)

    # Prepare data for the pie chart
    labels = data[what]
    values = data["Invested by User"]

    # Match colors to labels
    default_color = "#d3d3d3"
    pie_colors = [colors[label] if label in colors else default_color for label in labels]

    # Create the Plotly pie chart
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            marker=dict(colors=pie_colors),  # Assign custom colors
        )]
    )

    # Update layout (title and style)
    fig.update_layout(
        title="Your exposure to the EQUITY:",
        template="plotly_white"
    )

    # Return the plot
    return fig


def five_days_graph(data, selected_politician):
    help_df = five_days(data, selected_politician)

    help_df_sorted = help_df.sort_values(by="Invested", ascending=False)

    colors = help_df_sorted["Invested"].apply(lambda x: "green" if x > 0 else "red")

    # Create the Plotly bar chart
    fig = go.Figure()

    # Add bar trace for the investment per month
    fig.add_trace(go.Bar(
        x=help_df_sorted["Traded"],
        y=help_df_sorted["Invested"],
        name=selected_politician,
        marker=dict(color=colors)
    ))

    # Update layout (labels and title)
    fig.update_layout(
        title=f"Days with the biggest trading volume of ({selected_politician})",
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
