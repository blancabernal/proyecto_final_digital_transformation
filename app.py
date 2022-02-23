import dash
import pandas as pd
from dash import dcc
from dash import html
import krakenex
from pykrakenapi import KrakenAPI
from dash.dependencies import Output, Input
import time
from Figure_class import Figure
from vwap import vwap

api = krakenex.API()
k = KrakenAPI(api) #puto obrero que escucha!!

pairs = k.get_tradable_asset_pairs()
criptos = pairs.index

operations = ["buy", "sell"]
data = []

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family = Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "BlancaBernal: TrabajoFinal"
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                    html.H1(
                    children="Trabajo Final", className="header-title"
                ),
                html.P(
                    children="💰 Análisis de la cotización de las criptomonedas y su fluctuación 💰",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Types", className="menu-title"),
                        dcc.Dropdown(
                            id="pairs-filter",
                            options=[
                                {"label": cripto, "value": cripto}
                                for cripto in criptos.unique()
                            ],
                            value="XBTUSDT",
                            clearable=False,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Operation", className="menu-title"),
                        dcc.Dropdown(
                            id="buy_sell-filter",
                            options=[
                                {"label": operation, "value": operation}
                                for operation in operations
                            ],
                            value="buy",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Date Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date_range-filter",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="mix-graph",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("mix-graph", "figure"), Output("date_range-filter", "min_date_allowed"),
     Output("date_range-filter", "max_date_allowed")],
    [
        Input("pairs-filter", "value"),
        Input("buy_sell-filter", "value"),
        Input("date_range-filter", "start_date"),
        Input("date_range-filter", "end_date"),
    ],
)
def update_data (cripto, operation, start_date, end_date):
    recent, last = k.get_recent_trades(cripto, since = 16277760124432, ascending = True)
    new_recent = recent.copy()
    date_times = 0

    while date_times < 3:
        time.sleep(6)
        date_times += 1
        recent, last = k.get_recent_trades(cripto, since = last, ascending = True)
        new_recent = pd.concat([new_recent, recent])

    global data
    data = new_recent
    data = vwap(data)
    min_date_allowed = data.index.min().to_pydatetime()
    max_date_allowed = data.index.max().to_pydatetime()

    filtered_data = data[data.buy_sell == operation]
    if start_date is not None and end_date is not None:
        mask = (
                (data.index >= start_date) & (data.index <= end_date)
        )
        filtered_data = data.loc[mask, :]

    mix_chart_figure = Figure(filtered_data, cripto)
    data_graph = mix_chart_figure.build()

    return data_graph, min_date_allowed, max_date_allowed


if __name__ == "__main__":
    app.run_server(debug=True)