from feast_mssql.mssql_config import MSSQLConfig
from feast_mssql.type_map import arrow_to_mssql_type
from pymssql import Connection, Cursor

import pandas as pd
import numpy as np
import pyarrow as pa
import pymssql

from typing import Dict


def _get_conn(config: MSSQLConfig) -> pymssql.Connection:
    return pymssql.connect(
        server=config.host,
        port=int(config.port),
        user=config.user,
        password=config.password,
        database=config.database,
        # TODO: add SSL options for secure connectivity
    )


def _df_to_create_table_sql(entity_df: pd.DataFrame, table_name: str) -> str:
    """
    Generate the SQL to create a table with column names and types in entity_df.
    """
    pa_table = pa.Table.from_pandas(entity_df)
    columns = [
        f""""{f.name}" {arrow_to_mssql_type(str(f.type))}""" for f in pa_table.schema
    ]
    return f"""CREATE TABLE "{table_name}" ({", ".join(columns)});"""


def df_to_mssql_table(
    config: MSSQLConfig, entity_df: pd.DataFrame, table_name: str
) -> Dict[str, np.dtype]:
    """
    Create a table for the data frame, insert all the values, and return the table schema
    """
    query = f"""
        INSERT INTO {schema}.{table_name} VALUES ({', '.join( ("%s",) * len(entity_df.columns))});
    """
    with _get_conn(config) as conn, conn.cursor() as cur:
        # create table
        cur.execute(_df_to_create_table_sql(entity_df, table_name))
        # insert values into table
        sql_data = tuple(
            map(tuple, entity_df.replace({np.NaN: None}).values)
        )  # prepare data for pymssql
        cur.executemany(query, sql_data)  # execute insert
        conn.commit()  # commit necessary to persist data in db
        return dict(zip(entity_df.columns, entity_df.dtypes))


def get_query_schema(config: MSSQLConfig, sql_query: str) -> Dict[str, np.dtype]:
    with _get_conn(config) as connection:
        connection.set_session(readonly=True)
        df = pd.read_sql(
            f"SELECT TOP (0) * FROM {sql_query}",
            connection,
        )
        return dict(zip(df.columns, df.dtypes))


def sql_create_table(entity_df, table_name, cursor: Cursor = None) -> str | Cursor:
    pa_table = pa.Table.from_pandas(entity_df)
    columns = [
        f""""{f.name}" {arrow_to_mssql_type(str(f.type))}""" for f in pa_table.schema
    ]
    return f"""CREATE TABLE "{table_name}" ({", ".join(columns)});"""


def sql_drop_table(
    table_name: str, cursor: Cursor = None, schema="dbo"
) -> str | Cursor:
    query = f"DROP TABLE IF EXISTS {schema}.{table_name};"

    if cursor is not None:
        cursor.execute(query)
        return cursor
    return query


def sql_insert_values_into_table(
    entity_df: pd.DataFrame, table_name: str, cursor: Cursor = None, schema="dbo"
) -> str | Cursor:
    query = f"""
        INSERT INTO {schema}.{table_name} VALUES ({', '.join( ("%s",) * len(entity_df.columns))});
    """
    if cursor is not None:
        sql_data = tuple(map(tuple, entity_df.replace({np.NaN: None}).values))
        cursor.executemany(query, sql_data)
        return dict(zip(entity_df.columns, entity_df.dtypes))
        return cursor
    else:
        return query


def sql_create_database(database_name: str, cursor: Cursor = None) -> str | Cursor:
    query = f"""
        IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{database_name}')
        BEGIN
            CREATE DATABASE {database_name};
        END;
    """
    if cursor is not None:
        cursor.execute(query)
        return cursor
    else:
        return query
