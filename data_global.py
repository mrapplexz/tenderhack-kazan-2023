from pathlib import Path

import pandas as pd

from validation import split_log_msg

DATA_DIR = Path('data')

ERRORS = pd.read_csv(str(DATA_DIR / 'errors.csv')).set_index('id')
ERRORS['timestamp'] = pd.to_datetime(ERRORS['timestamp'])
ERRORS['log_split'] = ERRORS['logs'].apply(split_log_msg)
ERRORS['checkbox'] = '❌'

USERS = pd.read_csv(str(DATA_DIR / 'users.csv')).set_index('id')
