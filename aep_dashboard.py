# Import required libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Step 1: Load the CSV files into DataFrames
appointments_df = pd.read_csv('data/aep_appointments.csv')
events_df = pd.read_csv('data/aep_events.csv')
policies_df = pd.read_csv('data/aep_policies.csv')

# Data Cleaning and transformations
appointments_df['appointment_time'] = pd.to_datetime(appointments_df['appointment_time'])
events_df = events_df.dropna(subset=['eventstatus'])

# Step 2: Create Interactive Plotly Visualizations with Dark and Vibrant Solid Colors

# Color sequence for vibrant colors
color_sequence = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFBD33', '#33FFF1', '#A833FF']

# Appointments by Event Type with dark vibrant solid colors
fig_appointments = px.bar(appointments_df, x='event', title='Interactive Appointments by Event Type',
                          labels={'event': 'Event Type'}, color='event',
                          color_discrete_sequence=color_sequence)

# Events by Status with a dropdown filter and dark vibrant solid colors
fig_events = px.bar(events_df, x='eventstatus', title='Interactive Events by Status',
                    labels={'eventstatus': 'Event Status'}, color='eventstatus',
                    color_discrete_sequence=color_sequence)

# Policies by Type with dark vibrant solid colors
fig_policies = px.bar(policies_df, x='policy_type', title='Interactive Policies by Type',
                      labels={'policy_type': 'Policy Type'}, color='policy_type',
                      color_discrete_sequence=color_sequence)

# Step 3: Initialize the Dash app
app = dash.Dash(__name__)

# Custom CSS to apply to dropdown menus (including overriding browser defaults)
custom_css = {
    'background-color': '#4a4a4a',  # Dark grey background
    'color': '#FFFFFF',  # White text
    'border': '1px solid #FFFFFF',  # White border
    'padding': '5px',
    'width': '100%'
}

# Define the layout with a dark background and bright, stylish elements
app.layout = html.Div(style={'backgroundColor': '#1a1a1a', 'padding': '20px'}, children=[
    html.H1(children='AEP Dashboard', style={
        'text-align': 'center',
        'color': '#00FF00',
        'font-size': '48px',
        'font-family': 'Verdana, Geneva, sans-serif',
        'text-shadow': '3px 3px #FF0000',
        'letter-spacing': '2px'
    }),

    html.Div(
        children='''Explore interactive visualizations for Appointments, Events, and Policies. Use the filters and buttons to interact with the graphs.''',
        style={'text-align': 'center', 'color': '#FFFFFF', 'font-size': '18px',
               'font-family': 'Courier New, Courier, monospace'}),

    # Appointments Section
    html.H2(children='Appointments by Event Type', style={'color': '#FFA500', 'font-family': 'Georgia, serif'}),
    dcc.Dropdown(
        id='appointments-filter',
        options=[{'label': event, 'value': event} for event in appointments_df['event'].dropna().unique()],
        multi=True,
        placeholder='Filter by event type',
        style=custom_css  # Applying the custom CSS
    ),
    dcc.Graph(id='appointments-graph', figure=fig_appointments),

    # Events Section
    html.H2(children='Events by Status', style={'color': '#33FF57', 'font-family': 'Georgia, serif'}),
    dcc.Dropdown(
        id='events-filter',
        options=[{'label': status, 'value': status} for status in events_df['eventstatus'].dropna().unique()],
        multi=True,
        placeholder='Filter by event status',
        style=custom_css  # Applying the custom CSS
    ),
    dcc.Graph(id='events-graph', figure=fig_events),

    # Policies Section
    html.H2(children='Policies by Type', style={'color': '#FF33FF', 'font-family': 'Georgia, serif'}),
    dcc.Dropdown(
        id='policies-filter',
        options=[{'label': policy, 'value': policy} for policy in policies_df['policy_type'].dropna().unique()],
        multi=True,
        placeholder='Filter by policy type',
        style=custom_css  # Applying the custom CSS
    ),
    dcc.Graph(id='policies-graph', figure=fig_policies)
])


# Step 4: Callbacks for interactivity

# Callback for updating the Appointments chart based on dropdown selection
@app.callback(
    Output('appointments-graph', 'figure'),
    [Input('appointments-filter', 'value')]
)
def update_appointments(selected_event):
    if selected_event is None or selected_event == []:
        filtered_df = appointments_df
    else:
        filtered_df = appointments_df[appointments_df['event'].isin(selected_event)]

    fig = px.bar(filtered_df, x='event', title='Interactive Appointments by Event Type',
                 labels={'event': 'Event Type'}, color='event',
                 color_discrete_sequence=color_sequence)
    fig.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#FFFFFF')
    return fig


# Callback for updating the Events chart based on dropdown selection
@app.callback(
    Output('events-graph', 'figure'),
    [Input('events-filter', 'value')]
)
def update_events(selected_status):
    if selected_status is None or selected_status == []:
        filtered_df = events_df
    else:
        filtered_df = events_df[events_df['eventstatus'].isin(selected_status)]

    fig = px.bar(filtered_df, x='eventstatus', title='Interactive Events by Status',
                 labels={'eventstatus': 'Event Status'}, color='eventstatus',
                 color_discrete_sequence=color_sequence)
    fig.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#FFFFFF')
    return fig


# Callback for updating the Policies chart based on dropdown selection
@app.callback(
    Output('policies-graph', 'figure'),
    [Input('policies-filter', 'value')]
)
def update_policies(selected_policy):
    if selected_policy is None or selected_policy == []:
        filtered_df = policies_df
    else:
        filtered_df = policies_df[policies_df['policy_type'].isin(selected_policy)]

    fig = px.bar(filtered_df, x='policy_type', title='Interactive Policies by Type',
                 labels={'policy_type': 'Policy Type'}, color='policy_type',
                 color_discrete_sequence=color_sequence)
    fig.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#FFFFFF')
    return fig


# Step 5: Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

