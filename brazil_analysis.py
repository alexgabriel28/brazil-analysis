# Perform necessary  imports
from dash.dcc import Dropdown
import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

from flask_caching import Cache


import plotly as ply
import plotly.express as px
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import json
from urllib.request import urlopen

# # Violent Deaths by Municipality
# violent_deaths_mun = pd.read_csv(
#     "mortes-violentas-mun.csv",
#     header = 0,
#     delimiter = ";"
# ).rename(
#     columns = {"período":"Year", "nome":"Municipality", "valor":"Deaths"}
# )
#
# # Violent Deaths by Region
# violent_deaths = pd.read_csv(
#     "mortes-violentas-state.csv",
#     header = 0,
#     delimiter = ";"
# ).rename(
#     columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"}
# )

# # Get geo-data for Brazilian Municipalities
# with urlopen('https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json') as response:
#     Brazil_mun = json.load(response)
#
# # Get geo-data for Brazilian States
# with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
#     Brazil = json.load(response)

# with open("C:/Users/gabri/brazil-analysis/assets/brazil_geo.json", "w") as f:
#     json.dump(Brazil, f)
# with open("C:/Users/gabri/brazil-analysis/assets/brazil_mun_geo.json", "w") as f:
#     json.dump(Brazil_mun, f)
# with open('Brazil_Geo.json') as json_file:
#     Brazil = json.load(json_file)
# with open('Brazil_Mun_Geo.json') as json_file:
#     Brazil_mun = json.load(json_file)
#
# # Create State ID Map
# state_id_map = {}
# for feature in Brazil['features']:
#     feature['id'] = feature['properties']['name']
#     state_id_map[feature['properties']['sigla']] = feature['id']
# violent_deaths["State"] = violent_deaths["State_ID"].replace(state_id_map)
#
# # Define function to get the population from the provided .xlsx per year and state
# def get_pop_state(
#     state_id_map,
#     line,
#     year_range = [2000, 2010],
#     path = "retroprojecao_2018_populacao_2000_2010.xlsx"
#     ):
#     cols = [i for i in range(year_range[0], year_range[1]+1)]
#     population_state = pd.DataFrame(columns = cols)
#     for state_id in state_id_map.keys():
#         sheet = pd.read_excel(path, sheet_name = state_id)
#         temp = sheet.iloc[[line], 1:len(cols) + 1]
#         temp.columns = cols
#         temp.index = [state_id]
#         population_state = pd.concat([population_state, temp])
#     return population_state
#
# # Import data
# homicides_men_state = pd.read_csv(
#     "homicides_men_state.csv", delimiter = ";"
#     ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
# homicides_men_state["State"] = homicides_men_state["State_ID"].replace(state_id_map)
#
# homicides_women_state = pd.read_csv(
#     "homicides_women_state.csv", delimiter = ";"
#     ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
# homicides_women_state["State"] = homicides_women_state["State_ID"].replace(state_id_map)
#
# homicides_women_afro_state = pd.read_csv(
#     "homicides_women_afro_state.csv", delimiter = ";"
#     ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
# homicides_women_afro_state["State"] = homicides_women_afro_state["State_ID"].replace(state_id_map)
#
# homicides_men_afro_state = pd.read_csv(
#     "homicides_men_afro_state.csv", delimiter = ";"
#     ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
# homicides_men_afro_state["State"] = homicides_men_afro_state["State_ID"].replace(state_id_map)
#
# temp = pd.merge(
#     homicides_men_state,
#     homicides_women_state,
#     left_on = ["State_ID", "Year", "State", "cod"],
#     right_on = ["State_ID", "Year", "State", "cod"],
#     how = "outer",
#     suffixes = (" Men", " Women")
#     )
#
# temp_2 = pd.merge(homicides_men_afro_state,
#           homicides_women_afro_state,
#           left_on = ["State_ID", "Year", "State", "cod"],
#           right_on = ["State_ID", "Year", "State", "cod"],
#           how = "outer",
#           suffixes = (" Men Afro", " Women Afro")
#          )
#
# homicides_merged = pd.merge(temp,
#           temp_2,
#           left_on = ["State_ID", "Year", "State", "cod"],
#           right_on = ["State_ID", "Year", "State", "cod"],
#           how = "outer",
#          )
#
# homicides_merged["Ratio Fem/Mal"] = homicides_merged["Deaths Women"] / homicides_merged["Deaths Men"]
# homicides_melted = pd.melt(
#     homicides_merged,
#     id_vars = ["cod", "State_ID", "Year", "State", "Ratio Fem/Mal"],
#     var_name = "Victim Group",
#     value_name = "Deaths"
#     )
#
# homicides_melted["Victim Group"] = homicides_melted["Victim Group"].str.replace("Deaths ", "")
# population_state_2000_2010 = get_pop_state(state_id_map, 50)
# population_state_2011_2022 = get_pop_state(
#     state_id_map = state_id_map,
#     line = 50,
#     year_range = [2011, 2023],
#     path = "projection_pop_state_2010_2060.xlsx"
#     )
#
# pop_state_2000_2022 = pd.concat([population_state_2000_2010, population_state_2011_2022], axis = 1)
# pop_state_2000_2022["State_ID"] = pop_state_2000_2022.index
# pop_state_00_22_melted = pd.melt(pop_state_2000_2022, id_vars = "State_ID", var_name = "Year", value_name = "Population")
# pop_state_00_22_melted["Population"] = pop_state_00_22_melted["Population"].astype("int64")
#
# homicides_melted = pd.merge(
#     homicides_melted,
#     pop_state_00_22_melted,
#     left_on = ["State_ID", "Year"],
#     right_on = ["State_ID", "Year"],
#     how = "inner",
#     )
# homicides_melted["Deaths per 100,000"] = (homicides_melted.Deaths/homicides_melted.Population*100000).round(2)
#
# violent_deaths_00_19 = pd.merge(
#     violent_deaths,
#     pop_state_00_22_melted,
#     how = "inner",
#     left_on = ["State_ID", "Year"],
#     right_on = ["State_ID", "Year"])
#

#
# polar_deaths = homicides_melted[homicides_melted.Year.isin([2018, 2019])][homicides_melted["Victim Group"].isin(["Men", "Woman"])]
# polar_deaths = polar_deaths.sort_values("Deaths per 100,000")
with open('brazil_geo.json') as json_file:
    Brazil = json.load(json_file)
with open('brazil_mun_geo.json') as json_file:
    Brazil_mun = json.load(json_file)

# Create State ID Map
state_id_map = {}
for feature in Brazil['features']:
    feature['id'] = feature['properties']['name']
    state_id_map[feature['properties']['sigla']] = feature['id']

polar_deaths = pd.read_csv("polar_deaths.csv")
polar_deaths.Year = polar_deaths.Year.astype("int64")
violent_deaths_00_19 = pd.read_csv("violent_deaths_00_19.csv")
violent_deaths_00_19.Year = violent_deaths_00_19.Year.astype("int64")
homicides_melted = pd.read_csv("homicides_melted.csv")
homicides_melted.Year = homicides_melted.Year.astype("int64")

def create_dropdown_options(input_data):
    options = [{"label":i, "value":i} for i in input_data.sort_values().unique()]
    return options

def create_dropdown_value(input_data):
    value = input_data.sort_values().unique().tolist()
    return value

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'auto'
    }
}

brasil_color_sequence = ["#7BB242","#F5DB00","#1A86C9", "#265073", "#D8576B"]
brasil_color_sequence.extend(px.colors.sequential.Plasma_r)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
    })

@cache.memoize(timeout=600)  # Number of seconds to cache the result
def plot_polar():
    fig_polar = px.scatter_polar(
        polar_deaths,
        r = "Deaths per 100,000",
        theta = "State",
        size = "Population",
        color = "Year",
        color_discrete_sequence=brasil_color_sequence,
        )
    fig_polar.update_layout(font = dict(size = 13))
plot_polar()

# fig_polar = px.scatter_polar(
#     polar_deaths,
#     r = "Deaths per 100,000",
#     theta = "State",
#     size = "Population",
#     color = "Year",
#     color_discrete_sequence=brasil_color_sequence,
#     )
# fig_polar.update_layout(font = dict(size = 13))

@cache.memoize(timeout=600)  # Number of seconds to cache the result
def plot_choropleth():
    fig_map = px.choropleth_mapbox(
        violent_deaths_00_19,
        locations = "State",
        featureidkey = "id",
        geojson = Brazil,
        color = "Deaths",
        hover_name = "State",
        hover_data = ["Deaths", "Year"],
        custom_data = ["State"],
        mapbox_style = "carto-darkmatter",
        color_continuous_scale = "OrRd",
        center = {"lat":-14, "lon":-55},
        zoom = 2,
        opacity = 0.6,
        animation_frame = "Year",
    )

    fig_map.update_geos(fitbounds = "locations", visible = False)
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_layout(
        hovermode='x',
        hoverlabel=dict(bgcolor="rgba(38, 80, 115, 0.75)"),
        font = dict(color = "black"),
        title = dict(
            text = "Total Violent Deaths per State and Year",
            ),
        title_x = 0.5,
        margin = {"t":30, "r":15},
        #zmax = 35000,
        )
plot_choropleth()

mask = homicides_melted["Victim Group"].isin(["Men"])
mask_state = homicides_melted.State.isin(["Rio de Janeiro"])

fig = px.line(
    homicides_melted[mask_state][mask].dropna(),
    x = "Year",
    y = "Deaths per 100,000",
    #size = "Ratio Fem/Mal",
    color = "Victim Group",
    color_discrete_sequence = brasil_color_sequence,
    hover_data = ["Deaths", "Year", "State"],
    hover_name = "Deaths",
)
fig.update_yaxes(range=[0, homicides_melted["Deaths per 100,000"].max()])

app.layout = html.Div(
                children = [
                        html.Header(
                            children = [
                            html.Img(
                                src = app.get_asset_url("brazil_header_img.jpg"),
                                style = {
                                "max-height":"250px",
                                "width":"100%",
                                "object-fit":"cover",
                                "margin":"0px",
                                "padding":"0px",
                                "border":"0px"}
                                ),
                            ], # style = {"background-image": 'url("brazil_header_img.jpg")', "object-fit":"cover", "height":"100px"}
                        ),
                        html.Br(),
                        html.H1(
                        "Analysis of Brazilian Indicators: 2000 - 2019",
                        style = {"textAlign":"center"}
                        ),
                        html.Br(),
                        dcc.Markdown("""
                            This report tries to shine a light on the development of
                            important social, economic and demographic indicators for Brazil.
                            The goal is to find relationships between economic
                            development, education, poverty and violence.
                            """,
                            style = {
                                "textAlign":"center",
                                "marginLeft":"15%",
                                "marginRight":"15%",
                                "font-size":"160%",
                            }
                        ),
                        html.Br(),
                        html.H2("Violence and Homicide", style = {"textAlign":"center"}),
                        html.Br(),
                        html.Div(
                            children = [
                            html.Div(children = [
                                dcc.Graph(
                                    id = "map_deaths",
                                    figure = fig_map,
                                    style = {"display":"inline-block", "height":"85vh", "width":"45vw"},
                                )], style = {"display":"inline-block", "marginRight":"5%"}),
                            html.Div(children = [
                                dcc.Graph(
                                    id = "graph_1",
                                    figure = fig,
                                    style = {
                                        "display":"inline-block",
                                        "height":"75vh",
                                        "width":"45vw",
                                        "verticalAlign":"top",
                                        }
                                    ),
                                dcc.Checklist(
                                    id = "checklist_hom",
                                    options = ["Men", "Men Afro", "Women", "Women Afro"],
                                    inline = True,
                                    value = ["Men"],
                                    style = {"horizontalAlign":"right", "marginRight":"0px"}
                                    # style = {"display":"inline-block"}
                                ),
                            ], style = {
                                "display":"inline-block",
                                "verticalAlign":"top",
                                #"align-items": "right",
                                #"justify-content": "center",
                                "width":"30%"
                            })
                        ], style = {
                            "display":"inline-block",
                            "marginLeft":"2.5%",
                            "marginRight":"2.5%",
                            "max-height":"50%",
                            # "align-items": "center",
                            # "justify-content": "center"
                        }),
                        html.Br(),
                        html.Br(),
                        dcc.Markdown("""
                            ### Comparison of States


                            """
                            , style = {"textAlign":"center"}
                            ),
                        html.Div([
                            html.Div([
                                    dcc.Dropdown(
                                        id = "dropdown_deaths",
                                        multi = True,
                                        options = create_dropdown_options(
                                            homicides_melted["Year"]
                                            ),
                                        value = [2018, 2019],
                                        placeholder = "Select years",
                                    ),
                                    dcc.Graph(
                                        id = "polar_deaths",
                                        figure = fig_polar,
                                        style = {
                                            "height":"85vh", "width":"45vw", "marginRight":"2.5%"
                                        }
                                    )
                                ], style = {"width":"45vw", "display":"inline-block", "marginRight":"2.5%"}),
                              html.Div([
                                    dcc.Markdown("""
                                        Although absolute numbers of violent deaths
                                        remain high and at a disturbing niveau, a consistent
                                        decline in deaths per capita in the densely populated States of
                                        Rio de Janeiro and São Paulo has lead to a overall decline in deaths.
                                        However, there were still ~ 45,000 violent deaths in 2019, making
                                        parts of Brasil a de facto civil war area. The cities with the highest rate
                                        of murders per 100,000 people are Natal and Fortaleza.


                                        > ### Deadliest cities in Brazil (per 100,000)
                                        > ### Natal: 74.67 | Fortaleza: 69.15


                                        However, the deadliest city in the US, St.Louis fares just below
                                        with a rate of 60 murders per 100,000.

                                        Striking is also the disparity between homicides amongst
                                        persons with an african heritage and caucasian descent.

                                        Depending on the state, up to 90 % of violently killed Brazilians are black.
                                        The left graph shows the sorted death rate per 100,000 people per state, with
                                        the bubble size indicating the population size.
                                        """,
                                        style = {
                                                "font-size":"140%",
                                                "display":"inline-block",
                                                "height":"75vh",
                                                "width":"35vw",
                                                "verticalAlign":"middle",
                                                "textAlign":"justify",
                                                "marginLeft":"100px",
                                                "marginTop":"35px"
                                            },
                                        )
                                    ], style = {"display":"inline-block",
                                                "verticalAlign":"top",
                                                "horizontalAlign":"right",
                                                #"align-items": "right",
                                                #"justify-content": "center",
                                                "width":"30%"})
                            ], style = {
                                "display":"inline-block",
                                "marginLeft":"2.5%",
                                "marginRight":"2.5%",
                                "max-height":"50%",
                                # "align-items": "center",
                                # "justify-content": "center"),
                                })
            ])
@app.callback(
    Output("polar_deaths", "figure"),
    Input("dropdown_deaths", "value"),
    )
def update_polar_figure(selection):
    polar_deaths = homicides_melted[homicides_melted["Victim Group"].isin(["Men", "Woman"])]
    years = [2018, 2019]
    if selection:
        years = selection
    polar_deaths = polar_deaths[polar_deaths.Year.isin(years)]
    polar_deaths = polar_deaths.sort_values("Deaths per 100,000")

    fig_polar = px.scatter_polar(
        polar_deaths,
        r = "Deaths per 100,000",
        theta = "State",
        size = "Population",
        color = "Year",
        color_discrete_sequence=brasil_color_sequence,
    )
    fig_polar.update_layout(
        font = dict(size = 13),
        legend=dict(
            yanchor="top",
            xanchor="right",
            y=0.99,
            x = 0.99,
            bgcolor = "rgba(255, 255, 255, 0.4)"
        ),
        margin={"r":10},
    )
    return fig_polar

@app.callback(
    Output("graph_1", "figure"),
    Input("map_deaths", "hoverData"),
    Input("checklist_hom", "value"),
    )
def update_line_homicides(hoverData, hom_type):
    df = homicides_melted
    hom = ["Men"]
    sta = ["Rio de Janeiro"]
    if hom_type:
        hom = hom_type
    if hoverData:
        sta = hoverData['points'][0]['location']
    mask = df["Victim Group"].isin(hom)
    mask_state = df.State.isin([sta])
    fig = px.line(
        df[mask_state][mask].dropna(),
        x = "Year",
        y = "Deaths per 100,000",
        #size = "Ratio Fem/Mal",
        color = "Victim Group",
        color_discrete_sequence = brasil_color_sequence,
        hover_data = ["Deaths", "Year", "State"],
        hover_name = "Deaths",
        title = "Deaths per Victim Group and State \n (hover over map)",
    )
    fig.update_yaxes(range=[0, homicides_melted["Deaths per 100,000"].max()])
    fig.update_layout(
        margin={"t":30, "r":15},
        title_x = 0.5,
        legend=dict(
            yanchor="top",
            xanchor="right",
            y=0.99,
            x = 0.99,
            bgcolor = "rgba(38, 80, 115, 0.3)",
            ),
    )
    return fig

if __name__ == '__main__':
   app.run_server(debug=True) #, port="8055")
