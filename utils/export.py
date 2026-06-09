def export_excel(
        df,
        file_path):

    df.to_excel(
        file_path,
        index=False
    )