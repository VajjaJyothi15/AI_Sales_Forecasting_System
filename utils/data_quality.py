def calculate_data_quality(df):

    total_cells = (
        df.shape[0] *
        df.shape[1]
    )

    missing = (
        df.isnull()
        .sum()
        .sum()
    )

    score = (
        (total_cells - missing)
        / total_cells
    ) * 100

    return round(score, 2)