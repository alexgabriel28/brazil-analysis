import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly as ply

state_id_map = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MG': 'Minas Gerais',
    'MS': 'Mato Grosso do Sul',
    'MT': 'Mato Grosso',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'PR': 'Paraná',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'RS': 'Rio Grande do Sul',
    'SC': 'Santa Catarina',
    'SE': 'Sergipe',
    'SP': 'São Paulo',
    'TO': 'Tocantins'
    }

homicides_men_state = pd.read_csv(
    "/content/drive/MyDrive/Brazil Analysis/homicides_men_state.csv", delimiter = ";"
    ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
homicides_men_state["State"] = homicides_men_state["State_ID"].replace(state_id_map)

homicides_women_state = pd.read_csv(
    "/content/drive/MyDrive/Brazil Analysis/homicides_women_state.csv", delimiter = ";"
    ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
homicides_women_state["State"] = homicides_women_state["State_ID"].replace(state_id_map)

homicides_women_afro_state = pd.read_csv(
    "/content/drive/MyDrive/Brazil Analysis/homicides_women_afro_state.csv", delimiter = ";"
    ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
homicides_women_afro_state["State"] = homicides_women_afro_state["State_ID"].replace(state_id_map)

homicides_men_afro_state = pd.read_csv(
    "/content/drive/MyDrive/Brazil Analysis/homicides_men_afro_state.csv", delimiter = ";"
    ).rename(columns = {"nome":"State_ID", "período":"Year", "valor":"Deaths"})
homicides_men_afro_state["State"] = homicides_men_afro_state["State_ID"].replace(state_id_map)

temp = pd.merge(
    homicides_men_state, 
    homicides_women_state, 
    left_on = ["State_ID", "Year", "State", "cod"], 
    right_on = ["State_ID", "Year", "State", "cod"],
    how = "outer",
    suffixes = (" Men", " Women")
    )

temp_2 = pd.merge(homicides_men_afro_state, 
          homicides_women_afro_state,
          left_on = ["State_ID", "Year", "State", "cod"], 
          right_on = ["State_ID", "Year", "State", "cod"],
          how = "outer",
          suffixes = (" Men Afro", " Women Afro")
         )

homicides_merged = pd.merge(temp, 
          temp_2,
          left_on = ["State_ID", "Year", "State", "cod"], 
          right_on = ["State_ID", "Year", "State", "cod"],
          how = "outer",
         )
homicides_melted = pd.melt(homicides_merged, id_vars = ["cod", "State_ID", "Year", "State"], var_name = "hom_type", value_name = "Deaths")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
                       html.H4("Total Deaths"),
                       dcc.Graph(id = "graph_1"),
                       dcc.Checklist(
                           id = "Total Deaths",
                           options = ["Deaths Men", "Deaths Men Afro", "Deaths Women Afro", "Deaths Women Afro"],
                           inline = True,
                           value = ["Total Men"],
                       ),
])

@app.callback(
    Output("graph_1", "figure"),
    Input("checklist", "value"))
def update_line_homicides(hom_type):
    df = homicides_melted
    mask = df.hom_type.isin(hom_type)
    fig = px.line(
        x = "Year", 
        y = "Deaths", 
        color = "State",
        hover_data = ["Deaths", "Year"],
        hover_name = "Deaths"
    )
    return fig

app.run_server(debug = True)

if __name__ == '__main__':
    app.run_server(debug=True)