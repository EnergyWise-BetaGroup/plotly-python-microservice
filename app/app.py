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

    fig2.update_layout(legend=dict(y=1.4, orientation='h'))

    fig2_html = fig2.to_html(full_html=False, include_plotlyjs='cdn')

    return jsonify({'visualisation_html': fig2_html})


@app.route("/generate-table-visualisation", methods=["POST"])
def generate_table_visualisation():

    data = request.json

    print("Data:")
    print(data)

    df = pd.DataFrame(data)

    # df= df_input[['start']]  # DataFrame with just 'start' column
    # df_intensity = df_input[['intensity']]

    # df = pd.DataFrame(start)
    # df_intensity = pd.DataFrame(intensity)

    # df['intensity'] = df_intensity['intensity']

    new_df = df.copy()

    new_df['start'] = pd.to_datetime(new_df['start'])

    new_df = new_df.groupby(pd.Grouper(key="start", freq="2h")).mean()
    
    new_df = new_df.iloc[0:12, :]

    print(new_df)

    new_df = new_df.transpose()

    new_df_columns = new_df.columns.tolist()

    print(new_df)

    new_df_values = new_df.iloc[0]

    threshold33 = new_df.quantile(q=0.33, axis=1)

    threshold66 = new_df.quantile(q=0.66, axis=1)

    red = "🟥"
    amber = "🟨"
    green = "🟩"

    def color(a):
        if a > threshold66.iloc[0]:
            return [a, red]
        elif a > threshold33.iloc[0]:
            return [a, amber]
        else:
            return [a, green]

    x = list(map(color, new_df_values))

    def appliance(x):
        list_app = []  
        y = 0

        while y < len(x) - 1: 
            if x[y][1] == "🟩" and x[y + 1][1] == "🟩":
                list_app.append("🚙 🧺")
            elif x[y][1] == "🟩" or x[y + 1][1] == "🟩":
                list_app.append("🧺")
            else:
                list_app.append("") 
            y += 1

        if x[len(x)-1][1] == "🟥":
            list_app.append("")
        elif x[len(x)-1][1] == "🟨":
            list_app.append("")
        elif x[len(x)-1][1] == "🟩" and x[len(x)-2][1] == "🟩":
            list_app.append("🧺")
        elif x[len(x)-1][1] == "🟩":
            list_app.append("🧺")
        return list_app

    emojis = appliance(x)

    table_values = [[emojis[i], x[i][0], x[i][1]] for i in range(len(x))]


    fig3 = go.Figure(data=[go.Table(
                columnwidth = [1000],
                header=dict(values=new_df_columns,
                        line_color='white',
                        fill_color='rgb(1, 102, 102)',
                        align=['center'],
                        font=dict(color='white', size=12),
                        height=70),
                    cells=dict(values=table_values,
                        line_color='white',
                        fill=dict(color=['rgb(221, 252, 233)', 'white','rgb(221, 252, 233)', 'white',
                                        'rgb(221, 252, 233)', 'white','rgb(221, 252, 233)', 'white',
                                        'rgb(221, 252, 233)', 'white','rgb(221, 252, 233)', 'white']),
                        align=['center'],
                        font_size=30,
                        height=100))
                        ])

    fig3_html = fig3.to_html(full_html=False, include_plotlyjs='cdn')

    return jsonify({'visualisation_html': fig3_html})




@app.route("/generate-gauge-visualisation", methods=["POST"])
def generate_gauge_style_visualisation():
    data_dict = request.json
 
    # Convert the meter data to a DataFrame
    meter_data = data_dict["data"]["meter"]

    df_meter = pd.DataFrame(meter_data)
    df_intensity = pd.DataFrame(intensity_data)
    print("df_intensity")
    print(df_intensity)
    # Merge the meter and intensity data on the 'start_datetime' column
    #df = pd.merge(df_meter[['datapoint', 'start_datetime']], df_intensity[['datapoint', 'start_datetime']], on='start_datetime', suffixes=('_meter', '_intensity'))
    #df = df_intensity.merge(df_meter, how='inner', left_on='start_datetime', right_on='start_datetime')
    print("Merged")
    #print(df)
    # Calculate CO2 emissions by multiplying meter datapoint and intensity datapoint
    df_meter['CO2_Emissions'] = df_meter['datapoint'] * df_intensity['datapoint']
    print(df_meter)


    print(df)
 
    # Sum the emissions for each day
    daily_emissions = df.groupby('Date')['CO2_Emissions'].sum().reset_index()
 
    # Print the final results
    print(daily_emissions)
 
    # Print last and previous day for reference
    last_day = pd.to_datetime(daily_emissions['Date']).max().normalize()
    previous_day = last_day - pd.Timedelta(days=1)
 
    last_day_emissions = daily_emissions[daily_emissions['Date'] == last_day.date()]['CO2_Emissions'].sum()
    previous_day_emissions = daily_emissions[daily_emissions['Date'] == previous_day.date()]['CO2_Emissions'].sum()
 
    if previous_day_emissions > 0:
        percentage_increase = ((last_day_emissions - previous_day_emissions) / previous_day_emissions) * 100
    else:
        percentage_increase = 100 if last_day_emissions > 0 else 0
 
    print(percentage_increase)
 
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

    print(fig_guage_day.to_html(full_html=False, include_plotlyjs='cdn'))
 
    fig_guage_day.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
    )

 
    last_7_days = daily_emissions.iloc[-7:]["CO2_Emissions"]
    previous_7_days = daily_emissions.iloc[-14:-7]["CO2_Emissions"]
 
    last_7_avg = last_7_days.mean()
    previous_7_avg = previous_7_days.mean()
 
    if previous_7_avg > 0:
        percentage_increase = ((last_7_avg - previous_7_avg) / previous_7_avg) * 100
    else:
        percentage_increase = 100 if last_7_avg > 0 else 0
 
    fig_guage_week = go.Figure(go.Indicator(
        mode="gauge+number",  # Removing delta mode to avoid potential unwanted dash
        value=percentage_increase,
        title={'text': "Percentage Change in CO2 Emissions (Last Week vs Previous Week)"},
        gauge={
            'axis': {'range': [-100, 100]},  # Range from -100% to 100%
            'bar': {'color': "darkblue"},    # Bar color
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
        number={'valueformat': ".2f", 'suffix': "%", 'font': {'size': 100}},
        domain={
            'x': [0, 1],  # Horizontal position of the gauge (from 0 to 1, meaning left to right)
            'y': [0, 1]  # Lower the value
        }
       
    ))

    print(fig_guage_week.to_html(full_html=False, include_plotlyjs='cdn'))
 
    fig_guage_week.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot background
    )
 
    fig_guage_day_html = fig_guage_day.to_html(full_html=False, include_plotlyjs='cdn')
    fig_guage_week_html = fig_guage_week.to_html(full_html=False, include_plotlyjs='cdn')

    return jsonify({
        'visualisation_guage_day_html': fig_guage_day_html,
        'visualisation_guage_week_html': fig_guage_week_html,
        'visualisation_day_emission': last_day_emissions
    })
 
    #return jsonify({'visualisation_guage_day_html': fig_guage_day_html})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)