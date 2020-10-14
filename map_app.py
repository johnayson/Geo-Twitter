# -*- coding: utf-8 -*-
#Data Visualization app of Twitter data
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlite3
import random
import datetime
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate




#build dataframe from database
def get_df():
    # Create your connection.
    cnx = sqlite3.connect('tweets.db')
    df = pd.read_sql_query("SELECT * FROM geo_tweets  where date(created_at) > DATE('now','-7 day') ", cnx)
    return df
def get_unique_hashes(df):
    hashes_list = list(df['hash'].drop_duplicates())
    return hashes_list

#assigns colors to each unique hash in the dataframe
def get_colors(df):
    unique_hashes_cnt = len(df[['hash']].drop_duplicates())
    unique_hashes = list(df['hash'].drop_duplicates())   #df.groupby(['hash'])))
    #unique_colors = []
    colors_dict = {}
    final_colors = []

    #assign colors to each hash
    for i in range(unique_hashes_cnt):
        colors_dict[unique_hashes[i]] ="rgb(" + str(random.randint(0,230)/(i+1)) + "," + str(random.randint(0,250)) + "," + str(random.randint(0,250))+ ")"
    #put colors in dictionary, key value

    for  index, row in df.iterrows():
        final_colors.append(colors_dict[row['hash']])

    return final_colors


def build_trace(df,this_hash):
    tweets_df = get_df()
    data = dict(
        type = "scattermapbox",
        showlegend = True,
        legendgroup = "group_" + this_hash,
        lat =df[(df['hash']==this_hash)] ['coordinate_y'],
        lon = df[(df['hash']==this_hash)] ['coordinate_x'],
        mode = "markers",
        marker = dict(
            size = 10,
            color = get_colors(df[(df['hash']==this_hash)])
        ),
        name = this_hash,
        hoverinfo = "text",
        text =  [["Location: {loc} <br /> Hash: {hash} <br /> Tweet: {text} ".format(loc=i,hash=j,text=k)]
            for i,j,k in zip(tweets_df[(tweets_df['hash']==this_hash)]['location'],tweets_df[(tweets_df['hash']==this_hash)]['hash'],
                tweets_df[(tweets_df['hash']== this_hash)]['text'])]
     )
    return data


#tweets_df = get_df()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def serve_layout():
    tweets_df = get_df()
    hash_list=get_unique_hashes(tweets_df)
    final_list = []
    #print(len(tweets_df))
    for hash in hash_list:
        trace = build_trace(tweets_df,hash)
        final_list.append(trace)
    print("hey")
    print(final_list[0]['marker'])
    init_layout = html.Div(id ='comp',children=[
        html.H1(children='Geo-twitter for Major Professional Sports'),
        #html.Div(id = 'update_ts',children='As of ' + str(datetime.datetime.now())),
        dcc.Graph(id='map-graph',
    	figure = {
    		"data" : final_list,
            "layout": {
    			"mapbox" :{
    				"style":"open-street-map",
    				"zoom":1,
    				"legend": {"font": {"size":30},"orientation": "h"}
    		    },
    		#"center": {"lat":40.4637 , "lon":3.7492},
                "title":"Tweets count " + str(len(tweets_df))+"<br />Tweets the last 7 days. Last updated " + str(datetime.datetime.now()),
    		    "height":600,
    		    "autosize" : True
    		}
         }
         ),
         dcc.Interval(
            id='interval-component',
            interval=30*60*1000, # in milliseconds every 30 minutes
            n_intervals=0
        )
        ])
    return init_layout
# Multiple components can update everytime interval gets fired., n is used for interval
#if just figure 'map-graph'(id),figure
#updates the id comp with a new the return component
# @app.callback(Output('comp','children'),
#               [Input('interval-component', 'n_intervals')])

#Live update based on interval refresh
@app.callback(Output('map-graph','figure'),
              [Input('interval-component', 'n_intervals')])
def start(n):
    #On default, dash sends  callback to page load to every callback
    #if it's a page reload, prevent dynamic page update
    print(n)
    if n is 0:
        raise PreventUpdate

    tweets_df = get_df()
    hash_list=get_unique_hashes(tweets_df)
    #global final_list
    final_list = []
    #print(len(tweets_df))
    for hash in hash_list:
    	trace = build_trace(tweets_df,hash)
    	final_list.append(trace)
    print(final_list[0]['marker'])
    figure = {
        "data" : final_list,
        "layout": {
            "mapbox" :{
                "style":"open-street-map",
                "zoom":1,
                "legend": {"font": {"size":30},"orientation": "h"}
        },
        "title": "Tweets count " + str(len(tweets_df))+"<br /> Tweets the last 7 days. Last updated " + str(datetime.datetime.now()),
        "height":600,
        "autosize" : True

        }


         }

    return figure

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
