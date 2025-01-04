def best_alignment(data_general, data_user):
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
        .rename(columns = {"score" : "MSE score", "alignment" : "Alignment (%)"})  # Sort by alignment (high to low), then score (low to high)
        .head(5)
    )

    return top_5_politicans