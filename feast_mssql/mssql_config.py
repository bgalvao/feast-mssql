from feast.repo_config import FeastConfigBaseModel
from pydantic import StrictStr
from pydantic.typing import Literal

class MSSQLConfig(FeastConfigBaseModel):
    host: StrictStr
    port: int = 1433
    database: StrictStr
    user: StrictStr
    password: StrictStr
    type: Literal["feast_mssql.MSSQLOfflineStore"] = "feast_mssql.MSSQLOfflineStore"
