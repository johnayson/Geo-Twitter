# -*- coding: utf-8 -*-
#Data Visualization app of twitter data
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlite3
import random
import datetime
from dash.dependencies import Input, Output




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
        colors_dict[unique_hashes[i]] ="rgb(" + str(random.randint(0,230)+20) + "," + str(random.randint(0,250)) + "," + str(random.randint(0,250))+ ")"
    #put colors in dictionary, key value

    for  index, row in df.iterrows():
        final_colors.append(colors_dict[row['hash']])

    return final_colors
      #for each position in the list just get the value/color for given hash


   #return 170 #[123,50,170]#random.randint(1,200)
def build_trace(df,this_hash):
    data = dict(
        type = "scattermapbox",
        showlegend = True,
        legendgroup = "group_" + this_hash,
        lat =df[(df['hash']==this_hash)] ['coordinate_y'],
        lon = df[(df['hash']==this_hash)] ['coordinate_x'],
        mode = "markers",
        name = this_hash,
        marker = dict(
            size = 10,
            color = get_colors(df[(df['hash']==this_hash)])
        ),
        hoverinfo = "text",
        text =  [["Location: {loc} <br /> Hash: {hash} <br /> Tweet: {text} ".format(loc=i,hash=j,text=k)]
            for i,j,k in zip(tweets_df[(tweets_df['hash']==this_hash)]['location'],tweets_df[(tweets_df['hash']==this_hash)]['hash'],
                tweets_df[(tweets_df['hash']== this_hash)]['text'])]
     )
    return data


tweets_df = get_df()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
tweets_df = get_df()
hash_list=get_unique_hashes(tweets_df)
final_list = []
#print(len(tweets_df))
for hash in hash_list:
    trace = build_trace(tweets_df,hash)
    final_list.append(trace)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout_map = dict(
    showlegend = True,
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffefc',
    paper_bgcolor='#fffefc',
    marker=dict(
            size=8,
            color="#191A1A",
            opacity=0.7,
            symbol=3
    ),
    legend=dict(font=dict(size=30), orientation='h'),
    title='Tweets around the world',
    mapbox=dict(
        style="open-street-map"
    )
)
def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))

# Multiple components can update everytime interval gets fired., n is used for interval
#if just figure 'map-graph'(id),figure
#updates the id comp with a new the return component
# @app.callback(Output('comp','children'),
#               [Input('interval-component', 'n_intervals')])
@app.callback(Output('map-graph','figure'),
              [Input('interval-component', 'n_intervals')])
def start(n):
    # tweets_df = get_df()
    # hash_list=get_unique_hashes(tweets_df)
    # final_list = []
    # #print(len(tweets_df))
    # for hash in hash_list:
    # 	trace = build_trace(tweets_df,hash)
    # 	final_list.append(trace)
    # html_obj = html.Div(id='comp',children=[
    #     html.H1(children='Geo-twitter for Major Professional Sports' + str(datetime.datetime.now())),
    #     html.H2(children='Geo-twitter' + str(len(tweets_df))),
    #     html.Div(children='As of ' + str(datetime.datetime.now())),
    #     dcc.Graph(id='map-graph',
    # 	figure = {
    # 		"data" : final_list,
    #         "layout": {
    # 			"mapbox" :{
    # 				"style":"open-street-map",
    # 				"zoom":1,
    # 				"legend": {"font": {"size":30},"orientation": "h"},
    #
    #
    # 		     },
    # 		#"center": {"lat":40.4637 , "lon":3.7492},
    # 		     "height":600,
    #              "title": "Tweets the last 7 days. Last updated " + str(datetime.datetime.now())
    # 		     #"autosize" : True
    # 		      }
    #
    #
    #          }
    #     ),
    #     dcc.Interval(
    #        id='interval-component',
    #        interval=3*1000, # in milliseconds
    #        n_intervals=0
    #     )
    #
    #  ])
    # return html_obj

    tweets_df = get_df()
    hash_list=get_unique_hashes(tweets_df)
    final_list = []
    #print(len(tweets_df))
    for hash in hash_list:
    	trace = build_trace(tweets_df,hash)
    	final_list.append(trace)
    figure = {
        "data" : final_list,
        "layout": {
            "mapbox" :{
                "style":"open-street-map",
                "zoom":1,
                "legend": {"font": {"size":30},"orientation": "h"}
        },
        #"center": {"lat":40.4637 , "lon":3.7492},
        "title": "Tweets count " + str(len(tweets_df))+"\n Tweets the last 7 days. Last updated " + str(datetime.datetime.now()),
        "height":600,
        "autosize" : True

        }


         }

    return figure

#app.layout = start
app.layout = html.Div(id ='comp',children=[
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
		    "height":600,
		    "autosize" : True

		}


     }
     ),
     dcc.Interval(
        id='interval-component',
        interval=120*1000, # in milliseconds
        n_intervals=0
    )
 ])


if __name__ == '__main__':
    app.run_server(debug=True)
