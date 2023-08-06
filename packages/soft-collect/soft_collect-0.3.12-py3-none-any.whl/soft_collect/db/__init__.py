from .db2 import DB2
from .oracle import Oracle
from .sqlserver import SQLServer
from .postgres import Postgres

SUPPORTED_DBs = {
    "Oracle": Oracle,
    "DB2": DB2,
    "SQLServer": SQLServer,
    "Postgres": Postgres,
}


def get_DB_client(DBM, *args, **kwargs):
    return SUPPORTED_DBs[DBM](*args, **kwargs)
