from feast.repo_config import FeastConfigBaseModel
from pydantic import StrictStr
from pydantic.typing import Literal
from typing import Optional


class MSSQLConfig(FeastConfigBaseModel):
    host: StrictStr
    port: int = 1433
    database: StrictStr
    db_schema: Optional[StrictStr] = "dbo"
    user: StrictStr
    password: StrictStr
    sslmode: Optional[StrictStr] = None
    sslkey_path: Optional[StrictStr] = None
    sslcert_path: Optional[StrictStr] = None
    sslrootcert_path: Optional[StrictStr] = None
