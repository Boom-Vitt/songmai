"""Completed version of the offline handoff fixture."""

from html import escape


def render(title, cta):
    return (
        '<!doctype html><html lang="th"><head><meta charset="utf-8">'
        '<title>Demo</title></head><body>'
        f'<h1>{escape(title)}</h1><a href="/signup">{escape(cta)}</a>'
        '</body></html>'
    )
