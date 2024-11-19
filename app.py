import pandas as pd
import datetime as dt
import os
from dash import dcc, html
from dash.dependencies import Input, Output
import dash
import plotly.graph_objects as go
import tab1  # Import tab1.py
import tab2  # Import tab2.py

# Database handling
class db:
    def __init__(self):
        self.transactions = self.transation_init()
        self.cc = pd.read_csv(r'db\country_codes.csv', index_col=0)
        self.customers = pd.read_csv(r'db\customers.csv', index_col=0)
        self.prod_info = pd.read_csv(r'db\prod_cat_info.csv')

    @staticmethod
    def transation_init():
        transactions = []  # Start with an empty list
        src = r'db\transactions'
        for filename in os.listdir(src):
            file_path = os.path.join(src, filename)
            transactions.append(pd.read_csv(file_path, index_col=0))  # Append each file to the list

        # Concatenate all DataFrames into a single one
        transactions = pd.concat(transactions, ignore_index=True)

        def convert_dates(x):
            try:
                return dt.datetime.strptime(x, '%d-%m-%Y')
            except ValueError:
                return dt.datetime.strptime(x, '%d/%m/%Y')

        transactions['tran_date'] = transactions['tran_date'].apply(convert_dates)

        return transactions

    def merge(self):
        df = self.transactions.join(
            self.prod_info.drop_duplicates(subset=['prod_cat_code'])
            .set_index('prod_cat_code')['prod_cat'],
            on='prod_cat_code',
            how='left',
        )

        df = df.join(
            self.prod_info.drop_duplicates(subset=['prod_sub_cat_code'])
            .set_index('prod_sub_cat_code')['prod_subcat'],
            on='prod_subcat_code',
            how='left',
        )

        df = df.join(
            self.customers.join(self.cc, on='country_code')
            .set_index('customer_Id'),
            on='cust_id',
        )

        self.merged = df


df = db()
df.merge()

# Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Tabs(
                    id='tabs',
                    value='tab-1',
                    children=[
                        dcc.Tab(label='Sprzedaż globalna', value='tab-1'),
                        dcc.Tab(label='Produkty', value='tab-2'),
                    ],
                ),
                html.Div(id='tabs-content'),
            ],
            style={'width': '80%', 'margin': 'auto'},
        )
    ],
    style={'height': '100%'},
)

@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.render_tab(df.merged)
    elif tab == 'tab-2':
        return tab2.render_tab(df.merged)

if __name__ == '__main__':
    app.run_server(debug=True)
