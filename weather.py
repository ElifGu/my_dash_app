import dash
from dash import Dash, html, dcc, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State

# Lesen der Daten
df = pd.read_csv('maxdata.csv')
df_rain = pd.read_csv('maxprecip.csv')
df_min = pd.read_csv('mintemp.csv')

# Erstellung des zweiten Diagramms
fig_2 = px.line(df, x='month', y='max_temp', color='city', height=500, title='Maximum temperature in bars')

# maximum temperature diagramm
fig_3 = px.choropleth(
    df, locations="alpha-3", projection='mercator',
    color="max_temp", 
    hover_name="city", 
    color_continuous_scale=px.colors.sequential.Reds, range_color= (-30, 40),
    animation_frame= 'month',
    height= 600
)

# maximum preciption bar chart
fig_4 = px.bar(df_rain, x= 'month', y='max_precip_mm', color='city',barmode='group', height= 500, title= 'Maximum precipitation per month in bars')

# minimum temprature map
fig_5 = px.choropleth(
    df_min, locations="alpha-3", projection='equal earth',
    color="min_temp", 
    hover_name="country", 
    color_continuous_scale=px.colors.sequential.ice, range_color= (-55, 25),
    animation_frame= 'month',
    height= 600
)

app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

# Header
header = html.Div([
    html.H1(children='Natural disasters caused by weather',
            style={'textAlign': "center", 'color': 'darkslategray'}),
    html.H2('(from October 2022 to October 2023)', style={'textAlign': "center", 'color': 'slategray'})
])

# Footer
footer = html.Div([
    html.P('This is the footer', style={'textAlign': 'center', 'color': 'gray'})
])

# Radio-Element für fig_4 hinzufügen
radio_item_fig_4 = dcc.RadioItems(
    id='radio-fig-4',
    options=[
        {'label': 'Option 1', 'value': 'option1'},
        {'label': 'Option 2', 'value': 'option2'},
        # Füge weitere Optionen hinzu, je nach Bedarf
    ],
    value='option1'  # Standardwert auswählen
)

# Content
content = html.Div([
    html.H3('Heat Waves', style={"paddingLeft": "100px"}),
    dcc.Graph(figure=fig_3),  # Füge das erste Diagramm hinzu
    dcc.Graph(figure=fig_2),   # Füge das zweite Diagramm hinzu
    html.H3('Hard Rainfalls', style={"paddingLeft": "100px"}),
    radio_item_fig_4,  # Füge das Radio-Element für fig_4 hinzu
    dcc.Graph(id='fig-4-graph'),  # Leeres Graph-Element für fig_4
    html.H3('Cold Waves', style={"paddingLeft": "100px"}),
    dcc.Graph(figure=fig_5)
])

# Kombiniere Header, Content und Footer
app.layout = html.Div([
    header,
    content,
    footer
])

# Callback-Funktion, um den Graphen fig_4 basierend auf der ausgewählten Option im Radio-Element zu aktualisieren
@app.callback(
    Output('fig-4-graph', 'figure'),
    Input('radio-fig-4', 'value')
)
def update_fig_4(selected_option):
    # Hier kannst du deine Logik implementieren, um das fig_4-Diagramm basierend auf der ausgewählten Option zu aktualisieren
    # Du kannst die ausgewählte Option verwenden, um die Daten für das Diagramm zu filtern oder zu ändern
    # Erstelle und gib das aktualisierte fig_4-Diagramm zurück
    # Beispiel:
    if selected_option == 'option1':
        updated_fig_4 = px.bar(df_rain, x='month', y='max_precip_mm', color='city', barmode='group', height=500, title='Option 1')
    elif selected_option == 'option2':
        updated_fig_4 = px.bar(df_rain, x='month', y='another_column', color='city', barmode='group', height=500, title='Option 2')
    return updated_fig_4

if __name__ == '__main__':
    app.run_server()

server = app.server  