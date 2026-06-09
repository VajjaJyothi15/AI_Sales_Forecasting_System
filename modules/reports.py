import streamlit as st
import os
from utils.column_mapper import standardize_columns

from reports.pdf_report import (
    generate_pdf_report
)

from reports.excel_export import (
    export_excel
)


def show():

    st.title(
        "📑 Reports Center"
    )

    if "data" not in st.session_state:

        st.warning(
            "Upload Dataset First"
        )

        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    st.subheader(
        "Export Reports"
    )

    # -------------------
    # PDF REPORT
    # -------------------

    if st.button(
        "📄 Generate PDF Report"
    ):

        pdf_path = (
            "generated_report.pdf"
        )

        generate_pdf_report(
            pdf_path,
            df,
            st.session_state.get("forecast_data")
        )

        with open(
            pdf_path,
            "rb"
        ) as file:

            st.download_button(

                label=
                "Download PDF",

                data=file,

                file_name=
                "Sales_Report.pdf",

                mime=
                "application/pdf"
            )

    st.divider()

    # -------------------
    # EXCEL REPORT
    # -------------------

    if st.button(
        "📊 Generate Excel Report"
    ):

        excel_path = (
            "sales_export.xlsx"
        )

        export_excel(
            df,
            excel_path
        )

        with open(
            excel_path,
            "rb"
        ) as file:

            st.download_button(

                label=
                "Download Excel",

                data=file,

                file_name=
                "Sales_Data.xlsx",

                mime=
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.divider()

    # -------------------
    # FORECAST EXPORT
    # -------------------

    if (
        "forecast_data"
        in st.session_state
    ):

        st.subheader(
            "Forecast Export"
        )

        forecast_csv = (

            st.session_state[
                "forecast_data"
            ]

            .to_csv(
                index=False
            )
        )

        st.download_button(

            "⬇ Download Forecast",

            forecast_csv,

            "forecast.csv",

            "text/csv"
        )

    st.divider()

    # -------------------
    # EXECUTIVE SUMMARY
    # -------------------

    st.subheader(
        "Executive Summary"
    )

    st.success(
        """
        Revenue trends analyzed.

        Forecast generated.

        Inventory optimized.

        Business KPIs monitored.

        Recommendations available.
        """
    )
