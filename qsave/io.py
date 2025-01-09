import os
import logging

try:
    from msgspec.json import encode, decode
    from msgspec import DecodeError
except ImportError:
    log = logging.getLogger(__name__)
    log.warning("msgspec not installed. Install it with 'pip install msgspec' for better performance.")
    from json import dumps as encode, loads as decode
    from json.decoder import JSONDecodeError as DecodeError

from json.encoder import JSONEncoder


def write_file(
    filename: os.PathLike,
    data: dict[object, object],
    pretty: bool = False,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    sort_keys=False,
    indent=2,
    separators=None,
    default=None,
    **kwargs
) -> None:
    if pretty:
        pretty_encoder = JSONEncoder(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default
        )
        encoded_data = pretty_encoder.encode(data)
    else:
        encoded_data = encode(data, **kwargs)
        if isinstance(encoded_data, bytes):
            encoded_data = encoded_data.decode()

    with open(
        file=filename,
        mode="w"
    ) as f:
        f.write(encoded_data)


def open_file(
    filename: os.PathLike,
    **kwargs
) -> dict:
    try:
        with open(
            file=filename,
            mode="r"
        ) as f:
            return decode(f.read(), **kwargs)
    except FileNotFoundError:
        return {}
    except DecodeError:
        return {}
