"""
Textbase parser for Iconclass data files.

Parses the custom text-based record format used by Iconclass (notations.txt, keys.txt).
Records are separated by a '$' on its own line. Fields are uppercase single-letter codes
(N, C, K, S, R) followed by values; continuation lines start with ';'.

Replaces the previously external `textbase` dependency used by make_index.py and make_skos.py.
Based on the inline parser in make_sqlite.py (from github.com/iconclass/data).
"""


def parse(filename):
    """Yield parsed record dicts from an Iconclass textbase file.

    Each record is a dict mapping uppercase field names to lists of values,
    except 'N' and 'K' which are single-element lists (matching the original
    textbase module's behavior expected by make_index.py and make_skos.py).
    """
    with open(filename, "rt", encoding="utf8") as f:
        content = f.read()

    for chunk in content.split("\n$"):
        obj = _parse_record(chunk)
        if obj:
            yield obj


def _parse_record(chunk):
    """Parse a single $-delimited record into a dict."""
    obj = {}
    buf = []
    last_field = None

    for line in chunk.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split(" ", 1)
        if len(parts) < 2:
            continue

        field = parts[0]
        value = parts[1]

        if field == ";":
            buf.append(value)
        elif field != last_field:
            if last_field is not None and buf:
                obj[last_field] = buf
            buf = [value]
            last_field = field
        else:
            buf.append(value)

    if last_field is not None and buf:
        obj[last_field] = buf

    return obj if obj else None
