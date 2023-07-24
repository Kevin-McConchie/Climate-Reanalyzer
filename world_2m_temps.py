####Compiled from Jupyter Notebook file####

# Dependencies
import json
import requests
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go


# Get data from website and save_to_json_file()
def fetch_world_temperatures():
    url = "https://climatereanalyzer.org/clim/t2_daily/json/cfsr_world_t2_day.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def save_to_json_file(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file)

if __name__ == "__main__":
    world_temperatures = fetch_world_temperatures()
    if world_temperatures is not None:
        save_to_json_file(world_temperatures, "Resources\world_2m_temps.json")
        print("Data successfully fetched and saved to 'world_2m_temps.json' file.")

# Load file for chart generation
def load_json_file(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
        return data

#Line chart generation
def plot_line_graph(data):
    fig = go.Figure()

    for year_data in data:
        year_name = year_data["name"]
        temperatures = year_data["data"]

        # Replace NaN values with None
        temperatures = [temp if temp is not None else None for temp in temperatures]

        # Create x-axis values from the first of each month
        start_date = pd.to_datetime("1979-01-01")
        dates = [start_date + pd.DateOffset(days=i) for i in range(len(temperatures))]

        if year_name == "1979-2000 mean":
            fig.add_trace(go.Scatter(x=dates, y=temperatures, mode='lines', name=year_name, line=dict(color='black', width=2, dash='dot'),
                                    hovertemplate="Date: %{x|%b %d}<br>" +
                                                "Obs Temp: %{y:.2f}°C<br>" +
                                                "Climate Mean: %{customdata[0]:.2f}°C<br>" +
                                                "Anomaly: %{customdata[1]:.2f}°C",
                                    customdata=list(zip(temperatures, [t - temperatures[0] for t in temperatures])),
                                    line_shape="linear", showlegend=True))  # Show legend entry for this trace
        elif year_name in ["plus 2σ", "minus 2σ"]:
            fig.add_trace(go.Scatter(x=dates, y=temperatures, mode='lines', name=year_name, line=dict(color='black', width=2, dash='dot'),
                                    hovertemplate="Date: %{x|%b %d}<br>" +
                                                "Obs Temp: %{y:.2f}°C",
                                    line_shape="linear", showlegend=True))  # Show legend entry for this trace
        elif year_name == "2022":
            fig.add_trace(go.Scatter(x=dates, y=temperatures, mode='lines', name=year_name, line=dict(color='orange', width=2),
                                    hovertemplate="Date: %{x|%b %d}<br>Obs Temp: %{y:.2f}°C",
                                    line_shape="linear", showlegend=True))  # Show legend entry for this trace
        elif year_name == "2023":
            fig.add_trace(go.Scatter(x=dates, y=temperatures, mode='lines', name=year_name, line=dict(color='black', width=2),
                                    hovertemplate="Date: %{x|%b %d}<br>Obs Temp: %{y:.2f}°C",
                                    line_shape="linear", showlegend=True))  # Show legend entry for this trace
        else:
            fig.add_trace(go.Scatter(x=dates, y=temperatures, mode='lines', name=year_name, line=dict(color='grey', width=1),
                                    hovertemplate="Date: %{x|%b %d}<br>Obs Temp: %{y:.2f}°C",
                                    line_shape="linear"))  # By default, hide legend entry for this trace

    fig.update_layout(title="2-meter Daily World Temperatures (90°S-90°N, 0-360°E)",
                      yaxis_title="Temperature (°C)",
                      legend_title_text="Year",
                      legend=dict(orientation="h", yanchor="bottom", y=-1.02, xanchor="right", x=1),
                      showlegend=True,
                      plot_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(showgrid=True, gridcolor='black', gridwidth=1,
                                 tickvals=pd.date_range(start=f"1979-01-01", end=f"2023-01-01", freq="MS").tolist(),
                                 tickformat="%b %-d"),  # Sets the tick format to display abbreviated month and day without leading zero
                      yaxis=dict(showgrid=True, gridcolor='black', gridwidth=1),
                      width=900, height=800)

    # Add "Show All" and "Hide All" buttons for year selection in the legend
    buttons = [dict(label="Show All",
                    method="update",
                    args=[{"visible": [True] * len(fig.data)}, {"title": "2-meter Daily World Temperatures (90°S-90°N, 0-360°E) "}]),
               dict(label="Hide All",
                    method="update",
                    args=[{"visible": 'legendonly'},
                          {"title": "2-meter Daily World Temperatures (90°S-90°N, 0-360°E)"}])]

    fig.update_layout(updatemenus=[dict(direction='left', pad={'r': 10, 't': 10}, showactive=True, type='buttons',
                                        x=.95, xanchor='right', y=-1, yanchor='top', buttons=buttons)])
    fig.update_xaxes(showline=True, linecolor='black', linewidth=1, mirror=True)
    fig.update_yaxes(showline=True, linecolor='black', linewidth=1, mirror=True)

    # Center the title
    fig.update_layout(title_x=0.5)

    # Add subhead (data source) underneath the title
    fig.add_annotation(
        go.layout.Annotation(
            text="Data Source: https://climatereanalyzer.org/clim/t2_daily/",
            xref="paper", yref="paper",
            x=0.5, y=-0.15,
            showarrow=False,
            font=dict(size=10)
        )
    )

    return fig  # Return the figure to use it later

if __name__ == "__main__":
    data = load_json_file("Resources\world_2m_temps.json")
    if data is not None:
        fig = plot_line_graph(data)
        fig.show()      