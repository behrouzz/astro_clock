import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from astro_clock import Clock


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
    dcc.Input(
            id="lon", type="number", placeholder="Longtitude",
            min=-360, max=360#, step=0.5,
        ),
    dcc.Graph(id='chart'),
    dcc.Interval(id='interval', interval=1*1000, n_intervals=0),

])



@app.callback(
    Output(component_id='chart', component_property='figure'),
    Input(component_id='interval', component_property='n_intervals'),
    Input(component_id='lon', component_property='value'),
)
def update_plot(n, lon):
    if lon is None:
        lon = 0
        
    c = Clock(datetime.utcnow(), lon)
    mst = c.mean_solar_time
    tst = c.true_solar_time
    lst = c.lst

    theta_h, theta_m, theta_s = angles(mst)
    data_mst = []
    data_mst.append(dial(theta_h, r_h))
    data_mst.append(dial(theta_m, r_m))
    data_mst.append(dial(theta_s, r_s))

    theta_h, theta_m, theta_s = angles(tst)
    data_tst = []
    data_tst.append(dial(theta_h, r_h))
    data_tst.append(dial(theta_m, r_m))
    data_tst.append(dial(theta_s, r_s))

    theta_h, theta_m, theta_s = angles(lst)
    data_lst = []
    data_lst.append(dial(theta_h, r_h))
    data_lst.append(dial(theta_m, r_m))
    data_lst.append(dial(theta_s, r_s))

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "polar"}, {"type": "polar"}, {"type": "polar"}]],
        )
    #fig = go.Figure(data=data)
    for i in data_mst:
        fig.add_trace(i, row=1, col=1)
    for i in data_tst:
        fig.add_trace(i, row=1, col=2)
    for i in data_lst:
        fig.add_trace(i, row=1, col=3)
    fig.update_polars({'angularaxis':angularaxis, 'radialaxis':radialaxis})
    fig.update_layout(title=f'Means solar time | Longtitude:{lon}',
                      height=500, width=500, template='plotly_dark')
    return fig


app.run_server(debug=True)

