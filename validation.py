import datetime as dt


def split_log_msg(s: str):
    return s[:10]


def fmtdate(date: dt.date):
    return date.strftime('%d.%m.%Y')


def parse_date(date: str) -> dt.date:
    return dt.datetime.strptime(date, '%d.%m.%Y').date()


def fmtdates(d1: dt.date, d2: dt.date):
    return f'{fmtdate(d1)}-{fmtdate(d2)}'


def parse_dates(dates: str):
    dates = dates.split('-', maxsplit=1)
    if len(dates) != 2:
        return None
    d1, d2 = dates
    try:
        d1 = parse_date(d1)
        d2 = parse_date(d2)
        return d1, d2
    except:
        return None
