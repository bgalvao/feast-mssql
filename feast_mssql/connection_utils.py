from feast_mssql.mssql_config import MSSQLConfig
from feast_mssql.type_map import arrow_to_mssql_type
from pymssql import Connection, Cursor

import pandas as pd
import pyarrow as pa
import pymssql

from typing import Dict


def get_connection(config: MSSQLConfig) -> pymssql.Connection:
    return pymssql.connect(
        server=config.host,
        port=int(config.port),
        user=config.user,
        password=config.password,
        database=config.database,
    )


def sql_create_table(entity_df, table_name, cursor: Cursor = None) -> str | Cursor:
    pa_table = pa.Table.from_pandas(entity_df)

    columns = [
        f""""{f.name}" {arrow_to_mssql_type(str(f.type))}""" for f in pa_table.schema
    ]

    query = f"""CREATE TABLE "{table_name}" ({", ".join(columns)});"""

    if cursor is not None:
        cursor.execute(query)
        return cursor

    return query


def sql_drop_table(table_name: str, cursor: Cursor = None) -> str | Cursor:
    query = f"DROP TABLE IF EXISTS dbo.{table_name};"

    if cursor is not None:
        cursor.execute(query)
        return cursor
    return query


def sql_insert_values_into_table(
    table_name: str, df: pd.DataFrame, cursor: Cursor = None
) -> str | Cursor:
    query = f"""
        INSERT INTO dbo.{table_name} VALUES {', '.join( ("%s",) * len(df.columns))};
    """
    if cursor is not None:
        sql_data = tuple(map(tuple, df.values))
        cursor.executemany(query, sql_data)
        return cursor
    else:
        return query
