
import pandas as pd
import geopandas as gpd
import math
import json
import os
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

#setting
fw = 60
fig_width = str(fw) + '%'
rest_width = str(100 - fw - 5) + '%'

#from .urls import app_name
population_passenger_app = DjangoDash(name='population_passenger_app')

#for passengers
file_name = os.path.join(os.getcwd(),'data','S12-18_GML','train_passenger.csv')
df = pd.read_csv(file_name,sep='\t')

#for population
geodf = []
# for pref_num in range(8,15,1):
for pref_num in [13]:
    pref_num = str(pref_num).zfill(2)
    pop_shp = os.path.join(os.getcwd(),'data','1km_mesh_suikei_2018_shape_' + pref_num,'1km_mesh_2018_' + pref_num + '.shp')
    if len(geodf)==0:
        geodf = gpd.read_file(pop_shp)
    else:
        tmp_geodf = gpd.read_file(pop_shp)
        geodf = pd.concat([geodf,tmp_geodf])

pop_geojson = os.path.join(os.getcwd(),'data','1km_mesh.geojson')
if os.path.exists(pop_geojson)==False:
    geodf.to_file(pop_geojson, driver = "GeoJSON")

geodf.reset_index(inplace=True)
geodf['id_1'] = geodf.index + 1
geodf['id_2'] = geodf['id_1'].apply(lambda x: str(x).zfill(2))

with open(pop_geojson) as geofile:
    geo_area = json.load(geofile)

i=1
for feature in geo_area["features"]:
    feature ['id'] = str(i).zfill(2)
    i += 1

#for visualization
colors = {
    'background': 'rgb(20,0,121)',
    'text': 'rgb(255, 255, 255)',
}
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

population_passenger_app.layout = html.Div(children=[
        html.Div(children=[
            html.H1(
                children='Population and Train Passengers',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),

            ],
            style={'backgroundColor': colors['background']}),
        html.Div(className="inline-block_test",children=[
            dcc.Loading(
                id="loading-1",
                children=[html.Div(dcc.Graph(id='population-passenger-graph')),
                ],
                type="default",
                ),

            dcc.Markdown("""
                **Seclect year for population**
                """),
            html.P(
                dcc.RangeSlider(
                    id = 'year_population',
                    min=2020,
                    max=2050,
                    step=5,
                    marks={i: i for i in range(2020,2051,5)},
                    value=[2020,2035]

                )),
            dcc.Markdown("""
                **Seclect year for train passengers**
                """),
            html.P(
            dcc.RangeSlider(
                id = 'year_passenger',
                min=2011,
                max=2017,
                step=1,
                marks={i: i for i in range(2011,2018,1)},
                value=[2016,2017]
            )),
            ],style={'width': fig_width, 'display': 'inline-block', 'vertical-align':'top'}
        ),
        html.Div(className="inline-block_test",children=[
            dcc.Markdown("""
                **Hover Data**
            """),
            dcc.Graph(id='hover-data'),
            dcc.Markdown("""
                **Click Data**
            """),
            dcc.Graph(id='click-data'),
            ],
            style={'width': rest_width, 'display': 'inline-block', 'vertical-align':'top'}
        ),
    ],
)
color1 = "rgb(156, 181, 255)"
color2 = "rgb(156, 219, 255)"
color3 = "rgb(156, 255, 243)"
color4 = "rgb(255, 247, 156)"
color5 = "rgb(255, 194, 156)"
color6 = "rgb(255, 156, 156)"
colorscale_population = [
            [0.00, color1],
            [1/6, color1],
            [1/6, color2],
            [2/6, color2],
            [2/6, color3],
            [3/6, color3],
            [3/6, color4],
            [4/6, color4],
            [4/6, color5],
            [5/6, color5],
            [5/6, color6],
            [1.00, color6],
            ]
color1 = "rgb(35, 63, 247)"
color2 = "rgb(35, 205, 247)"
color3 = "rgb(35, 247, 190)"
color4 = "rgb(247, 212, 35)"
color5 = "rgb(247, 155, 35)"
color6 = "rgb(247, 88, 35)"
colorscale_passenger = [
            [0.00, color1],
            [1/6, color1],
            [1/6, color2],
            [2/6, color2],
            [2/6, color3],
            [3/6, color3],
            [3/6, color4],
            [4/6, color4],
            [4/6, color5],
            [5/6, color5],
            [5/6, color6],
            [1.00, color6],
            ]

@population_passenger_app.callback(
    Output('population-passenger-graph', 'figure'),
    [Input('year_population', 'value'),
     Input('year_passenger', 'value')])
def update_glagh(year_population,year_passsenger):
    df['passengers_change'] = df['乗降客数'+str(year_passsenger[1])]/df['乗降客数'+str(year_passsenger[0])] * 100
    df['passengers_change'] = df['passengers_change'].apply(lambda x: 115 if x>115 else 85 if x<85 else float(Decimal(str(x)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)))
    df['text'] = df.apply(lambda x: x['駅名'] + '<br>'                                    
                                    + 'row: ' + str(x.name)+ '<br>'
                                    + 'passengers change: ' + str(x['passengers_change']) + '<br>' 
                                    + str(year_passsenger[0]) + ' daily passengers: ' + str(x['乗降客数'+str(year_passsenger[0])]) + '<br>' 
                                    + str(year_passsenger[1]) + ' daily passengers: ' + str(x['乗降客数'+str(year_passsenger[1])])
                                ,axis=1)
    
    geodf['population_change'] = geodf['PTN_'+ str(year_population[1])] / geodf['PTN_'+ str(year_population[0])] * 100
    geodf['population_change'] = geodf['population_change'].apply(lambda x: 115 if x>115 else 85 if x<85 else float(Decimal(str(x)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)))
    # geodf['text'] = 'test'
    geodf['text'] = geodf.apply(lambda x: 'row: ' + str(x.name )+ '<br>'
                                        + 'population change: ' + str(x['population_change']) + '<br>' 
                                        + str(year_population[0]) + ' daily population: ' + str(x['PTN_'+str(year_population[0])]) + '<br>' 
                                        + str(year_population[1]) + ' daily population: ' + str(x['PTN_'+str(year_population[1])])
                                    ,axis=1)


    fig = go.Figure(go.Choroplethmapbox(name='population',geojson=geo_area, locations=geodf['id_2'], z=geodf['population_change'] ,
                                        text=geodf['text'],
                                        # colorscale="Viridis",
                                        colorscale = colorscale_population, #px.colors.cyclical.IceFire,
                                        marker_opacity=0.4, marker_line_width=0.2,
                                        hoverinfo='text',
                                        colorbar = dict(
                                                x = 1.0,
                                                title={'text':'population' + '<br>' + 'change(%)'}
                                                )))
    fig2 = go.Figure(go.Scattermapbox(name='passsengers', lat=df["lat"], lon=df["lon"],text=df['text'], 
                                        hoverinfo='text',
                                        marker=dict(
                                            # color = df['乗降客数2017'],
                                            color = df['passengers_change'],
                                            size = df['passengers_change'].apply(lambda x: (x-85)/1.2 + 1 if x==x else 1),
                                            colorscale = colorscale_passenger, #px.colors.cyclical.IceFire,
                                            opacity=0.8,
                                            colorbar = dict(
                                                x = 1.08,
                                                title={'text':'passengers' + '<br>' + 'change(%)'}
                                                )
                                        )
                    ))
    fig.add_trace(fig2.data[0])

    fig.update_layout(mapbox_style="carto-positron",
                    mapbox_zoom=8, mapbox_center = {"lat": 35.7, "lon": 139.7},
                    height = 600,
                    margin=dict(l=20, r=0, t=25, b=0),
                    )

    return fig


def linechart(pointData):
    if pointData is None:
        return {'data':'','layout':''}
    else:
        curveNum = pointData['points'][0]['curveNumber']
        txt = pointData['points'][0]['text']

        if curveNum == 0:        
            row = int(txt.split('<br>')[0].split(' ')[1])
            data = [dict(
                    x = [i for i in range(2020,2051,5)],
                    y = [geodf.iloc[row]['PTN_' + str(year)] for year in range(2020,2051,5)],
                    mode = 'lines+markers',
                )]
            layout = {
                    'height': 350,
                    'margin': {'l': 55, 'b': 30, 'r': 10, 't': 15},
                    'annotations': [{
                        'x': 0, 'y': 0.95, 'xanchor': 'left', 'yanchor': 'bottom',
                        'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                        'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                        'text': 'Populatioin',
                    }],
                    'xaxis': {'showgrid': False,'title': 'Year'},
                    'yaxis': {'type': 'linear','title': 'Population'},
                    
                }
        elif curveNum ==1:
            station_name = txt.split('<br>')[0]
            row = int(txt.split('<br>')[1].split(' ')[1])
            data = [dict(
                    x = [i for i in range(2011,2018,1)],
                    y = [df.iloc[row]['乗降客数' + str(year)] for year in range(2011,2018,1)],
                    mode = 'lines+markers',
                )]
            layout = {
                    'height': 350,
                    'margin': {'l': 55, 'b': 30, 'r': 10, 't': 15},
                    'annotations': [{
                        'x': 0, 'y': 0.95, 'xanchor': 'left', 'yanchor': 'bottom',
                        'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                        'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                        'text': 'Train Passenger ' + station_name,
                    }],
                    'xaxis': {'showgrid': False,'title': 'Year'},
                    'yaxis': {'type': 'linear','title': 'Passengers'},
                    
                }
            
        return {
            'data':data,
            'layout': layout
        }

@population_passenger_app.callback(
    Output('hover-data', 'figure'),
    [Input('population-passenger-graph', 'hoverData')])
def display_hover_data(hoverData):
    return linechart(hoverData)

@population_passenger_app.callback(
    Output('click-data', 'figure'),
    [Input('population-passenger-graph', 'clickData')])
def display_click_data(clickData):
    return linechart(clickData)

# population_passenger_app.run_server()
