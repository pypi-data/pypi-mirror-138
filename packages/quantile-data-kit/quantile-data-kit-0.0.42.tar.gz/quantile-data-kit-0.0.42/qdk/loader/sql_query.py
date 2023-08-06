from typing import Any, Dict, List, Optional, Union

import dask.dataframe as dd
import pandas as pd
from dagster import Field, Noneable, Permissive, StringSource
from qdk.loader.dataframe import DataFrameLoader


class SqlQueryLoader(DataFrameLoader):
    config_schema = {
        "connection_uri": Field(
            StringSource,
            description="The SqlAlchemy connection uri. (postgresql://user:password@host:port/database)",
        ),
        "query": Field(
            str,
            description="SQL query that needs to be executed.",
        ),
        "use_dask": Field(
            bool,
            default_value=False,
            description="Whether to load the dataframe using Dask.",
        ),
        "index_column": Field(
            Noneable(str),
            default_value=None,
            description="Which database column should be used as dataframe index.",
        ),
        "drop_na": Field(
            Noneable([str]),
            default_value=None,
            description="Whether to drop rows with missing values. ('column', or ['col_a', 'col_b'])",
        ),
        "drop_duplicates": Field(
            Noneable([str]),
            default_value=None,
            description="Whether to drop duplicates in certain columns. ('column', or ['col_a', 'col_b'])",
        ),
        "load_params": Field(
            Permissive({}),
            description="Extra parameters that get passed to the loading function.",
        ),
    }

    @classmethod
    def load(
        cls,
        connection_uri: str,
        query: str,
        use_dask: bool = False,
        index_column: Optional[str] = None,
        drop_na: List[str] = None,
        drop_duplicates: List[str] = None,
        load_params: Dict[str, Any] = {},
    ) -> Union[pd.DataFrame, dd.DataFrame]:
        # Choose which framework to use for data loading
        framework = dd if use_dask else pd

        # Query the database
        df = framework.read_sql_query(
            query,
            connection_uri,
            index_col=index_column,
            **load_params,
        )

        # Post process the data that is coming in
        df = cls.post_process(
            df,
            drop_na=drop_na,
            drop_duplicates=drop_duplicates,
            compute_ddf=False,
        )

        return df
