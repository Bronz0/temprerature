import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

# external stylesheet
external_stylessheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylessheets)
app.title = 'Teperature'

# load data
df_all_countries = pd.read_csv('https://raw.githubusercontent.com/Bronz0/temprerature/master/temperatures.csv')
df_global = pd.read_csv('https://raw.githubusercontent.com/Bronz0/temprerature/master/global_temperature.csv')

# get available countries
available_countries = sorted(df_all_countries.country.unique())

control = html.Div([
    dcc.Dropdown(
        id='countries-dropdown',
        options=[{'label': i, 'value': i} for i in available_countries],
        value=str(available_countries[0])
    )
],
    style={'width': '48%', 'display': 'inline-block'}
)

graph = dcc.Graph(id='my-graph')

app.layout = html.Div([
    control,
    graph
])


@app.callback(
    Output('my-graph', 'figure'),
    [Input(component_id='countries-dropdown', component_property='value')])
def update_graph(selected_countrie):
    # filter data by selected country
    filtered_df = df_all_countries[df_all_countries.country == selected_countrie]
    # add the globa data to be returned every time
    result_data = [dict(
        x=df_global.year,
        y=df_global.avg_temp,
        text='Global',
        mode='markers',
        marker={
            'size': 5,
            'opacity': 0.7,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name='global'

    )]

    # filter by cities
    for city in filtered_df.city.unique():
        f = filtered_df[filtered_df.city == city]
        result_data.append(dict(
            x=f.year,
            y=f.groupby('year').avg_temp.mean(),
            text=str(selected_countrie) + "," + str(city),
            mode='markers',
            marker={
                'size': 5,
                'opacity': 0.7,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=str(city)
        ))

    return {
        'data': result_data,
        'layout': dict(
            title='Temperature Changes Over The Time',
            xaxis={'title': 'year'},
            yaxis={'title': 'Avg Temperature (C°)'},
            margin={'l': 40, 'b': 40, 't': 80, 'r': 0},
            hovermode='closest'
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True)
