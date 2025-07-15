from datetime import datetime


def filesize_filter(value):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if value < 1024:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} PB"


def datetime_filter(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M')
