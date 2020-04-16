#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:10:18 2020

@author: zachcornelison
"""

#imports
#from jupyter_plotly_dash import JupyterDash
import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd

#import stylesheet
external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']


df = pd.read_csv('zipcode-data.csv')

df['Zip Code'] = df['Zip Code'].astype(str)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#000000',
    'text': '#5d76a9',
    'label': '#f5b112'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.Div([
            html.H1(
            children='Memphis Zip Code Data',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding-top': 40
                }
            ),
            html.Div(children='Visualizing U.S. Census Bureau datapoints for various Memphis zip codes', style={
            'textAlign': 'center',
            'color': colors['text'],
            'padding-bottom': 40
            })
        ], className='row'),
###############################################################      
        html.Div([
            dcc.Dropdown(
                id='demo-dropdown',
                options=[{'label': i, 'value': i} for i in df['Zip Code']],
                value='null',
                multi=True
            ),
        html.Div(id='dd-output-container')]),
###############################################################        
        html.Div([
            html.Div([
                dcc.Graph(
                    id='graph1'
                )
            ], className='six columns'
            ),
###############################################################  
            html.Div([
                dcc.Graph(
                    id='graph2'
                )
            ], className='six columns'
            ),
###############################################################              
            html.Div(children='', style={
                'padding': 250
            }),
###############################################################
            html.Div([
               dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'padding': '5px'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(212, 225, 250)'
                        }
                    ],
                    style_header={
                        'fontWeight': 'bold'
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Zip Code', 'Area Name']
                    ]),
            ], className='twelve columns'),
###############################################################
            html.Div(children='', style={
                'padding': 250
            }),
###############################################################  
        ], className='row')
    ], className='ten columns offset-by-one'),    
])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)
###############################################################  

@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_image_src(selector):
    filtered_data = df.loc[df['Zip Code'].isin(selector), 
                            ['Area Name', 'percent no internet', 'Zip Code']]
    figure = {
        'data': [{'x': [area_name], 
                  'y': [percent], 
                  'type': 'bar', 
                  'name': zip_code}
                  for area_name, percent, zip_code in filtered_data.to_numpy()
        ],
        'layout': {
            'title': 'Percent of Homes Lacking Broadband Internet',
            'xaxis' : dict(
                title='Area Name',
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='Percent Without Broadband',
                titlefont=dict(
                family='Helvetica, monospace',
                size=18,
                color='#7f7f7f'
            ))
        }
    }
    return figure
###############################################################  
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_image_src(selector):
    filtered_data = df.loc[df['Zip Code'].isin(selector), 
                            ['Area Name', 'Mean Income Past 12 Months', 'Zip Code']]
    figure = {
        'data': [{'x': [area_name], 
                  'y': [income], 
                  'type': 'bar', 
                  'name': zip_code}
                  for area_name, income, zip_code in filtered_data.to_numpy()
        ],
        'layout': {
            'title': 'Mean Home Income Past 12 Months',
            'xaxis' : dict(
                title='Area Name',
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='Income',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
