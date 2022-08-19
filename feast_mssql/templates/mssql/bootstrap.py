import pymssql

from datetime import datetime, timedelta

import pyarrow as pa
import pandas as pd
import numpy as np

from feast_mssql.mssql_config import MSSQLConfig
from feast_mssql.connection_utils import (
    _get_conn,
    sql_create_table,
    sql_drop_table,
    sql_insert_values_into_table,
    sql_create_database,
)
from feast_mssql.type_map import arrow_to_mssql_type

import click

import pathlib
from typing import Dict


def get_feast_driver_test_data() -> pd.DataFrame:
    from feast.driver_test_data import create_driver_hourly_stats_df
    from datetime import datetime, timedelta

    end_date = datetime.now().replace(microsecond=0, second=0, minute=0)
    start_date = end_date - timedelta(days=15)

    driver_entities = [1001, 1002, 1003, 1004, 1005]
    driver_df = create_driver_hourly_stats_df(driver_entities, start_date, end_date)
    return driver_df


def get_repo_config_path() -> pathlib.Path:
    repo_path = pathlib.Path(__file__).parent.absolute()
    config_filepath = repo_path / "feature_store.yaml"
    return config_filepath


def config_cli() -> MSSQLConfig:
    return MSSQLConfig(
        host=click.prompt("MSSQL host", default="localhost"),
        port=click.prompt("MSSQL port", default="1433"),
        database=click.prompt("MSSQL DB name", default="feast_offline_store"),
        user=click.prompt("MSSQL user", default="sa"),
        password=click.prompt("MSSQL password", hide_input=True, default="Dck3r_pa55"),
    )


def overwrite_config(config_filepath: pathlib.Path, config: MSSQLConfig) -> None:
    def replace_str_in_file(file_path, match_str, sub_str):
        sub_str = str(sub_str)
        with open(file_path, "r") as f:
            contents = f.read()
        contents = contents.replace(match_str, sub_str)
        with open(file_path, "wt") as f:
            f.write(contents)

    replace_str_in_file(config_filepath, "DB_HOST", config.host)
    replace_str_in_file(config_filepath, "DB_PORT", config.port)
    replace_str_in_file(config_filepath, "DB_NAME", config.database)
    replace_str_in_file(config_filepath, "DB_USERNAME", config.user)
    replace_str_in_file(config_filepath, "DB_PASSWORD", config.password)


def bootstrap():
    # Bootstrap() will automatically be called from the init_repo() during `feast init`

    # get config file
    # create driver df
    # re-write config with user input

    driver_df = get_feast_driver_test_data()

    config_filepath = get_repo_config_path()
    config = config_cli()
    overwrite_config(config_filepath, config)

    if click.confirm(
        'Should I upload example data to MSSQL (overwriting "feast_driver_hourly_stats" table)?',
        default=True,
    ):
        table_name = "feast_driver_hourly_stats"
        with _get_conn(config=config) as connection:

            with connection.cursor() as cursor:
                # sql_create_database(config.database)
                # cursor.execute(f"USE {config.database};")
                cursor.execute(sql_drop_table(table_name))
                connection.commit()

                cursor.execute(sql_create_table(driver_df, table_name))
                connection.commit()

                insert_sql = sql_insert_values_into_table(driver_df, table_name)
                sql_data = tuple(map(tuple, driver_df.replace({np.NaN: None}).values))
                cursor.executemany(insert_sql, sql_data)
                connection.commit()


if __name__ == "__main__":
    bootstrap()
