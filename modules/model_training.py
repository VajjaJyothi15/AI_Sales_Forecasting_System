import streamlit as st
import plotly.express as px
from utils.column_mapper import standardize_columns

from models.train_models import (
    train_models
)

from models.model_evaluation import (
    get_best_model
)

from models.save_model import (
    save_model
)


def show():

    st.title(
        "🤖 Machine Learning Dashboard"
    )

    if "data" not in st.session_state:

        st.warning(
            "Upload Dataset First"
        )

        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    if df.empty:
        st.warning("Uploaded dataset has no rows to train on.")
        return

    st.info(
        """
        Train multiple machine learning
        models and compare performance.
        """
    )

    if st.button(
        "🚀 Train Models"
    ):

        try:

            results_df, models = (
                train_models(df)
            )

            st.subheader(
                "Model Comparison"
            )

            st.dataframe(
                results_df,
                use_container_width=True
            )

            best = (
                get_best_model(
                    results_df
                )
            )

            st.success(
                f"Best Model: {best['Model']}"
            )

            fig = px.bar(

                results_df,

                x="Model",

                y="R2",

                title=
                "Model Accuracy Comparison"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            best_model_name = (
                best["Model"]
            )

            save_model(

                models[
                    best_model_name
                ],

                "models_saved/best_model.pkl"
            )

            st.success(
                "Model Saved Successfully"
            )

        except Exception as e:

            st.error(
                str(e)
            )
