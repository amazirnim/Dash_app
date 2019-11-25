#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div(children=[ #layout is an imporant feature -> how the dashboard looks like
                                # we write the html inside that the people will see
    html.H1(children='Hello Dash'), 

    
                                # Children is what inside the div -> inside the children there is the text
    html.Div(children=''' 
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={ #figure is a dictionnary where you put the data and the layout to draw a graph
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__': 
    app.run_server(debug=False)


# In[ ]:




