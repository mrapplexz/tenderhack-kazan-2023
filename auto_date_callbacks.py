import datetime as dt

import pandas as pd
from dash import callback, Output, Input, html

from validation import fmtdates
import dash_bootstrap_components as dbc


def autodates_component():
    return dbc.Row([
        dbc.Col([
            dbc.Col(
                dbc.Input(
                    placeholder='Период',
                    value=fmtdates(dt.date.today() - dt.timedelta(days=7), dt.date.today()),
                    id='period',
                    size='sm',
                ),
                className='pb-1'
            ),
            html.Div(className='w-100'),
            dbc.Col(
                [
                    html.Div(
                        dbc.Select(
                            options=[
                                {'label': 'по часам', 'value': 'by-hour'},
                                {'label': 'по дням', 'value': 'by-day'},
                                {'label': 'по неделям', 'value': 'by-week'},
                                {'label': 'по месяцам', 'value': 'by-month'},
                            ],
                            value='by-day',
                            id='granularity',
                            size='sm',
                        ), id='granularity-div'
                    ),
                    html.Div(
                        dbc.Input(
                            id="user-id",
                            type="text",
                            size='sm',
                            value="1",
                            placeholder="ID пользователя"
                        ), id='user-id-div'
                    ),
                    html.Div(
                        dbc.Checkbox(
                            id="percent",
                            label="% от пользов. базы"
                        ), id='percent-div'
                    )
                ],
                className='pt-1'
            )
        ], width=8),
        dbc.Col(
            dbc.DropdownMenu(
                label='Авто',
                children=[
                    dbc.DropdownMenuItem("последний день", id='last-day', n_clicks=0),
                    dbc.DropdownMenuItem("последняя неделя", id='last-week', n_clicks=0),
                    dbc.DropdownMenuItem("последние 2 недели", id='last-2-weeks', n_clicks=0),
                    dbc.DropdownMenuItem("последний месяц", id='last-month', n_clicks=0),
                    dbc.DropdownMenuItem("последний год", id='last-year', n_clicks=0),
                ]
            ),
            width=4
        )
    ])


def setup_autodates():
    @callback(Output("granularity", "value", allow_duplicate=True), [Input("last-day", "n_clicks")],
              prevent_initial_call=True)
    def last_day_click_g(n):
        if n > 0:
            return 'by-hour'

    @callback(Output("period", "value", allow_duplicate=True), [Input("last-day", "n_clicks")],
              prevent_initial_call=True)
    def last_day_click_p(n):
        if n > 0:
            return fmtdates(dt.date.today(), dt.date.today())

    @callback(Output("granularity", "value", allow_duplicate=True), [Input("last-week", "n_clicks")],
              prevent_initial_call=True)
    def last_week_click_g(n):
        if n > 0:
            return 'by-day'

    @callback(Output("period", "value", allow_duplicate=True), [Input("last-week", "n_clicks")],
              prevent_initial_call=True)
    def last_week_click_p(n):
        if n > 0:
            return fmtdates(dt.date.today() - dt.timedelta(days=7), dt.date.today())

    @callback(Output("granularity", "value", allow_duplicate=True), [Input("last-2-weeks", "n_clicks")],
              prevent_initial_call=True)
    def last_2_weeks_click_g(n):
        if n > 0:
            return 'by-day'

    @callback(Output("period", "value", allow_duplicate=True), [Input("last-2-weeks", "n_clicks")],
              prevent_initial_call=True)
    def last_2_weeks_click_p(n):
        if n > 0:
            return fmtdates(dt.date.today() - dt.timedelta(days=14), dt.date.today())

    @callback(Output("granularity", "value", allow_duplicate=True), [Input("last-month", "n_clicks")],
              prevent_initial_call=True)
    def last_month_click_g(n):
        if n > 0:
            return 'by-day'

    @callback(Output("period", "value", allow_duplicate=True), [Input("last-month", "n_clicks")],
              prevent_initial_call=True)
    def last_month_click_p(n):
        if n > 0:
            return fmtdates(dt.date.today() - dt.timedelta(days=30), dt.date.today())

    @callback(Output("granularity", "value", allow_duplicate=True), [Input("last-year", "n_clicks")],
              prevent_initial_call=True)
    def last_year_click_g(n):
        if n > 0:
            return 'by-week'

    @callback(Output("period", "value", allow_duplicate=True), [Input("last-year", "n_clicks")],
              prevent_initial_call=True)
    def last_year_click_p(n):
        if n > 0:
            return fmtdates(dt.date.today() - dt.timedelta(days=365), dt.date.today())


@callback(Output('user-id-div', 'className'),
          Input('tab', 'active_tab'))
def class_name_user_id_div(tab):
    if tab == 'tab-errors-history':
        return ''
    else:
        return 'hidden'


@callback(Output('granularity-div', 'className'),
          Input('tab', 'active_tab'))
def class_name_granularity_div(tab):
    if tab == 'tab-errors-history':
        return 'hidden'
    else:
        return ''


@callback(Output('percent-div', 'className'),
          Input('tab', 'active_tab'))
def class_name_percent_div(tab):
    if tab == 'tab-errors-users':
        return ''
    else:
        return 'hidden'


def trunc_timestamp(timestamp: pd.Timestamp, granularity: str):
    if granularity == 'by-hour':
        return pd.Timestamp(year=timestamp.year, month=timestamp.month, day=timestamp.day, hour=timestamp.hour)
    elif granularity == 'by-day':
        return pd.Timestamp(year=timestamp.year, month=timestamp.month, day=timestamp.day)
    elif granularity == 'by-week':
        return pd.Timestamp(year=timestamp.year, month=timestamp.month, day=timestamp.day) - pd.Timedelta(
            days=timestamp.weekday())
    elif granularity == 'by-month':
        return pd.Timestamp(year=timestamp.year, month=timestamp.month, day=1)
