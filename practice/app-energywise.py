from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import json

df = pd.read_csv('../data/clean_data.csv')

df2 = pd.read_csv('../data/energy_sources copy.csv') 

columns = df2.columns

values = df2.loc[0, :]

app = Dash()

fig = px.line(df, x='Start', y='CO2 Emissions', labels={'Start':'Datetime', 'CO2 Emissions':'Your CO2 Emissions'})
fig.update_traces(line_color='rgb(1, 102, 102)', line_width=2)
fig.update_layout(
    plot_bgcolor='white',  
)


fig2 = px.pie(df2, names=columns, values=values, color=columns,
              color_discrete_map={'biomass':'rgb(160, 229, 185)',
                                 'coal':'rgb(250, 72, 72)',
                                 'imports':'rgb(53, 63, 66)',
                                 'gas':'rgb(245, 140, 173)',
                                 'nuclear':'rgb(99, 124, 133)',
                                 'other':'rgb(144, 160, 165)',
                                 'hydro':'rgb(34, 155, 137)',
                                 'solar':'rgb(141, 245, 218)',
                                 'wind':'rgb(39, 222, 176)'
                                 })

fig2.update_traces(hole=.4)


app.layout = html.Div(children=[
    html.H1(children='Your Data', style={'textAlign': 'center'}),

    dcc.Graph(
        id='carbon-emissions',
        figure=fig
    ),

    html.H1(children='The current Energy Sources', style={'textAlign': 'center'}),

    dcc.Graph(
        id='energy-piechart',
        figure=fig2
    )
])

if __name__ == '__main__':
    app.run(debug=True)



