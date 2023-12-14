import datetime as dt

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate

from auto_date_callbacks import setup_autodates, autodates_component, trunc_timestamp
from data_global import ERRORS
from tab_by_error import tab_1_component
from tab_by_user import tab_by_user_component
from tab_history import tab_history_component
# from tab_history import tab_history_component
from validation import parse_dates

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=['https://cdn.plot.ly/plotly-locale-ru-latest.js'],
           suppress_callback_exceptions=True)
# app.config.supress_callback_exceptions = True

app.layout = dbc.Container(className='p-3', children=[
    html.Div(children=[
        dbc.Alert([dbc.Row([
            dbc.Col("Ебать пиздец ошибка 228!", width=10),
            dbc.Col(html.Div(dbc.Button("Отправить", id="notif-send", className="btn-sm"), className="d-grid"), width=2)
        ])], color="danger"),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Tabs(id="tab", active_tab='tab-errors-total', children=[
                dbc.Tab(label='Ошибки по типам', tab_id='tab-errors-total'),
                dbc.Tab(label='Ошибки по пользователям', tab_id='tab-errors-users'),
                dbc.Tab(label='История ошибок', tab_id='tab-errors-history')
            ]),
            width=9
        ),
        dbc.Col(
            autodates_component(),
            width=3
        )
    ]),
    html.Div([
        html.Div([
            html.Div(id='tab-content')
        ], className='row justify-content-center h-100')
    ], className='container-fluid h-100'),
    dcc.Store(id='period-validated'),
    dcc.Store(id='granularity-validated'),
    dcc.Store(id='user-id-validated')
])

setup_autodates()


@callback(Output('period-validated', 'data'), Input('period', 'value'))
def update_period(period):
    parsed = parse_dates(period)
    if parsed is None:
        raise PreventUpdate()
    return parsed


@callback(Output('granularity-validated', 'data'), Input('granularity', 'value'))
def update_granularity(gran):
    return gran


@callback(Output('user-id-validated', 'data'), Input('user-id', 'value'))
def update_user_id(idx):
    try:
        return  int(idx)
    except:
        raise PreventUpdate()


@callback(Output('tab-content', 'children'),
          Input('tab', 'active_tab'),
          Input('period-validated', 'data'),
          Input('granularity-validated', 'data'),
          Input('user-id-validated', 'data'),
          Input('percent', 'value'))
def render_content(tab, period, granularity, user_id, percent):
    percent = percent == True  # can be none...
    period = dt.date.fromisoformat(period[0]), dt.date.fromisoformat(period[1])
    from_dt = pd.Timestamp(period[0])
    to_dt = pd.Timestamp(period[1], hour=23, minute=59, second=59, microsecond=999)
    errors = ERRORS[ERRORS['timestamp'].between(from_dt, to_dt)]
    errors['timestamp_trunc'] = errors['timestamp'].apply(lambda x: trunc_timestamp(x, granularity))
    if tab == 'tab-errors-total':
        return tab_1_component(errors)
    elif tab == 'tab-errors-users':
        return tab_by_user_component(errors, percent)
    elif tab == 'tab-errors-history':
        # return dcc.Textarea()
        return tab_history_component(errors, user_id)


if __name__ == '__main__':
    app.run(debug=True)
