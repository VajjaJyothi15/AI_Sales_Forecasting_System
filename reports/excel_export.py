import pandas as pd


def export_excel(
        df,
        filepath):

    with pd.ExcelWriter(
        filepath
    ) as writer:

        df.to_excel(

            writer,

            sheet_name="Sales Data",

            index=False
        )

    return filepath