from typing import Tuple

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px

import pandas as pd
import datetime as dt

from data_global import USERS


def build_top(top_errors: pd.DataFrame, col: str, name: str) -> str:
    error_str = [f'### {name}\n\n']
    for _, top_error in top_errors.iterrows():
        error_str.append('**')
        error_str.append(top_error[col])
        error_str.append('** - ')
        error_str.append(str(top_error['count']))
        error_str.append(' пользователей\n\n')
    return ''.join(error_str)


def tab_by_user_component(errors: pd.DataFrame, percent: bool):
    total_counts = errors.groupby('timestamp_trunc')['user_id'].nunique().reset_index(name='count')
    if percent:
        total_counts['count'] = total_counts['count'] / len(USERS)
    yaxes = [0, total_counts['count'].max() * 1.1] if percent else [0, total_counts['count'].max() + 10]
    types_counts = errors.groupby(['timestamp_trunc', 'error_type'])['user_id'].nunique().reset_index(name='count')
    if percent:
        types_counts['count'] = types_counts['count'] / len(USERS)
    top_errors_by_type = errors.groupby('error_type')['user_id'].nunique().reset_index(
        name='count'
    ).sort_values(by='count', ascending=False)[:5]
    top_errors_by_unique = errors.groupby('log_split')['user_id'].count().reset_index(
        name='count'
    ).sort_values(by='count', ascending=False)[:5]


    error_str_by_type = build_top(top_errors_by_type, 'error_type', 'ТОП по типам')
    error_str_by_unique = build_top(top_errors_by_unique, 'log_split', 'ТОП по ошибкам')

    return dbc.Col([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.line(total_counts, x='timestamp_trunc', y='count', markers=True).update_yaxes(range=yaxes),
                    config={'locale': 'ru'}
                ),
                dcc.Markdown(
                    error_str_by_type
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(types_counts, x='timestamp_trunc', y='count', color='error_type').update_yaxes(range=yaxes),
                    config={'locale': 'ru'}
                ),
                dcc.Markdown(
                    error_str_by_unique
                )
            ], width=6)
        ])
    ])
