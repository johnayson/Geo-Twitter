# -*- coding: utf-8 -*-
#Data Visualization app of twitter data
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlite3



def get_df():
   # Create your connection.
   cnx = sqlite3.connect('tweets.db')

   df = pd.read_sql_query("SELECT * FROM geo_tweets", cnx)
   #print(df['coordinate_x'])
   return df


tweets_df = get_df()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout_map = dict(
    autosize=True,
    height=500,
    #font=dict(color="#191A1A"),
    #titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Tweets around the world',
    #style="open-street-map"
    mapbox=dict(
        #accesstoken=mapbox_access_token,
        style="open-street-map",
        #center=dict(
        #    lon=-73.91251,
        #    lat=40.7342
        #),
        #zoom=10
    )
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(id='map-graph',
	figure = {
           "data": [{
	      "type": "scattermapbox",
	      "lat": tweets_df['coordinate_y'], #["36.7505", "40.8296", "42.7484", "44.7069", "39.7527"],
	      "lon": tweets_df['coordinate_x'],#["-73.9934", "-73.9262", "-73.9857", "-74.0113"],
              #"mode": "markers" ,
              #"name": "xyz",
              "hoverinfo": "text",
              #"text" : "Location: {loc} <bri>hash: {hash} ".format(loc=tweets_df['location'] , hash=tweets_df['hash'])
              "text" : [["Location: {loc} <br /> hash: {hash} ".format(loc=i,hash=j)] for i,j in zip(tweets_df['location'],tweets_df['hash'])],
              #"hovertext": [["Name: {} <br>Type: {} <br>Provider: {}".format(i,j,k)]
              #                  for i,j,k in zip("a","b","c")],
	    }],
            'layout': layout_map#{"mapbox" :{"style":"open-street-map" } }#layout_map,

            
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
