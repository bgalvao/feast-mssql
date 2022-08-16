def arrow_to_mssql_type(t_str: str) -> str:
    # print(t_str)
    try:
        if t_str.startswith("timestamp") or t_str.startswith("datetime"):
            # return "timestamptz" if "tz=" in t_str else "timestamp"
            return "datetime2"
        return {
            "null": "null",
            "bool": "bit",
            "int8": "tinyint",
            "int16": "smallint",
            "int32": "int",
            "int64": "bigint",
            # not supported unless as strings smh
            # "list<item: int32>": "int[]",
            # "list<item: int64>": "bigint[]",
            # "list<item: bool>": "boolean[]",
            # "list<item: double>": "double precision[]",
            # "list<item: timestamp[us]>": "timestamp[]",
            "uint8": "smallint",
            "uint16": "int",
            "uint32": "bigint",
            "uint64": "bigint",
            # "float": "real",
            "float": "float",
            "double": "float",
            "binary": "binary",
            "string": "text",
        }[t_str]
    except KeyError:
        raise ValueError(f"Unsupported type: {t_str}")
