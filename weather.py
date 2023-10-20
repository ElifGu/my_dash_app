import dash
from dash import Dash, html, dcc, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State

# Lesen der Daten
new = pd.read_csv('heatweaves.csv')
df = pd.read_csv('maxdata.csv')
df_rain = pd.read_csv('maxprecip.csv')
df_min = pd.read_csv('mintemp.csv')
wind = pd.read_csv('windy.csv')

# maximum temperature diagramm

fig_3 = px.choropleth(new,
                    locations='alpha-3',  # Use the 'alpha-3' column for country outlines
                    locationmode='ISO-3',  # Use ISO-3 country codes
                    color='max_temp',
                    projection='natural earth',
                    title='Maximum Temperature of Cities Around the World',
                    animation_frame= 'month',
                    height= 600,
                    color_continuous_scale=px.colors.sequential.Plasma)

# Add the scatter plot on top of the choropleth map
scatter = px.scatter_geo(new,
                         lat='lat',
                         lon='lon',
                         text='city',
                         projection='natural earth')

fig_3.add_trace(scatter.data[0])

# Update the layout to set the country boundaries to black
fig_3.update_geos(
    countrycolor='black',
    showcountries=True,
)

# fig_3 = px.choropleth(
#     df, locations="alpha-3", projection='natural earth',
#     color="max_temp", 
#     hover_name="city", 
#     color_continuous_scale=px.colors.sequential.Reds, range_color= (-30, 40),
#     animation_frame= 'month',
#     height= 600
# )

# maximum preciption bar chart
fig_4 = px.bar(df_rain, x= 'month', y='max_precip_mm', color='city',barmode='group', height= 500, title= 'Maximum precipitation per month in bars')

# minimum temprature map
fig_5 = px.choropleth(
    df_min, locations="alpha-3", projection='natural earth',
    color="min_temp", 
    hover_name="country", 
    color_continuous_scale=px.colors.sequential.ice, range_color= (-55, 25),
    animation_frame= 'month',
    height= 600
)

fig_wind = px.line(wind, x= 'month', y= 'max_wind', markers=True, color= 'city', height= 500, title= 'Maximum Wind')


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
        {'label': 'Show all cities', 'value': 'option1'},
        {'label': 'Option 2', 'value': 'option2'},
        # Füge weitere Optionen hinzu, je nach Bedarf
    ],
    value='option1'  # Standardwert auswählen
)

# Content
content = html.Div([
    html.H3('Heat Waves', style={"paddingLeft": "100px"}),
    dcc.Graph(figure=fig_3),  # Füge das erste Diagramm hinzu
    html.H3('Floods', style={"paddingLeft": "100px"}),
    radio_item_fig_4,  # Füge das Radio-Element für fig_4 hinzu
    dcc.Graph(id='fig-4-graph'),  # Leeres Graph-Element für fig_4
    html.H3('Cold Waves', style={"paddingLeft": "100px"}),
    dcc.Graph(figure=fig_5),
    html.H3('Heavy wind', style={"paddingLeft": "100px"}),
    dcc.Graph(figure=fig_wind)
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