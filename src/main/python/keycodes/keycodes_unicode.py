import unicodedata
from collections import namedtuple

UNICODE_SYMBOLS = (
    '«»„“§—–-•'
    '×±≠≈‰'
    '°′″'
    '✓'
    '⌃⌥⇧⌘'
    '₽€'
    '®™©¢'
)

UnicodeEntry = namedtuple('UnicodeEntry',['symbol', 'qmk_id', 'label', 'tooltip'])

UNICODE_DATA = []

for s in UNICODE_SYMBOLS:
    name = unicodedata.name(s)
    entry = UnicodeEntry(
        symbol=s,
        qmk_id=f"UC_{name.replace(' ', '_').replace('-', '_')}",
        label=f"UC\n{s}",
        tooltip=f"Type '{s}' ({name.lower()})",
    )
    UNICODE_DATA.append(entry)
