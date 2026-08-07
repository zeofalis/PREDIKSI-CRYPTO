import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def history_chart(data):

    fig = px.line(
        data,
        x=data.index,
        y="Close",
        template="plotly_dark"
    )

    fig.update_traces(
        line_color="#00FFAB"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        hovermode="x unified",
        height=550
    )

    return fig


def prediction_chart(
    tanggal,
    aktual,
    prediksi
):

    df = pd.DataFrame({

        "Tanggal": tanggal,
        "Aktual": aktual.flatten(),
        "Prediksi": prediksi.flatten()

    })

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(
            x=df["Tanggal"],
            y=df["Aktual"],
            mode="lines",
            name="Aktual"
        )

    )

    fig.add_trace(

        go.Scatter(
            x=df["Tanggal"],
            y=df["Prediksi"],
            mode="lines",
            name="Prediksi"
        )

    )

    fig.update_layout(
        template="plotly_dark",
        height=550
    )

    return fig