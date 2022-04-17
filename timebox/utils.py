# From https://github.com/jmoiron/humanize/blob/master/src/humanize/filesize.py
suffixes = {
    "decimal": ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"),
    "binary": ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"),
    "gnu": "KMGTPEZY",
}


def naturalsize(value, binary=False, gnu=False, format="%.1f"):
    """
    Format a number of bytes like a human readable filesize (e.g. 10 kB).
    By default, decimal suffixes (kB, MB) are used.
    Non-GNU modes are compatible with jinja2's `filesizeformat` filter.
    Examples:
        ```pycon
        >>> naturalsize(3000000)
        '3.0 MB'
        >>> naturalsize(300, False, True)
        '300B'
        >>> naturalsize(3000, False, True)
        '2.9K'
        >>> naturalsize(3000, False, True, "%.3f")
        '2.930K'
        >>> naturalsize(3000, True)
        '2.9 KiB'
        ```
    Args:
        value (int, float, str): Integer to convert.
        binary (bool): If `True`, uses binary suffixes (KiB, MiB) with base
            2<sup>10</sup> instead of 10<sup>3</sup>.
        gnu (bool): If `True`, the binary argument is ignored and GNU-style
            (`ls -sh` style) prefixes are used (K, M) with the 2**10 definition.
        format (str): Custom formatter.
    Returns:
        str: Human readable representation of a filesize.
    """
    if gnu:
        suffix = suffixes["gnu"]
    elif binary:
        suffix = suffixes["binary"]
    else:
        suffix = suffixes["decimal"]

    base = 1024 if (gnu or binary) else 1000
    bytes = float(value)
    abs_bytes = abs(bytes)

    if abs_bytes == 1 and not gnu:
        return "%d Byte" % bytes
    elif abs_bytes < base and not gnu:
        return "%d Bytes" % bytes
    elif abs_bytes < base and gnu:
        return "%dB" % bytes

    for i, s in enumerate(suffix):
        unit = base ** (i + 2)
        if abs_bytes < unit and not gnu:
            return (format + " %s") % ((base * bytes / unit), s)
        elif abs_bytes < unit and gnu:
            return (format + "%s") % ((base * bytes / unit), s)
    if gnu:
        return (format + "%s") % ((base * bytes / unit), s)
    return (format + " %s") % ((base * bytes / unit), s)


def format_size(value):
    return naturalsize(value, binary=True)


# def compress(f_in):
#     with tempfile.NamedTemporaryFile() as f_out:

#     with gzip.open('/home/joe/file.txt.gz', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)


def generate_union_parser(union_type, union_type_name):
    def parse_union_type(cls, value):
        if not isinstance(value, dict):
            return value
        try:
            target_type = value.get("type")
        except Exception:
            raise ValueError(f"{union_type_name} config does not have a `type` field: {value}")
        import inspect

        accepted_types = {
            inspect.signature(t).parameters["type"].annotation.__args__[0]: t
            for t in union_type.__args__
        }
        target_class = accepted_types.get(target_type)
        if target_class is None:
            raise ValueError(f"{union_type_name} of type {target_type} does not exist ({value})")

        try:
            return target_class.parse_obj(value)
        except Exception as exc:
            print(f"Failed parsing {target_class.__name__} from {value}")
            print(exc)
            print()
            raise

    return parse_union_type


def generate_union_parser_list(union_type, union_type_name):
    parse_union_type = generate_union_parser(union_type, union_type_name)

    def parse_union_type_list(cls, value):
        if not isinstance(value, list):
            print("Expected {value} to be a list")
        return [parse_union_type(cls, elem) for elem in value]

    return parse_union_type_list
