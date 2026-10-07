"""Offline acceptance check. Baseline intentionally fails; the resumed fix passes."""

from app import render


page = render('<img src=x onerror=alert(1)>', 'A&B "สมัคร"')
assert '&lt;img src=x onerror=alert(1)&gt;' in page, 'FAIL: title must be escaped as HTML text'
assert 'A&amp;B &quot;สมัคร&quot;' in page, 'FAIL: CTA must be escaped as HTML text'
assert '<img src=x onerror=alert(1)>' not in page, 'FAIL: input became an HTML element'
assert '<html lang="th">' in page, 'FAIL: preserve Thai page language'
assert 'href="/signup"' in page, 'FAIL: preserve approved signup URL'
print('PASS: title and CTA are escaped; Thai language and signup URL preserved.')
