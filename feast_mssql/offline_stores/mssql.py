from feast.infra.offline_stores.offline_store import (
    OfflineStore,
    RetrievalJob
)
from feast.data_source import DataSource
from feast.repo_config import FeastConfigBaseModel

from pydantic import StrictStr
from pydantic.typing import Literal

# OfflineStore class definition
# minimum set of functions to be implemented
class MSSQLOfflineStore(OfflineStore):

    @staticmethod
    def pull_latest_from_table_or_query(
        config: RepoConfig,
        data_source: DataSource,
        join_key_columns: List[str],
        feature_name_columns: List[str],
        event_timestamp_column: str,
        created_timestamp_column: Optional[str],
        start_date: datetime,
        end_date: datetime,
    ) -> RetrievalJob:
        
        assert isinstance(data_source, MSSQLDataSource)
        from_expression = data_source.get_table_query_string()

        return MSSQLRetrievalJob(evaluation_function)

    @staticmethod
    def get_historical_features(
        config: RepoConfig,
        feature_views: List[FeatureView],
        feature_refs: List[str],
        entity_df: Union[pd.DataFrame, str],
        registry: Registry,
        project: str,
        full_feature_names: bool = False,
    ) -> RetrievalJob:
        raise NotImplementedError
        return MSSQLRetrievalJob

# Type Mapping, so that feast does not cast types incorrectly
class MSSQLDataSource(DataSource):

    @staticmethod
    def source_datatype_to_feast_value_type():
        pass

    def get_column_names_and_types():
        pass

    def get_table_query_string():
        raise NotImplementedError

    @staticmethod
    def from_proto(data_source: DataSourceProto):
        pass

    def to_proto(self) -> DataSourceProto:
        pass


class MSSQLRetrievalJob(RetrievalJob):

    def __init__(self, evaluation_function: Callable):
        """Initialize a lazy historical retrieval job"""

        # The evaluation function executes a stored procedure to compute a historical retrieval.
        self.evaluation_function = evaluation_function

    def to_df(self):
        # Only execute the evaluation function to build the final historical retrieval dataframe at the last moment.
        df = self.evaluation_function()
        return df

    def to_arrow(self):
        # Only execute the evaluation function to build the final historical retrieval dataframe at the last moment.
        df = self.evaluation_function()
        return pyarrow.Table.from_pandas(df)

    # def to_remote_storage(self):
    #     # Optional method to write to an offline storage location to support scalable batch materialization.
    #     pass


