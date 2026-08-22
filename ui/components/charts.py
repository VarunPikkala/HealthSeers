import numpy as np
import plotly.graph_objects as go
import streamlit as st
from utils.theme import get_theme


def _layout(fig, height=280):
    theme = get_theme()
    fig.update_layout(height=height, margin=dict(l=8, r=8, t=24, b=8), paper_bgcolor=theme["glass"], plot_bgcolor=theme["background_secondary"], font=dict(color=theme["text_secondary"], size=11), legend=dict(orientation="h", y=1.12, x=0), hovermode="x unified")
    fig.update_xaxes(showgrid=False, linecolor=theme["border"])
    fig.update_yaxes(showgrid=True, gridcolor=theme["chart_grid"], zeroline=False)
    return fig


def render_disease_trend_chart(row, title="DISEASE TREND"):
    history = list(row.get("history", [0] * 8))
    weeks = [f"W{i}" for i in range(1, len(history) + 1)]
    fig = go.Figure()
    theme = get_theme()
    fig.add_trace(go.Scatter(x=weeks, y=history, name="Historical", mode="lines+markers", line=dict(color=theme["data"], width=3), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=[weeks[-1], "Next week"], y=[history[-1], row.predicted_cases], name="Forecast", mode="lines+markers", line=dict(color=theme["accent"], width=3, dash="dash"), marker=dict(size=6)))
    fig.update_layout(title=dict(text=f"{title} <span style='font-size:11px'>· {row.district}</span>", font=dict(size=14, color=theme["structure"])), yaxis_title="Cases")
    st.plotly_chart(_layout(fig), use_container_width=True, config={"displayModeBar": False})


def render_env_charts(row=None):
    row = row if row is not None else {"precipitation": 42, "temperature": 29, "lai": 2.4}
    weeks = [f"W{i}" for i in range(1, 9)]
    values = [np.linspace(max(10, row["precipitation"] - 28), row["precipitation"], 8), np.linspace(row["temperature"] - 2, row["temperature"], 8), np.linspace(max(0.5, row["lai"] - 0.8), row["lai"], 8)]
    theme = get_theme()
    specs = [("PRECIPITATION", "Weekly precipitation (mm)", values[0], theme["data"]), ("TEMPERATURE", "Weekly temperature (C)", values[1], theme["medium"]), ("LAI", "Environmental indicator", values[2], theme["low"])]
    columns = st.columns(3)
    for column, (title, subtitle, data, color) in zip(columns, specs):
        with column:
            fig = go.Figure(go.Scatter(x=weeks, y=data, mode="lines+markers", line=dict(color=color, width=2), marker=dict(size=5)))
            fig.update_layout(title=dict(text=f"{title}<br><span style='font-size:10px'>{subtitle}</span>", font=dict(size=13, color=theme["structure"])))
            st.plotly_chart(_layout(fig, 220), use_container_width=True, config={"displayModeBar": False})
