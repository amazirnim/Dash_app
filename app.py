#!/usr/bin/env python
# coding: utf-8

# In[76]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv(
    'nama_10_gdp_1_Data.csv')
df.tail()


available_indicators = df['NA_ITEM'].unique()
geo_indicators = df['GEO'].unique()
unit_indicators = df['UNIT'].unique()

app.layout = html.Div([

######################################### GRAPH 1 ################################################
    
    html.Div([
        
        html.Div([ 
        dcc.RadioItems(
            id='unit_id',
            options=[{'label': i, 'value': i} for i in unit_indicators],
            value='Current prices, million euro',
            labelStyle={'display': 'inline-block'}
        ) 
    ]),
        html.Br(),        
        html.Div([ 
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices' #default value
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}), # this div has two component, needed to split in 2

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}) # right part, to split in 2,
        
        
    ]),

    dcc.Graph(id='indicator-graphic', hoverData={'points': [{'customdata': 'Spain'}]}),
    
    #slider
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),

    html.Br(),
    html.Hr(),
######################################### GRAPH 2 ################################################
    
    html.Div([ 
        html.Div([ 
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in geo_indicators],
                value='Spain' #default value
            ),
            dcc.RadioItems(
                id='xaxis-type2',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}), # this div has two component, needed to split in 2

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type2',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}), # right part, to split in 2,
    ]),

    dcc.Graph(id='indicator-graphic2')
])
    



######################################### CALLBACK 1 ################################################

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'), # for 1 output
    [dash.dependencies.Input('xaxis-column', 'value'),  # we have 5 inputs
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('unit_id', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type_name, yaxis_type_name, unit_id,
                 year_value):
    
    dff = df[df['TIME'] == year_value]
    dff = dff[dff["UNIT"] == unit_id]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            customdata=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type_name == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type_name == 'Linear' else 'log'
            },
            margin={'l': 80, 'b': 40, 't': 40, 'r': 80}
        )   
    }


######################################### CALLBACK CHANGE COUNTRY ################################################

@app.callback(
    dash.dependencies.Output('xaxis-column2', 'options'), 
    [dash.dependencies.Input('indicator-graphic', 'hoverData')])
def change_options_country(hoverData):
    return [{'label': i, 'value': i} for i in geo_indicators[geo_indicators == hoverData['points'][0]['customdata']]]

@app.callback(
    dash.dependencies.Output('xaxis-column2', 'value'),
    [dash.dependencies.Input('xaxis-column2', 'options')])
def change_value_country(available_option):
    return available_option[0]['value']


########################### CALLBACK CHANGE DROPDOWN X in DROPDOWN Y OF THE 2ND GRAPH #############################

@app.callback(
    dash.dependencies.Output('yaxis-column2', 'options'), 
    [dash.dependencies.Input('xaxis-column', 'value')])
def change_options_dropdown(dropdown):
    return [{'label': i, 'value': i} for i in available_indicators[available_indicators == dropdown]]

@app.callback(
    dash.dependencies.Output('yaxis-column2', 'value'),
    [dash.dependencies.Input('yaxis-column2', 'options')])
def change_value_dropdown(available_option):
    return available_option[0]['value']

######################################### CALLBACK 2 ################################################

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'), # for 1 output
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value'),
     dash.dependencies.Input('xaxis-type2', 'value'),
     dash.dependencies.Input('yaxis-type2', 'value'),
     dash.dependencies.Input('unit_id', 'value')])

def update_graph(xaxis_column_name2, yaxis_column_name2, xaxis_type2_name, yaxis_type2_name, unit_id):
    
    dff = df[df['GEO'] == xaxis_column_name2]
    #dff = df[df['GEO'] == hoverData['points'][0]['customdata']]
    dff = dff[dff["UNIT"] == unit_id]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == yaxis_column_name2]['TIME'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name2]['Value'],
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
            }
        )],
        
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name2,
                'type': 'linear' if xaxis_type2_name == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name2,
                'type': 'linear' if yaxis_type2_name == 'Linear' else 'log'
            },
            margin={'l': 80, 'b': 40, 't': 40, 'r': 80},
            hovermode='closest'
        )     
    }

                                                 
if __name__ == '__main__':
    app.run_server()


# In[ ]:




