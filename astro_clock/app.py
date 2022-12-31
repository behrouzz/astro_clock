import numpy as np
from datetime import datetime
import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


angularaxis = {'direction': "clockwise",
               'rotation': 90,
               'tickmode':'array',
               'tickvals': np.arange(12)*30,
               'ticktext': ['12'] + [str(i) for i in range(1,12)],
               'gridcolor': '#222'}

radialaxis = {'tickvals':[],
              'ticktext':[]}

r_h, r_m, r_s = 0.5, 0.8, 0.9


def dial(theta, r):
    data = go.Scatterpolar(
        theta=[0, theta],
        r=[0, r],
        mode='lines+markers',
        showlegend=False,
        )
    return data


def angles(t):
    s = t.second
    m = t.minute + t.second/60 + (t.microsecond/1000000)/60
    h = t.hour + m/60
    theta_s = t.second * 6
    theta_m = m * 6
    theta_h = h * 30
    return theta_h, theta_m, theta_s

# ============= RUN WITH DASH ================


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='chart'),
    dcc.Interval(id='interval', interval=1*1000, n_intervals=0)
])



@app.callback(
    Output(component_id='chart', component_property='figure'),
    Input(component_id='interval', component_property='n_intervals'),
)
def update_plot(n):

    theta_h, theta_m, theta_s = angles(datetime.utcnow())

    
    data = []
    data.append(dial(theta_h, r_h))
    data.append(dial(theta_m, r_m))
    data.append(dial(theta_s, r_s))

    fig = go.Figure(data=data)
    fig.update_polars({'angularaxis':angularaxis, 'radialaxis':radialaxis})
    fig.update_layout(title='Test', height=700, width=700, template='plotly_dark')
    return fig


app.run_server(debug=True)

