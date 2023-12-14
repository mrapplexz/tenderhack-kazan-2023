import time
from typing import Set

import dash
import dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input
import dash_core_components as dcc
from dash.exceptions import PreventUpdate

from data_global import USERS
from notification import YandexMailSender, subject_message, get_body_message

sender_config = {
    'mail': {
        'username': 'hack-mts@yandex.ru',
        'password': 'zlhtgwnbzcwvcery'
    }
}


def build_da_big_table(errors: pd.DataFrame, user_id: int):
    return html.Div([
        html.H4(f'Пользователь: {user_id}', style={'color': '#A93226'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in errors[errors['user_id'] == user_id].columns if i not in ['id']],
            data=errors[errors['user_id'] == user_id].sort_values('timestamp', ascending=False).to_dict('records'),
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'backgroundColor': 'rgb(255, 255, 255)',
                'color': 'black',
                'border': '1px solid grey',
                'textAlign': 'left'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ]
        )
    ])


def tab_history_component(errors_in: pd.DataFrame, user_id: int):
    return dbc.Container([
        dbc.CardHeader('User Errors', className="h2", style={'textAlign': 'center',
                                                             'padding': '15px'}),
        dbc.Container([
            dbc.Container([
                dbc.Button(f'Отправить уведомление (0 выбрано)', id='notify', n_clicks=0,
                           style={'margin-left': '10px'}),
                dbc.Button(f'Выбрать всех', id='notify-select-all', n_clicks=0, style={'margin-left': '10px'}),
            ], style={'margin-top': '15px'}),
        ]),
        dbc.Container([
            build_da_big_table(errors_in, user_id)
        ], id='user-output', style={'margin': '50px'}),
        dcc.Store('selected-rows', data=''),
        html.Div(id="email-result")  # Hidden div
    ])


def w_selected_rows(rows: Set[str]):
    return ','.join(map(str, rows))


def r_selected_rows(rows: str):
    return set(map(int, rows.split(','))) if rows != '' else set()


# Handle selection of events
@callback(
    Output('selected-rows', 'data', allow_duplicate=True),
    Input('table', 'active_cell'),
    dash.dependencies.State('table', 'data'),
    dash.dependencies.State('selected-rows', 'data'),
    prevent_initial_call=True
)
def select_row(active_cell, data, selected_rows):
    selected_rows = r_selected_rows(selected_rows)
    if active_cell:
        if active_cell['column_id'] == 'checkbox':
            if data[active_cell['row']]['checkbox'] == '❌':
                selected_rows.add(active_cell['row'])
            else:
                selected_rows.remove(active_cell['row'])

    return w_selected_rows(selected_rows)


@callback(
    [Output('table', 'data', allow_duplicate=True), Output('notify', 'children', allow_duplicate=True)],
    Input('selected-rows', 'data'),
    dash.dependencies.State('table', 'data'),
    prevent_initial_call=True
)
def on_update_selected(selected_rows, data):
    selected_rows = r_selected_rows(selected_rows)
    for i, dat in enumerate(data):
        if i in selected_rows:
            dat['checkbox'] = '✔️'
        else:
            dat['checkbox'] = '❌'
    return data, f'Отправить уведомление ({len(selected_rows)} штук)'


@callback(
    [Output('selected-rows', 'data', allow_duplicate=True), Output('email-result', 'children')],
    Input(component_id='notify', component_property='n_clicks'),
    [
        dash.dependencies.State('table', 'data'),
        dash.dependencies.State('selected-rows', 'data')
    ],
    prevent_initial_call=True
)
def send_notification(n_clicks, table, selected_rows):
    selected_rows = r_selected_rows(selected_rows)
    if n_clicks > 0:
        selected_errors = [x for i, x in enumerate(table) if i in selected_rows]
        for error in selected_errors:
            with YandexMailSender(config=sender_config) as sender:
                sender.send_mail(
                    recipient=USERS.loc[error['user_id']]['email'],
                    subject=subject_message,
                    body=get_body_message(error['error_type']),
                )

            time.sleep(1)
            print('Message has been sent')

        return w_selected_rows(set()), "Сообщение успешно отправлено!"
    raise PreventUpdate()


@callback(
    Output('selected-rows', 'data', allow_duplicate=True),
    Input(component_id='notify-select-all', component_property='n_clicks'),
    dash.dependencies.State('table', 'data'),
    prevent_initial_call=True
)
def select_all(n_clicks, table):
    if n_clicks > 0:
        return w_selected_rows(set(x for x in range(len(table))))
    raise PreventUpdate()
