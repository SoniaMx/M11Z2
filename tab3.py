from dash import dcc, html
import plotly.graph_objects as go
def render_tab(df):
    
    store_options = [{'label': store, 'value': store} for store in df['Store_type'].unique()]

    layout = html.Div([
        html.H1('Kanały sprzedaży', style={'text-align': 'center'}),

        html.Div([
            dcc.Dropdown(
                id='prod_dropdown',
                options=store_options,
                value=store_options[0]['value'] if store_options else None,
                placeholder='Wybierz kanał sprzedaży'
            ),
            dcc.Graph(id='bar-store')
        ], style={'width': '50%', 'margin': 'auto'}),

        
        html.Div([
            dcc.Graph(id='bar-age-gender')
        ], style={'width': '50%', 'margin': 'auto'}),
    ])

    return layout






