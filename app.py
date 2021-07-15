# -*- coding: utf-8 -*-

# Run this app with `python app3.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/ 

# based on app3.py and ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# modebar buttons: https://plotly.com/python/configuration-options/ (remove, or add shape-drawing)
# add text (your name) https://community.plotly.com/t/how-to-add-a-text-area-with-custom-text-as-a-kind-of-legend-in-a-plotly-plot/24349


from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import plotly.express as px
from skimage import io
import numpy as np

#import mydcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)



app.layout = html.Div([
    dcc.Markdown('''
        ### image annotation

        Indicate something on an image or plot.
        Click on the image/plot to make a marker. Click on an existing marker to remove it.

        ----------
        '''),

    dcc.Graph(
        id='image',
        config={
            'staticPlot': False,  # True, False
            'scrollZoom': False,  # True, False
            'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
            'showTips': True,  # True, False
            'displayModeBar': True,  # True, False, 'hover'
            'watermark': False,
            'modeBarButtonsToRemove': ['resetAxis', 'pan2d', 'resetScale2d', 'select2d', 'lasso2d', 'zoom2d',
                                       'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverCompareCartesian',
                                       'hoverClosestCartesian'],
        }
    ),

    dcc.Graph(
        id='graph',
        config={
            'staticPlot': False,  # True, False
            'scrollZoom': False,  # True, False
            'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
            'showTips': True,  # True, False
            'displayModeBar': True,  # True, False, 'hover'
            'watermark': False,
            'modeBarButtonsToRemove': ['resetAxis', 'pan2d', 'resetScale2d', 'select2d', 'lasso2d', 'zoom2d',
                                       'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverCompareCartesian',
                                       'hoverClosestCartesian'],
        }
    ),

    dcc.Markdown('''
        ----
        
        ### Questions students could consider

        Later
  
        ''')
], style={'width': '600px'}
)



#Code for clicking on an image

#global variable to keep track of clicked points
image_clicked_points = []

# The callback function with it's app.callback wrapper.
@app.callback(
    Output('image', 'figure'),
    Input('image', 'clickData'),
    )    
def update_graph(click_data):
    global image_clicked_points
    #images in plotly from: https://plotly.com/python/imshow/
    img = io.imread('https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/240px-Crab_Nebula.jpg')
    fig = px.imshow(img)

    #customizing the hover labels
    fig.update_traces(hovertemplate="x:%{x}<br>y:%{y}</br><extra></extra>")

    #fig.update_layout(width=800, height=600)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    if click_data is not None:
        new_x = click_data['points'][0]['x']
        new_y = click_data['points'][0]['y']

        if [new_x, new_y] in image_clicked_points:
            image_clicked_points.remove([new_x, new_y]) #removing a marker
        else:
            image_clicked_points.append([new_x, new_y]) #adding the new clicked point to a list of all clicked points

    for point in image_clicked_points: #drawing all the markers in the list
        fig.add_trace(go.Scatter(x=[point[0]], y=[point[1]], mode='markers', marker=dict(size=12,
            color='rgb(255, 0, 127)'), showlegend=False, hovertemplate="<br>x=%{x}</br>y=%{y}<extra></extra>"))

    return fig 


#Code for clicking on a plot

#global variable to keep track of clicked points
graph_clicked_points = []

# The callback function with it's app.callback wrapper.
@app.callback(
    Output('graph', 'figure'),
    Input('graph', 'clickData'),
    )
def update_graph(click_data):
    global graph_clicked_points
    #images in plotly from: https://plotly.com/python/imshow/
    np.random.seed(42)
    random_x = np.random.randint(1, 101, 100)
    random_y = np.random.randint(1, 101, 100)
    fig = px.scatter(random_x, random_y)

    #fig.update_traces(hovertemplate="x:%{x}<br>y:%{y}</br><extra></extra>")
    #fig.update_layout(width=800, height=600)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    if click_data is not None:
        new_x = click_data['points'][0]['x']
        new_y = click_data['points'][0]['y']

        if [new_x, new_y] in graph_clicked_points:
            graph_clicked_points.remove([new_x, new_y])
        else:
            graph_clicked_points.append([new_x, new_y])

    for point in graph_clicked_points:
        fig.add_trace(go.Scatter(x=[point[0]], y=[point[1]], mode='markers', marker=dict(size=12,
            color='rgb(255, 0, 127)'), showlegend=False, hovertemplate="<br>x=%{x}</br>y=%{y}<extra></extra>"))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)