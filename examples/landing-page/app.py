"""Intentionally unfinished fixture: escape user text before shipping."""


def render(title, cta):
    return (
        '<!doctype html><html lang="th"><head><meta charset="utf-8">'
        '<title>Demo</title></head><body>'
        f'<h1>{title}</h1><a href="/signup">{cta}</a>'
        '</body></html>'
    )
