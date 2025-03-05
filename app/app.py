from flask import Flask, jsonify, request
import plotly.graph_objs as go
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
        plot_bgcolor='white',  
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

    data_dict = json.loads(json_data)

    meter_data = data_dict["data"]["meter"]
    df_meter = pd.DataFrame(meter_data)

    intensity_data = data_dict["data"]["intensity"]
    df_intensity = pd.DataFrame(intensity_data)

    df = pd.merge(df_meter[['datapoint', 'start_datetime']], df_intensity[['datapoint', 'start_datetime']], on='start_datetime', suffixes=('_meter', '_intensity'))

    df['CO2_Emissions'] = df['datapoint_meter'] * df['datapoint_intensity']

    df['Datetime (UTC)'] = pd.to_datetime(df['start_datetime'])

    df['Date'] = df['Datetime (UTC)'].dt.date

    daily_emissions = df.groupby('Date')['CO2_Emissions'].sum().reset_index()

    print(daily_emissions)

    last_day = pd.to_datetime(daily_emissions['Date']).max().normalize()
    previous_day = last_day - pd.Timedelta(days=1)
    print(f"Last Day: {last_day}")
    print(f"Previous Day: {previous_day}")

    last_day_emissions = daily_emissions[daily_emissions['Date'] == last_day.date()]['CO2_Emissions'].sum()
    previous_day_emissions = daily_emissions[daily_emissions['Date'] == previous_day.date()]['CO2_Emissions'].sum()

    if previous_day_emissions > 0:
        percentage_increase = ((last_day_emissions - previous_day_emissions) / previous_day_emissions) * 100
    else:
        percentage_increase = 100 if last_day_emissions > 0 else 0 

    fig_guage_day = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentage_increase,
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
                'value': percentage_increase,  # Position of the pointer
            },
        },
        number={'valueformat': ".0f", 'suffix': "%"}  # Add percentage sign next to the value
    ))


    last_7_days = daily_emissions.iloc[-7:]["CO2_Emissions"]
    previous_7_days = daily_emissions.iloc[-14:-7]["CO2_Emissions"]



    last_7_avg = last_7_days.mean()
    previous_7_avg = previous_7_days.mean()

    if previous_7_avg > 0:
        percentage_increase = ((last_7_avg - previous_7_avg) / previous_7_avg) * 100
    else:
        percentage_increase = 100 if last_7_avg > 0 else 0 

    # Create the gauge chart
    fig_guage_week = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentage_increase,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "CO2 Emissions (Last 7 Days Avg)"},
        delta={'reference': previous_7_avg, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [min(previous_7_avg, last_7_avg) - 50, max(previous_7_avg, last_7_avg) + 50]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [min(previous_7_avg, last_7_avg) - 50, previous_7_avg], 'color': "lightgray"},
                {'range': [previous_7_avg, max(previous_7_avg, last_7_avg) + 50], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': previous_7_avg
            }
        }
    ))


    fig_guage_day.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig_guage_week.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig_guage_day_html = fig_guage_day.to_html(full_html=False, include_plotlyjs='cdn')
    fig_guage_week_html = fig_guage_week.to_html(full_html=False, include_plotlyjs='cdn')
    fig_guage_day_emissison_html = last_day_emissions.to_html(full_html=False, include_plotlyjs='cdn')

    return jsonify({'visualisation_guage_day_html': fig_guage_day_html},
                   {'visualisation_guage_week_html': fig_guage_week_html},
                   {'visualisation_day_emission': fig_guage_day_emissison_html})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)