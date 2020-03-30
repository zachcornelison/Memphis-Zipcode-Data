#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:10:18 2020

@author: zachcornelison
"""

#imports
#from jupyter_plotly_dash import JupyterDash
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd

#import stylesheet

df = pd.read_csv('zipcode-data.csv')

df['Zip Code'] = df['Zip Code'].astype(str)

# Boostrap CSS.
#import stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.Div([
            html.H1(
            children='Memphis Zip Code Data',
            style={
                'textAlign': 'center',
                'color': colors['text']
                }
            ),
            html.Div(children='Visualizing U.S. Census Bureau datapoints for various Memphis zip codes', style={
            'textAlign': 'center',
            'color': colors['text']
            })
        ], className='row'),
        
        html.Div([
            html.Div([
                dcc.Graph(
                    id='graph1',
                    figure={
                        'data': [
                            {'x': df.iloc[0:4, 1], 'y': df['percent no internet'], 'type': 'bar', 'name': 'Internet'},
                        ],
                        'layout': {
                            'title': 'Percent of homes lacking broadband internet',
                            #'xaxis': 'Zip Code Area',
                            #'yaxis': 'Percent Without Internet',
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            }
                        }
                    }
                )
            ], className='six columns'
            ),
            html.Div([
                dcc.Graph(
                    id='graph2',
                    figure={
                        'data': [
                            {'x': df.iloc[0:5, 1], 'y': df.iloc[0:5,3], 'type': 'bar', 'name': 'Income'},
                        ],
                        'layout': {
                            #'xaxis': 'Zip Code Area',
                            #'yaxis': 'Percent Without Internet',
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            }
                        }
                    }
                )
            ], className='six columns')   
        ], className='row')
    ], className='ten columns offset-by-one'),    
])

if __name__ == '__main__':
    app.run_server(debug=True)
