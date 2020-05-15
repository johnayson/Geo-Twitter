# -*- coding: utf-8 -*-
#Data Visualization app of twitter data
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlite3
import random


def get_df():
    # Create your connection.
    cnx = sqlite3.connect('tweets.db')

    df = pd.read_sql_query("SELECT * FROM geo_tweets  where date(created_at) > date ('2020-05-10') ", cnx)
    #print(df['coordinate_x'])
    return df

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
       
    #print(unique_colors)
    #for i in range(unique_hashes_cnt):
    #    colors_dict[unique_hashes[i]] = unique_colors[i]
    print(colors_dict)
    #put colors in dictionary, key value

    for  index, row in df.iterrows(): 
        final_colors.append(colors_dict[row['hash']])
    print(final_colors)
    
    return final_colors  
      #for each position in the list just get the value/color for given hash
        

   #return 170 #[123,50,170]#random.randint(1,200)
def build_trace(df,this_hash):
    data = dict(
        type = "scattermapbox",
        showlegend = True,
        legendgroup = "group4",
        lat =df[(df['hash']==this_hash)] ['coordinate_y'],
        lon = df[(df['hash']==this_hash)] ['coordinate_x'],
        mode = "markers",
        marker = dict(
            size = 10,
            color = get_colors(df[(df['hash']==this_hash)])
        ),
        text =  [["Location: {loc} <br /> Hash: {hash} <br /> Tweet: {text} ".format(loc=i,hash=j,text=k)] for i,j,k in zip(tweets_df[(tweets_df['hash']==this_hash)]['location'],tweets_df[(tweets_df['hash']==this_hash)]['hash'],tweets_df[(tweets_df['hash']== this_hash)]['text'])]
     )
    return data


tweets_df = get_df()
samp_json = build_trace(tweets_df,'#NHL')
print(samp_json)
colors_list = get_colors(tweets_df)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
    #style="open-street-map"
    mapbox=dict(
        #accesstoken=mapbox_access_token,
        style="open-street-map"
        #legend=dict(font=dict(size=30), orientation='h')
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
              "showlegend":True,"showscale":True,
              "legendgroup":"group1",
	      "lat": tweets_df[(tweets_df['hash']=='#NFL')] ['coordinate_y'],#tweets_df['coordinate_y'], #["36.7505", "40.8296", "42.7484", "44.7069", "39.7527"],
	      "lon": tweets_df[(tweets_df['hash']=='#NFL') ] ['coordinate_x'],#tweets_df['coordinate_x'],#["-73.9934", "-73.9262", "-73.9857", "-74.0113"],
              "mode": "markers" ,
              #k ="".join( "x{i}".format(i = j) for j in range(0,random.randint(1,10)))
              #"symbol" : "square", x="".join("{:2d}".format(i) for i in range(0,random.randint(1,10)))
              "marker" : {"size" : 10,"opacity" : 0.3, "color": get_colors(tweets_df[(tweets_df['hash']=='#NFL') ])},#colors_list},#"".join("rgb({color},0,0)".format(color =ret()))},
              #"name": "xyz",
              "color":"#fffefc",
              "hoverinfo": "text",
              #"text" : "Location: {loc} <bri>hash: {hash} ".format(loc=tweets_df['location'] , hash=tweets_df['hash'])
              "text" : [["Location: {loc} <br /> Hash: {hash} <br /> Tweet: {text} ".format(loc=i,hash=j,text=k)] for i,j,k in zip(tweets_df[(tweets_df['hash']=='#NFL')] ['location'],tweets_df[(tweets_df['hash']=='#NFL')]['hash'],tweets_df[(tweets_df['hash']=='#NFL')]['text'])],
              #"hovertext": [["Name: {} <br>Type: {} <br>Provider: {}".format(i,j,k)]
              #                  for i,j,k in zip("a","b","c")],
	    },
           { 
              "type": "scattermapbox",
              "showlegend":True,"showscale":True,
              "legendgroup":"group2",
              "lat": tweets_df[(tweets_df['hash']=='#MLB') ] ['coordinate_y'],#tweets_df['coordinate_y'], #["36.7505", "40.8296", "42.7484", "44.7069", "39.7527"],
              "lon": tweets_df[(tweets_df['hash']=='#MLB') ] ['coordinate_x'],#tweets_df['coordinate_x'],#["-73.9934", "-73.9262", "-73.9857", "-74.0113"],    
              "mode": "markers" ,
              #k ="".join( "x{i}".format(i = j) for j in range(0,random.randint(1,10)))
              #"symbol" : "square", x="".join("{:2d}".format(i) for i in range(0,random.randint(1,10)))
              "marker" : {"size" : 10,"opacity" : 0.3, "color": get_colors(tweets_df[(tweets_df['hash']=='#MLB') ])},#colors_list},#"".join("rgb({color},0,0)".format(color =ret()))},
              #"name": "xyz",
              "color":"#fffefc",
              "hoverinfo": "text",
              #"text" : "Location: {loc} <bri>hash: {hash} ".format(loc=tweets_df['location'] , hash=tweets_df['hash'])
              "text" : [["Location: {loc} <br /> Hash: {hash} <br /> Tweet: {text} ".format(loc=i,hash=j,text=k)] for i,j,k in zip(tweets_df[(tweets_df['hash']=='#MLB')]['location'],tweets_df[(tweets_df['hash']=='#MLB')]['hash'],tweets_df[(tweets_df['hash']=='#MLB')]['text'])],
              #"hovertext": [["Name: {} <br>Type: {} <br>Provider: {}".format(i,j,k)]
              #                  for i,j,k in zip("a","b","c")],
            },

          {
              "type": "scattermapbox",
              "showlegend":True,"showscale":True,
              "legendgroup":"group3",
              "name": ["turtles","first legend group - average"],
              "lat": ["36.7505", "40.8296", "42.7484", "44.7069", "39.7527"],
              "lon": ["-73.9934", "-73.9262", "-73.9857", "-74.0113"],
              "mode": "markers" ,
              #k ="".join( "x{i}".format(i = j) for j in range(0,random.randint(1,10)))
              #"symbol" : "square", x="".join("{:2d}".format(i) for i in range(0,random.randint(1,10)))
              "marker" : {"size" : 30,"opacity" : 0.3, "color": colors_list},#"".join("rgb({color},0,0)".format(color =ret()))},
              #"name": "xyz",
              "color":"#fffefc",
              "hoverinfo": "text",
              #"text" : "Location: {loc} <bri>hash: {hash} ".format(loc=tweets_df['location'] , hash=tweets_df['hash'])
              "text" : [["Location: {loc} <br /> Hash: {hash} <br /> Tweet: {text} ".format(loc=i,hash=j,text=k)] for i,j,k in zip(tweets_df['location'],tweets_df['hash'],tweets_df['text'])],
              #"hovertext": [["Name: {} <br>Type: {} <br>Provider: {}".format(i,j,k)]
              #                  for i,j,k in zip("a","b","c")],
            },
            samp_json


	    ],
            'layout': {
		"mapbox" :{
			"style":"open-street-map",
			"zoom":1,
			"legend": {"font": {"size":30},"orientation": "h"} 
			},
		#"center": {"lat":40.4637 , "lon":3.7492},
		"height":600,
		"autosize" : True,
		
		}#layout_map,

            
        }
    )
])
print(tweets_df[(tweets_df['hash']=='#NBA') ] ['coordinate_y'])
if __name__ == '__main__':
    app.run_server(debug=True)
