# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                            value='ALL',  # Default value to show all sites
                                            placeholder="Select a Launch Site here",  # Placeholder text for dropdown
                                            searchable=True  # Allow users to search for specific sites
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,  # Starting point of the slider
                                                max=10000,  # Ending point of the slider
                                                step=1000,  # Interval of the slider
                                                marks={i: f'{i} Kg' for i in range(0, 10001, 2000)},  # Slider labels every 2000 Kg
                                                value=[min_payload, max_payload]  # Default range selection
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# TASK 2: Add a callback function for `site-dropdown` as input and `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # Filtered dataframe
    filtered_df = spacex_df

    if entered_site == 'ALL':
        # If ALL sites are selected, create a pie chart for total success launches for all sites
        fig = px.pie(
            filtered_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches by Site'
        )
        return fig
    else:
        # If a specific site is selected, filter data for that site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Create a pie chart showing success (class=1) vs. failure (class=0) counts for the selected site
        fig = px.pie(
            site_df,
            names='class',
            title=f'Total Success vs. Failure Launches for {entered_site}'
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Extract payload range from slider
    low, high = payload_range

    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site == 'ALL':
        # If all sites selected, create scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites'
        )
    else:
        # Filter data for the selected site
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # Create scatter plot for the selected site
        fig = px.scatter(
            site_filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Outcome for {selected_site}'
        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()