import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from astro_clock import Clock
from hypatie.time import download_eot_file
import os

GRwidth = 800
GRheight = 500

if not os.path.isfile('eot_2020_2050.csv'):
    download_eot_file()
eot_df = pd.read_csv('eot_2020_2050.csv')

angularaxis = {'direction': "clockwise",
               'rotation': 90,
               'tickmode':'array',
               'tickvals': np.arange(12)*30,
               'ticktext': ['12'] + [str(i) for i in range(1,12)],
               'showgrid': False,
               'tickfont': {'color': '#A0A0A0'},
               'ticks': 'inside',
               }

radialaxis = {'tickvals':[],
              'ticktext':[],
              'showline': False,
              'range':[0, 1],
              }

dc = {
    'hour'   : {'r':0.5, 'color':'black', 'width':5, 'mode':'lines'},
    'minute' : {'r':0.85,'color':'black', 'width':3, 'mode':'lines'},
    'second' : {'r':0.9, 'color':'black', 'width':1, 'mode':'lines'},
    'lst_deg': {'r':0.8, 'color':'red',   'width':2, 'mode':'lines+markers'},
    }

aries = {
    'font': {'color': 'red', 'size': 15},
    'showarrow': False,
    'text': '\u2648&#xFE0E;',
    'x': 0.86,
    'xanchor': 'center',
    'xref': 'paper',
    'y': 0.725,
    'yanchor': 'bottom',
    'yref': 'paper',
}


def dial(typ, theta):
    data = go.Scatterpolar(
        theta=[0, theta],
        r=[0, dc[typ]['r']],
        mode=dc[typ]['mode'],
        showlegend=False,
        hoverinfo='skip',
        line={'color':dc[typ]['color'], 'width':dc[typ]['width']},
        marker={'symbol':'arrow-bar-up', 'size':10, 'angleref':'previous'},
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
head = 'Powered by: 𝓐𝓼𝓽𝓻𝓸𝓓𝓪𝓽𝓪𝓢𝓬𝓲𝓮𝓷𝓬𝓮.𝓷𝓮𝓽'

app = dash.Dash()

app.layout = html.Div([
    html.Label('Longtitude: '),
    dcc.Input(
            id="lon", type="number",
            placeholder="Enter your longtitude...",
            min=-360, max=360,
            style={'height':'30px', 'width':f'{GRwidth//4}px', "margin-right": f'{GRwidth//4}px'},
        ),
    html.Label(head, style={'horizontal-align':'right',
                                              'width':f'{GRwidth//4}px',
                                              'font-size':'18px',
                                              #'color':'blue', 
                                              }),
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

    t = datetime.utcnow()
    c = Clock(t=t, lon=lon, eot_df=eot_df)
    mst = c.mean_solar_time
    tst = c.true_solar_time
    lst = c.lst

    theta_h, theta_m, theta_s = angles(mst)
    data_mst = []
    data_mst.append(dial('hour', theta_h))
    data_mst.append(dial('minute', theta_m))
    data_mst.append(dial('second', theta_s))

    theta_h, theta_m, theta_s = angles(tst)
    data_tst = []
    data_tst.append(dial('hour', theta_h))
    data_tst.append(dial('minute', theta_m))
    data_tst.append(dial('second', theta_s))

    theta_h, theta_m, theta_s = angles(lst)
    data_lst = []
    data_lst.append(dial('hour', theta_h))
    data_lst.append(dial('minute', theta_m))
    data_lst.append(dial('second', theta_s))

    data_lst.append(dial('lst_deg', c.lst_deg))

    lst_deg = '{0:.3f}'.format(c.lst_deg)
    mst_title = f'Mean solar time:<br>{str(mst)[11:19]}'
    tst_title = f'True solar time:<br>{str(tst)[11:19]}'
    lst_title = f'Local sidereal time:<br>{str(lst)[:8]} ({lst_deg}°)'

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "polar"}, {"type": "polar"}, {"type": "polar"}]],
        subplot_titles=(mst_title, tst_title, lst_title),

        
        #vertical_spacing=0.2,
        horizontal_spacing=0.08,
        #title_y=0.5
        )
    
    
    for i in data_mst:
        fig.add_trace(i, row=1, col=1)
    for i in data_tst:
        fig.add_trace(i, row=1, col=2)
    for i in data_lst:
        fig.add_trace(i, row=1, col=3)

    tit1 = f'<b>Longtitude: {lon}°</b><br>'
    tit2 = f'GMT: {str(t)[:19]}<br>'
    tit3 = f'''<i>Equation of time: {c.eot_str[:-3].replace(":", "':")}"</i><br>'''
    title = tit1 + tit2 + tit3
    
    fig.update_polars({'angularaxis':angularaxis, 'radialaxis':radialaxis},
                      bgcolor='#A0A0A0', #bgcolor of subplots
                      )
    
    fig.update_layout(
        title={'text':title, 'x':0.5, 'y':0.1, 'font':{'color':'white'}},
        height=GRheight, width=GRwidth, #template='plotly_dark',
        paper_bgcolor = "black",
                      )
    
    for i in range(3):
        fig['layout']['annotations'][i].font.color = 'white'
    fig.add_annotation(aries)    
    
    return fig



##fig = update_plot(0,0)
##fig.add_annotation(dc4)
##a = fig['layout']['annotations']
app.run_server(debug=True)

