import plotly.graph_objects as go


def create_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "AI Match Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 40], 'color': "#ffcccc"},
                {'range': [40, 70], 'color': "#ffe599"},
                {'range': [70, 90], 'color': "#b6d7a8"},
                {'range': [90, 100], 'color': "#93c47d"}
            ]
        }
    ))

    return fig