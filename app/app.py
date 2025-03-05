from flask import Flask, jsonify, request
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import io
import base64
import json 


app = Flask(__name__)



@app.route("/generate-visualisation", methods=["POST"])
def generate_visualisation():

    data = request.json

    meter_data = data['data']['meter']
    intensity_data = data['data']['intensity']


    df_meter = pd.DataFrame(meter_data)
    df_intensity = pd.DataFrame(intensity_data)


    df_meter['CO2 Emission'] = df_meter['datapoint']*df_intensity['datapoint']


    fig = go.Figure(data=[go.Line(x=df_meter['start_datetime'], y=df_meter['CO2 Emission'])])

    fig.update_layout(
        xaxis_title='Date and time',  
        yaxis_title='CO2 Emissions'      
    )

    fig.update_traces(line_color='rgb(1, 102, 102)', line_width=2)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)' 
    )


    fig_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return jsonify({'visualisation_html': fig_html})



@app.route("/generate-pie-visualisation", methods=["POST"])
def generate_style_visualisation():
   
    data = request.json

    energy_data = data

    df_energy = pd.DataFrame(energy_data)


    fig2 = px.pie(df_energy, names=df_energy['fuel'], values=df_energy['perc'], color=df_energy['fuel'],
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

    fig2_html = fig2.to_html(full_html=False, include_plotlyjs='cdn')

    return jsonify({'visualisation_html': fig2_html})


@app.route("/generate-table-visualisation", methods=["POST"])
def generate_style_visualisation():



@app.route("/generate-gauge-visualisation", methods=["POST"])
def generate_style_visualisation():

    # gauge charts
    last_day = data['Datetime (UTC)'].max().normalize()
    previous_day = last_day - pd.Timedelta(days=1) 
    last_day_emissions = data[data['Datetime (UTC)'].dt.normalize() == last_day]['CO2 Emissions'].sum()
    previous_day_emissions = data[data['Datetime (UTC)'].dt.normalize() == previous_day]['CO2 Emissions'].sum()
    
    if previous_day_emissions > 0:
        percentage_increase = ((last_day_emissions - previous_day_emissions) / previous_day_emissions) * 100
    else:
        percentage_increase = 100 if last_day_emissions > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage_increase,
        title={'text': "Percentage Difference in CO2 Emissions from Previous Day"},
        gauge={
            'axis': {'range': [-100, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-100, 0], 'color': "green"},   
                {'range': [0, 20], 'color': "yellow"},   
                {'range': [20, 100], 'color': "red"}     
            ],
        }
    ))
    
    fig.show()
 
 
    start_of_last_week = pd.to_datetime("2025-02-17")
    end_of_last_week = pd.to_datetime("2025-02-23")
    
    start_of_previous_week = pd.to_datetime("2025-02-10")
    end_of_previous_week = pd.to_datetime("2025-02-16")
    
    last_week_emissions = data[(data['Datetime (UTC)'] >= start_of_last_week) & (data['Datetime (UTC)'] <= end_of_last_week)]['CO2 Emissions'].sum()
    
    
    previous_week_emissions = data[(data['Datetime (UTC)'] >= start_of_previous_week) & (data['Datetime (UTC)'] <= end_of_previous_week)]['CO2 Emissions'].sum()
    
    
    if previous_week_emissions > 0:  
        percentage_change = ((last_week_emissions - previous_week_emissions) / previous_week_emissions) * 100
    else:
        percentage_change = 100 if last_week_emissions > 0 else 0
    
    colors = ["#78c6a3", "white", "red"]
    # Create a color scale
    color_scale = [[0, colors[0]], [0.5, colors[1]], [1, colors[2]]]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentage_change,
        title={'text': "Percentage Change in CO2 Emissions (Last Week vs Previous Week)"},
        gauge={
            'axis': {'range': [-100, 100]},  # Range from -100% to 100%
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-100, 0], 'color': "#78c6a3"},   # Good: light green
                {'range': [0, 10], 'color': "#a8e1c6"},     # Blend to a lighter green
                {'range': [10, 20], 'color': "white"},       # Neutral: white
                {'range': [20, 30], 'color': "#f6e6e6"},     # Blend to a light pink
                {'range': [30, 100], 'color': "red"}         # Bad: red
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},  # Pointer line color and width
                'thickness': 0.75,
                'value': percentage_change,  # Position of the pointer
            },
        },
        number={'valueformat': ".0f", 'suffix': "%"}  # Add percentage sign next to the value
    ))
    
    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)