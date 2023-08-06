from typing import Any, Optional, Tuple, Type

from dataclass_csv import DataclassReader

from .classes import Preheader, Radio, fields


def map_fields(reader: DataclassReader) -> DataclassReader:
    for key, value in fields.items():
        reader.map(key).to(value)
    return reader


def parse_preheader(line: str) -> Preheader:
    args = []
    kwargs = {}
    for item in line.strip().replace("appRelease", "app_release").split(","):
        if "=" in item:
            key, value = item.split("=", 1)
            kwargs[key] = value
        else:
            args.append(item)
    return Preheader(*args, **kwargs)


def read(
    f: Any,
    cls: Type[object] = Radio,
    ignore_preheader: bool = False,
    *args: Any,
    **kwargs: Any,
) -> Tuple[Optional[Preheader], DataclassReader]:
    first_line = f.readline()
    preheader = None
    f.seek(0)  # go back to header for reader
    if first_line.startswith("WigleWifi"):
        if not ignore_preheader:
            preheader = parse_preheader(first_line)
        next(f)  # header is on second line

    reader = DataclassReader(f, cls, *args, **kwargs)
    reader = map_fields(reader)

    return preheader, reader
